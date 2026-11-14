"""Enrich candidate papers with bibliographic metadata (PubMed) and study context (System API).

- PubMed esummary: title, journal, publication date, DOI (batched, 150 PMIDs per call)
- System /v1/studies?filter=pubmed_id:<pmid>: system study_id, population text, study_type
Country is parsed from the population text first, then the title (author affiliations are never used).
Failures are recorded, not dropped.
"""
from __future__ import annotations

import json
import re
import time
from concurrent.futures import ThreadPoolExecutor

import pandas as pd
import requests

from common import INTERIM, SystemAPI, log_request, write_json

EUTILS = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi"

COUNTRIES = [
    "Benin", "Burkina Faso", "Burundi", "Cameroon", "Central African Republic", "Chad", "Congo",
    "Democratic Republic of the Congo", "DRC", "Côte d'Ivoire", "Cote d'Ivoire", "Ivory Coast", "Equatorial Guinea",
    "Ethiopia", "Gabon", "Gambia", "Ghana", "Guinea-Bissau", "Guinea", "Kenya", "Liberia", "Madagascar", "Malawi",
    "Mali", "Mauritania", "Mozambique", "Niger", "Nigeria", "Rwanda", "Senegal", "Sierra Leone", "Somalia",
    "South Sudan", "Sudan", "Tanzania", "Togo", "Uganda", "Zambia", "Zimbabwe", "Angola", "Eritrea", "Namibia",
    "India", "Myanmar", "Cambodia", "Laos", "Vietnam", "Thailand", "Indonesia", "Papua New Guinea", "Solomon Islands",
    "Vanuatu", "Bangladesh", "Pakistan", "Afghanistan", "Sri Lanka", "Brazil", "Peru", "Colombia", "Venezuela",
    "Haiti", "Yemen", "Sahel", "sub-Saharan Africa",
]
ALIASES = {"DRC": "Democratic Republic of the Congo", "Cote d'Ivoire": "Côte d'Ivoire",
           "Ivory Coast": "Côte d'Ivoire"}
CRX = re.compile(r"\b(" + "|".join(re.escape(c) for c in sorted(COUNTRIES, key=len, reverse=True)) + r")\b", re.I)


def countries_in(text: str) -> list[str]:
    found = []
    for m in CRX.finditer(text or ""):
        name = next(c for c in COUNTRIES if c.lower() == m.group(1).lower())
        name = ALIASES.get(name, name)
        if name == "Guinea" and re.search(r"(equatorial|papua new|guinea-bissau)", text, re.I):
            continue
        if name == "Niger" and re.search(r"nigeria", m.string[m.start():m.end() + 2], re.I):
            continue
        if name not in found:
            found.append(name)
    return found


def pubmed_meta(pmids: list[str]) -> dict:
    out = {}
    for i in range(0, len(pmids), 150):
        batch = pmids[i:i + 150]
        params = {"db": "pubmed", "id": ",".join(batch), "retmode": "json"}
        r = requests.get(EUTILS, params=params, timeout=60)
        log_request("pubmed", EUTILS, {"db": "pubmed", "n_ids": len(batch)}, r.status_code, None)
        r.raise_for_status()
        res = r.json().get("result", {})
        for pmid in batch:
            d = res.get(pmid)
            if not d or "error" in d:
                out[pmid] = {"pubmed_status": "not returned"}
                continue
            doi = next((a["value"] for a in d.get("articleids", []) if a.get("idtype") == "doi"), None)
            out[pmid] = {
                "pubmed_status": "ok", "title": d.get("title"), "journal": d.get("fulljournalname") or d.get("source"),
                "pubdate": d.get("pubdate"), "year": (d.get("pubdate") or "")[:4], "doi": doi,
                "pubtype": d.get("pubtype", []),
            }
        time.sleep(0.4)
    return out


def system_study(api: SystemAPI, pmid: str) -> dict:
    try:
        rows = api.get("/v1/studies", {"filter": f"pubmed_id:{pmid}", "limit": 5}).get("data", [])
    except Exception as exc:  # noqa: BLE001 - record and continue
        return {"system_status": f"error: {exc.__class__.__name__}"}
    if not rows:
        return {"system_status": "no study record"}
    s = rows[0]
    return {"system_status": "ok", "system_study_id": s.get("system_id") or s.get("study_id"),
            "population": s.get("population"), "study_type": s.get("study_type"),
            "system_doi": s.get("doi")}


def main() -> None:
    cand = pd.read_csv(INTERIM / "candidates.csv", dtype=str, keep_default_na=False)
    pmids = sorted(set(cand["pubmed_id"]) - {""})
    meta = pubmed_meta(pmids)
    api = SystemAPI(sleep_s=0.0)
    with ThreadPoolExecutor(max_workers=6) as ex:
        studies = dict(zip(pmids, ex.map(lambda p: system_study(api, p), pmids)))
    papers = []
    for p in pmids:
        rec = {"pubmed_id": p, **meta.get(p, {}), **studies.get(p, {})}
        pop_c = countries_in(rec.get("population") or "")
        title_c = countries_in(rec.get("title") or "")
        rec["countries"] = pop_c or title_c
        rec["country_source"] = "population" if pop_c else ("title" if title_c else "unknown")
        papers.append(rec)
    write_json(INTERIM / "papers.json", papers)
    df = pd.DataFrame(papers)
    print("papers:", len(df), "| pubmed ok:", (df.pubmed_status == "ok").sum(),
          "| system study ok:", (df.system_status == "ok").sum(),
          "| country known:", (df.country_source != "unknown").sum())
    print(df.country_source.value_counts().to_dict())


if __name__ == "__main__":
    main()
