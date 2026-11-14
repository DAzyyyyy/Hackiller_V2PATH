# Coordination board

Each agent edits **only its own row** and its own lines under *Requests* and *Log*. Read `AI_HANDOFF.md` first.

## Status

| Agent | Branch | Current task | Status | Last commit | Blockers | Updated (ET) |
|---|---|---|---|---|---|---|
| AI-1 Evidence & Integration (Claude Code) | `evidence-pipeline` | A1–A5, C2, I1 | starting | — | — | 11:30 |
| AI-2 Context & Full text | `context-data` | B1–B5, C1, optional B6 | done: contracts and validation passed; ready for integration | dd3b6b6 | 3 evidence-context corrections for AI-1 | 11:39 |

## Checkpoints (ET)

- [ ] 12:00: contract files exist (even partial), pushed
- [ ] 12:30: A–C done, pushed
- [ ] 12:35: AI-1 merges `context-data` → `evidence-pipeline`, rebuilds site data
- [ ] 12:45: front end starts (AI-1); AI-2 does QA and pitch-number checks
- [ ] 13:45: feature freeze
- [ ] 14:15: copy to the official fork `projects/<team-name>/` (team name: _TBD_)
- [ ] 14:45: PR opened and Devpost link submitted

## Requests

Format: `- [from → to] what you need, and which file/field (time)`

- [AI-2 → AI-1] C1: R21-SEAS has matching numerical HR/CI, but countries must be BFA;MLI (Nanoro and Bougouni), not all four trial countries. R21-STD must be BFA;KEN;TZA (Dande, Kilifi, Bagamoyo). Preserve adjusted VE source and 12-month first-episode outcome; Table 2 and Methods confirmed. Fulltext checks mark N because context needs correction, not because numbers differ. (11:38)
- [AI-2 → AI-1] C1: ACCESS-SMC-CC numerical conversion matches, but Figure 2A's comparator is no SMC within last 42 days. The 28 days describes the protection window, not the untreated comparator window. The case-control component covers five countries within the seven-country programme; please restore this context in your evidence table/site JSON. (11:38)
- [AI-2 → AI-1] B1–B6 ready: integrate only data/context/* and data/verified/fulltext_checks.csv into site data. BFA Pf8 has 2008 only; do not imply contemporaneous resistance for later trials. Optional crt/mdr1 files describe variant carriage, not AQ resistance classification. (11:38)

## Log

Format: `- HH:MM [AI-x] what changed (commit)`

- 11:30 [AI-1] Created AI_HANDOFF.md and COORDINATION.md; created branch `context-data` for AI-2.
- 11:38 [AI-2] Added 27 MAP + 4 WHO unchanged raw responses and hashes. Exports: countries 11; context_country_year 721 (WHO 331, MAP 390); pf8_sp_country_year 332; fulltext_checks 11 (all numerical matches, 3 context corrections); optional pf8_aq_markers_country_year 166. Pipeline and contract validation passed. PMC8457484 identified as PMID 34495978, DOI 10.1371/journal.pmed.1003727, "Effectiveness of seasonal malaria chemoprevention (SMC) treatments when SMC is implemented at scale: Case-control studies in 5 countries". No 27875528/34894221 rows were present in the supplied evidence_graph_checked table. Evidence and site files untouched.
