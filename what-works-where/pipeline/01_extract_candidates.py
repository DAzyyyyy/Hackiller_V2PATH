"""Scan the fixed Dataverse association snapshot and export malaria-prevention candidates.

Two passes over the 2M-row CSV:
  1. collect PMIDs whose variables mention malaria context (malaria, Plasmodium, Anopheles, ...)
  2. keep rows where a variable names one of the three PATH interventions (nets / SMC / vaccines)
     AND the paper has malaria context (this removes 'SMC = smooth muscle cell', pyriproxyfen
     for cats, chlorfenapyr residues on vegetables, etc.)
Outputs data/interim/candidates.csv plus a JSON summary.
"""
from __future__ import annotations

import re

import pandas as pd

from common import INTERIM, RAW_CSV, write_json

MALARIA_CTX = re.compile(r"malaria|plasmodium|falciparum|anophel|mosquito|parasit(a)?emi", re.I)

CLASSES = {
    "nets": re.compile(
        r"\bitns?\b|\bllins?\b|bed ?nets?|bednets?|mosquito nets?|insecticid\w*[- ]treated (bed ?)?nets?"
        r"|long[- ]lasting insecticid\w*|interceptor\s*g2|\big2\b|olyset|permanet|royal ?guard|pronet"
        r"|piperonyl|\bpbo\b|chlorfenapyr|pyriproxyfen|dual[- ]a(ctive)?[- ]?i(ngredient)?",
        re.I),
    "smc": re.compile(
        r"seasonal malaria chemopreven|\bsmc\b|\bspaq\b|\bsp ?\+ ?aq\b|sulfadoxine[- ]pyrimethamine"
        r"( plus| and| \+) amodiaquine|intermittent preventive treatment in children|\biptc\b",
        re.I),
    "vaccines": re.compile(
        r"rts,? ?s|\br21\b|malaria vaccin|mosquirix|matrix-m|vaccin\w* against malaria", re.I),
}

USECOLS = None  # keep every column of the snapshot
CHUNK = 250_000


def main() -> None:
    # pass 1: malaria-context PMIDs
    ctx_pmids: set[str] = set()
    n_rows = 0
    for chunk in pd.read_csv(RAW_CSV, dtype=str, chunksize=CHUNK, keep_default_na=False):
        n_rows += len(chunk)
        text = chunk["variable_1_name"] + " || " + chunk["variable_2_name"]
        hit = text.str.contains(MALARIA_CTX)
        ctx_pmids.update(chunk.loc[hit, "pubmed_id"].tolist())

    # pass 2: intervention rows within malaria papers
    keep = []
    for chunk in pd.read_csv(RAW_CSV, dtype=str, chunksize=CHUNK, keep_default_na=False):
        text = chunk["variable_1_name"] + " || " + chunk["variable_2_name"]
        in_ctx = chunk["pubmed_id"].isin(ctx_pmids) | text.str.contains(MALARIA_CTX)
        flags = {name: text.str.contains(rx) for name, rx in CLASSES.items()}
        any_hit = flags["nets"] | flags["smc"] | flags["vaccines"]
        sel = in_ctx & any_hit
        if sel.any():
            sub = chunk.loc[sel].copy()
            sub["class"] = [
                ";".join(n for n in CLASSES if flags[n].loc[i]) for i in sub.index
            ]
            keep.append(sub)

    cand = pd.concat(keep, ignore_index=True).drop_duplicates("system_id")
    for col in ("statistic_value", "ci_lower", "ci_upper", "ci_level", "p_value"):
        cand[col + "_num"] = pd.to_numeric(cand[col], errors="coerce")
    INTERIM.mkdir(parents=True, exist_ok=True)
    cand.to_csv(INTERIM / "candidates.csv", index=False)

    summary = {
        "snapshot_rows": n_rows,
        "malaria_context_pmids": len(ctx_pmids),
        "candidates": len(cand),
        "candidate_pmids": int(cand["pubmed_id"].nunique()),
        "by_class": {n: int(cand["class"].str.contains(n).sum()) for n in CLASSES},
        "pmids_by_class": {n: int(cand.loc[cand["class"].str.contains(n), "pubmed_id"].nunique())
                           for n in CLASSES},
        "with_both_ci": int((cand["ci_lower_num"].notna() & cand["ci_upper_num"].notna()).sum()),
        "statistic_types": cand["system_statistic_type"].value_counts().head(15).to_dict(),
    }
    write_json(INTERIM / "candidates_summary.json", summary)
    print(summary)


if __name__ == "__main__":
    main()
