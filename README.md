# PATH malaria visualization — raw data

Downloaded/prepared on 2026-11-14. **No data cleaning, filtering of downloaded rows, merging, correction or effect-size conversion has been performed.** WHO/MAP requests select geography and indicators at the source; their responses are saved unchanged. Sources and scope are below.

## Contents

- `data/raw/system/`: complete associations, studies, variables and concepts CSVs from System Public Graph, stored with lossless gzip compression. Associations reuse the user-supplied snapshot and are checked against the publisher manifest. Other tables use Dataverse `format=original`. The relationships table is not included: the current cleaning workflow uses association-level evidence and its study/variable/concept lookup tables.
- `data/raw/pf8/`: sample metadata, resistance marker genotypes, inferred resistance classifications, classification rules PDF and README. These are complete publisher files, not country subsets. Five files verified against Zenodo MD5 checksums.
- `data/raw/who/`: raw GHO JSON for Benin (`BEN`) and Tanzania (`TZA`), all returned years, four indicators: ITN use, ITN access, estimated malaria incidence and IRS coverage. No unit conversion. Base endpoint: `https://ghoapi.azureedge.net/api/`; query filter: `SpatialDim eq 'BEN' or SpatialDim eq 'TZA'`. `itn_use.json` is `MALARIA_ITN_USE`.
- `data/raw/map/`: JSON-stat national estimates for BEN/TZA, release **202608**, metrics `Pf_PR-rate`, `Pf_incidence-rate`, `ITN_use-rate`, each with mean/lower/upper responses. No reshaping. Query pattern: `https://data.malariaatlas.org/map-platform-app-backend/api/v1/trends/{malaria|interventions}/{metric}/admin0/{mean|lci|uci}?version=202608&iso3={BEN|TZA}`.
- `data/raw/literature/`: Europe PMC raw core metadata for 11 target PMIDs, an additional SMC search response and eight available full-text XML files. Full text was not available through this endpoint for every paper. Absence of an XML is not evidence that a study is absent.
- `metadata/`: raw publisher records, MAP access guide and releases, and SHA-256/byte counts for all packaged data files.

## Restore original System CSVs

GitHub cannot store a file above 100 MiB in normal Git. The 208 MB association gzip is therefore split into three consecutive byte parts. **This is packaging only; no rows were changed.** Other CSVs are single gzip files. Run:

```sh
python3 scripts/restore_system.py
```

The script restores to `data/restored/system/` and verifies each CSV against the publisher's SHA-256. Restored files are gitignored.

## Sources and attribution

1. **System, Inc., System Public Graph**, Harvard Dataverse DOI [10.7910/DVN/7V6JDO](https://doi.org/10.7910/DVN/7V6JDO), **CC BY-NC 4.0**. See `metadata/system_dataset.json` and `data/raw/system/MANIFEST.json`. Noncommercial terms remain applicable.
2. **MalariaGEN Pf8**, [dataset repository](https://zenodo.org/records/18681980), CC BY 4.0 per repository metadata. Cite MalariaGEN et al., *Pf8: an open dataset of Plasmodium falciparum genome variation in 33,325 worldwide samples*, DOI [10.12688/wellcomeopenres.24031.1](https://doi.org/10.12688/wellcomeopenres.24031.1). Original filenames, contents and publisher documentation retained.
3. **WHO Global Health Observatory**, [malaria data](https://www.who.int/data/gho/data/themes/malaria). Retain WHO attribution and applicable source terms. Country-level modeled context is not a trial effect estimate.
4. **Malaria Atlas Project**, [data platform](https://data.malariaatlas.org/). Attribution and metric-specific source terms apply; preserve release and source metadata. `metadata/map_access_guide.txt` explains metrics, missing values and interpretation.
5. **Article authors/publishers; Europe PMC**. Metadata/API: `https://www.ebi.ac.uk/europepmc/webservices/rest/`. Full text: `/{PMCID}/fullTextXML`. Individual article licenses are retained in each XML's permissions section; there is no blanket repository license over third-party articles or datasets.

## Limitations and next steps

- This is an input collection, **not a validated analytical dataset**. Raw graph errors and missing values are retained.
- Pf8 describes parasite drug-resistance markers; it does not measure mosquito insecticide resistance or directly estimate SMC protection.
- WHO/MAP data currently cover two demo countries. They do not cover all SMC/vaccine study countries.
- Core metadata PMIDs: 35339225, 37776879, 36706778, 38401551, 38310910, 34432975, 33278936, 34894221, 27875528, 36704118, 30398672.
- DHS, complete genome sequences, rasters and the System relationships table are not downloaded; they are optional for the agreed first cleaning stage.
- AI assistance: OpenAI Codex was used to locate/download sources, package raw files and write provenance documentation.
