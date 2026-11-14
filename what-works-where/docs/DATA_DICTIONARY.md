# Data dictionary

Everything the front end needs is in `site/data/` (static JSON, about 0.9 MB in total). Nothing at
runtime calls an API.

## site/data/verified.json — paper-verified anchor results (20 rows; 11 also checked in full text by AI-2)

One row per comparison × follow-up. Source: `data/verified/evidence_verified.csv` (hand-entered from the papers).

| Field | Meaning |
|---|---|
| `result_id` | Stable id, e.g. `BJ24-CFP` |
| `trial_family_id`, `registration` | One trial = one family, e.g. NCT03931473. Count independent evidence by family, not by paper |
| `pmid`, `short_ref`, `source_url` | Paper |
| `intervention_class` | `nets` \| `smc` \| `vaccines` \| `combination` |
| `intervention`, `comparator` | What was compared with what, as defined in the paper |
| `country`, `site`, `population` | Setting (country taken from the study site, not author affiliation) |
| `outcome_tier` | `vector / entomological`, `infection`, `clinical malaria`, `severe / hospital`, `anaemia & growth`, `mortality` |
| `outcome_definition` | Exact outcome |
| `effect_measure` | OR, aOR, HR, IRR, rate ratio, or "… (from VE = 1 − HR)" / "protective efficacy (as 1 − ratio)" when we converted a percentage |
| `estimate`, `ci_lower`, `ci_upper`, `ci_level` | On the ratio scale. Below 1 = fewer events with the intervention |
| `p_operator` | `<` or `=` as printed in the paper |
| `followup_label`, `followup_months` | Time since deployment. Not the publication year |
| `publication_year` | Year of the paper |
| `origin` | `graph + paper` or `paper only` |
| `graph_api_status`, `graph_csv_status`, `graph_association_id`, `graph_original_label` | Where the result appears in the graph and what label the graph gave it |
| `verification_status` | `checked against paper`, `label corrected`, `comparator restored`, `time point restored`, `paper supplement` |
| `verification_note` | Why (free text) |
| `iso3` | `;`-joined ISO3; **empty = multi-country or review** (show as "multi-country") |
| `fulltext_location`, `fulltext_quoted_text`, `fulltext_value_found`, `fulltext_ci_found`, `fulltext_matches_our_value`, `fulltext_discrepancy_note` | AI-2 full-text check (empty if no XML). `matches_our_value = N` rows were context corrections, now applied |

## site/data/graph_checked.json — graph rows reviewed against the abstract (33 rows)

Same comparison fields as `verified.json`, plus:

| Field | Meaning |
|---|---|
| `graph_association_id` | System association `system_id` |
| `graph_original_label` | `variable_1 -> variable_2` exactly as stored in the graph |
| `graph_statistic` | Statistic as stored in the graph, e.g. `hazard_ratio 62.7 (51.6-71.3)` |
| `source_location`, `source_quote` | `Abstract` + the sentence containing the number |
| `verification_status` | Adds `excluded: not an intervention effect` — **filter these out of effect plots** |
| `iso3` | as above; `followup_label` may be empty for observational rows (show "not reported") |

## site/data/graph.json — all graph candidates, as extracted (481 rows)

| Field | Meaning |
|---|---|
| `system_id`, `pubmed_id`, `study_id` | Graph ids |
| `system_statistic_type`, `statistic_value`, `ci_lower`, `ci_upper`, `ci_level`, `p_value`, `p_value_equality` | As stored in the snapshot |
| `variable_1_name`, `variable_2_name` | Raw variable names |
| `intervention_class`, `intervention_subtype` | e.g. `nets` / `chlorfenapyr-pyrethroid net` |
| `intervention_text`, `outcome_text` | The side naming the intervention, and the other side |
| `role` | `effect on outcome` \| `use or coverage as exposure (observational)` \| `uptake / behaviour` |
| `outcome_tier` | See above, plus `other` |
| `stat_family` | `ratio` \| `difference` \| `correlation` \| `other` |
| `plottable_ratio` | True only for positive ratios with an ordered, containing CI and value ≤ 20 |
| `direction` | `lower with intervention` / `higher with intervention` (raw, before polarity review) |
| `ci_excludes_null` | From the CI, or p < 0.05 if there is no CI |
| `qc_flags` | `;`-separated: no CI, non-positive ratio, ratio > 20, estimate outside CI, inverted exposure… |
| `title`, `journal`, `year`, `doi` | From PubMed |
| `countries`, `country_source` | Parsed from the population (`population`) or title (`title`), else `unknown` |
| `population`, `study_type` | From the System study record |
| `in_verified_set` | Paper also appears in `verified.json` |
| `iso3`, `region_notes` | ISO3 codes (`;`-joined), plus region words like Sahel |
| `match_rule` | `ours` / `teammate` / `both` |
| `teammate_flags`, `study_flags` | Teammate QC flags (e.g. `p_operator_unspecified`), study lookup flags |

## site/data/context.json

| Key | Contents |
|---|---|
| `summary` | Funnel counts (see docs/FINDINGS.md §1) |
| `malaria_neighbourhood` | Top 300 relationships of the `malaria` concept: `other_label`, `direction` (`other → anchor` = upstream factor), `num_studies`, `num_findings`, `last_published_date` |
| `intervention_neighbourhoods` | Same for `mosquito net`, `malaria vaccine`, `malaria prevention`, `indoor residual spraying` |
| `concepts` | System and Wikidata ids for those concepts |
| `anchor_coverage` | Per landmark paper: API study record, API association count, snapshot row count |
| `countries` | 11 rows from AI-2 `countries.csv`: `iso3,name,region,seasonality,showcase,in_who,in_map,in_pf8,notes` (5 core: TZA BEN BFA MLI NGA) |
| `country_year` | 721 rows, `context_country_year.csv`: WHO + MAP 2000–2025 for the 5 core countries; keep `unit` and `estimate_type` (modelled) visible |
| `pf8_sp` | 332 rows, SP resistance in sampled cases (`scope` = sampled_cases_not_prevalence); BFA has 2008 only |
| `pf8_aq_markers` | 166 rows, crt/mdr1 variant carriage (not an AQ resistance classification) |
| `who` | empty (superseded by `country_year`) |

## Working files (not loaded by the site)

| File | Purpose |
|---|---|
| `data/interim/candidates.csv` | Raw snapshot rows that matched (all columns) |
| `data/interim/candidates_classified.csv` | + classification columns |
| `data/interim/papers.json` | PubMed + System study metadata per PMID |
| `data/graph/graph_context.json` | Full API pull behind `context.json` |
| `data/review/review_queue.csv` | Prioritised review queue with abstract quotes and blank `verify_*` columns |
| `data/review/abstracts.json` | Europe PMC abstracts for priority 1–2 papers |
| `data/request_log.jsonl` | Every HTTP request (no credentials) |
