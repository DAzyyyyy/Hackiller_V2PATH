"""Assemble the small JSON files the static site reads (all well under 25 MB).

site/data/verified.json      hand-verified results (paper-checked), one row per comparison x time point
site/data/graph.json         graph candidates (raw, not yet reviewed) joined with paper metadata
site/data/context.json       graph neighbourhood, anchor coverage, WHO country context, summary counts
"""
from __future__ import annotations

import json

import pandas as pd
import requests

from common import GRAPH, INTERIM, SITE_DATA, VERIFIED, log_request, write_json

WHO = "https://ghoapi.azureedge.net/api/"
WHO_INDICATORS = {
    "MALARIA_ITN_USE": "Population sleeping under an ITN (%) — modelled",
    "MALARIA_ITN_COVERAGE": "Population with access to an ITN (%) — modelled",
    "MALARIA_EST_INCIDENCE": "Estimated malaria incidence (per 1,000 at risk)",
}
WHO_COUNTRIES = {"TZA": "Tanzania", "BEN": "Benin", "MLI": "Mali", "BFA": "Burkina Faso"}


def who_context() -> list[dict]:
    rows = []
    for code, label in WHO_INDICATORS.items():
        flt = " or ".join(f"SpatialDim eq '{c}'" for c in WHO_COUNTRIES)
        params = {"$filter": f"({flt}) and TimeDim ge 2010"}
        try:
            r = requests.get(WHO + code, params=params, timeout=60)
            log_request("who-gho", WHO + code, params, r.status_code, None)
            r.raise_for_status()
        except requests.RequestException as exc:
            print("WHO fetch failed", code, exc)
            continue
        for v in r.json().get("value", []):
            rows.append({"indicator": code, "label": label, "iso3": v["SpatialDim"],
                         "country": WHO_COUNTRIES.get(v["SpatialDim"]), "year": v["TimeDim"],
                         "value": v.get("NumericValue"), "low": v.get("Low"), "high": v.get("High")})
    return rows


def main() -> None:
    ver = pd.read_csv(VERIFIED / "evidence_verified.csv", dtype=str, keep_default_na=False)
    for c in ("estimate", "ci_lower", "ci_upper", "followup_months", "publication_year"):
        ver[c] = pd.to_numeric(ver[c], errors="coerce")
    write_json(SITE_DATA / "verified.json", json.loads(ver.to_json(orient="records")))

    gc_path = VERIFIED / "evidence_graph_checked.csv"
    gchk = pd.read_csv(gc_path, dtype=str, keep_default_na=False) if gc_path.exists() else pd.DataFrame()
    for c in ("estimate", "ci_lower", "ci_upper", "followup_months", "publication_year"):
        if c in gchk:
            gchk[c] = pd.to_numeric(gchk[c], errors="coerce")
    write_json(SITE_DATA / "graph_checked.json", json.loads(gchk.to_json(orient="records")) if len(gchk) else [])

    cand = pd.read_csv(INTERIM / "candidates_classified.csv", dtype=str, keep_default_na=False)
    papers = {p["pubmed_id"]: p for p in json.loads((INTERIM / "papers.json").read_text())}
    keep_cols = ["system_id", "pubmed_id", "study_id", "statistic_type", "system_statistic_type",
                 "statistic_value", "ci_lower", "ci_upper", "ci_level", "p_value", "p_value_equality",
                 "variable_1_name", "variable_2_name", "intervention_class", "intervention_subtype",
                 "intervention_text", "outcome_text", "role", "outcome_tier", "stat_family",
                 "plottable_ratio", "direction", "ci_excludes_null", "qc_flags"]
    g = cand[keep_cols].copy()
    for c in ("statistic_value", "ci_lower", "ci_upper", "ci_level", "p_value"):
        g[c] = pd.to_numeric(g[c], errors="coerce")
    g["plottable_ratio"] = g["plottable_ratio"].eq("True")
    recs = json.loads(g.to_json(orient="records"))
    verified_pmids = set(ver["pmid"])
    for r in recs:
        p = papers.get(r["pubmed_id"], {})
        r.update({
            "title": p.get("title"), "journal": p.get("journal"), "year": p.get("year"),
            "doi": p.get("doi") or p.get("system_doi"), "countries": p.get("countries", []),
            "country_source": p.get("country_source"), "population": p.get("population"),
            "study_type": p.get("study_type"), "in_verified_set": r["pubmed_id"] in verified_pmids,
        })
    write_json(SITE_DATA / "graph.json", recs)

    ctx = json.loads((GRAPH / "graph_context.json").read_text())
    summ = json.loads((INTERIM / "candidates_summary.json").read_text())
    effect = g[g.role != "uptake / behaviour"]
    context = {
        "summary": {
            "snapshot_rows": summ["snapshot_rows"],
            "candidate_associations": summ["candidates"],
            "candidate_papers": summ["candidate_pmids"],
            "effect_associations": int(len(effect)),
            "effect_papers": int(effect.pubmed_id.nunique()),
            "plottable_ratio_associations": int(g.plottable_ratio.sum()),
            "flagged_associations": int((g.qc_flags.str.len() > 0).sum()),
            "verified_results": int(len(ver)),
            "verified_trials": int(ver.trial_family_id.nunique()),
            "verified_papers": int(ver.pmid.nunique()),
            "graph_rows_abstract_checked": int(len(gchk)),
            "graph_rows_needing_context": int((gchk.verification_status != "checked against abstract").sum()) if len(gchk) else 0,
            "label_corrections": int(ver.verification_status.isin(
                ["label corrected", "comparator restored", "time point restored"]).sum()
                + (ver.verification_note.str.contains("restored from paper")).sum()),
        },
        "malaria_neighbourhood": ctx["neighbourhoods"].get("malaria", [])[:300],
        "intervention_neighbourhoods": {k: v for k, v in ctx["neighbourhoods"].items() if k != "malaria"},
        "concepts": {k: {"system_id": v["system_id"], "wikidata_id": v.get("wikidata_id")}
                     for k, v in ctx["concepts"].items()},
        "anchor_coverage": ctx["anchor_coverage"],
        "who": who_context(),
    }
    write_json(SITE_DATA / "context.json", context)
    print(json.dumps(context["summary"], indent=1), "| who rows:", len(context["who"]))


if __name__ == "__main__":
    main()
