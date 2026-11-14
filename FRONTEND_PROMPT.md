# Front-end prompt — "What works where" (PATH Visualize 2)

Paste everything below the line into the front-end agent or developer.

---

You are the **front-end lead** for a hackathon team. The data layer is finished and frozen. Your job is to turn it into a clear, honest, interactive dashboard that a non-specialist judge understands in 30 seconds, and that survives a live 3-minute pitch.

**Deadlines (US Eastern, today, 14 Nov 2026)**

| Time | What must happen |
|---|---|
| **13:45** | Feature freeze |
| **14:15** | Site copied into the official fork and live on GitHub Pages |
| **14:45** | PR + Devpost submitted |
| **15:00** | Live pitch |

A complete, correct, simple site beats an ambitious broken one.

**If anything is unclear, ask the user (team lead `qianndd`) before guessing.** Questions you must ask are listed in §12.

## 1. The challenge and our angle

- **The brief (PATH):** *"How does the effect of malaria prevention vary by setting and over time?"* Compare the reported effects of **insecticide-treated nets, seasonal malaria chemoprevention (SMC) and malaria vaccines** across countries, study settings and time, using the System Public Graph (a knowledge graph of statistical findings extracted from papers) and other open data.
- **Judging** (25% each):
  1. meaningful use of the Public Graph
  2. insight / usefulness
  3. technical execution
  4. communication
- **Judges:** a clinical-informatics lead, an evidence-for-policy researcher (NYU GovLab), a World Bank data scientist, an open-scholarship infrastructure lead, and System's head of communications. None is a malaria specialist.
- **Our thesis** (use this sentence on the site): ***"Malaria prevention evidence depends on the comparison, the setting and the follow-up period."***
- **Our finding about the graph:** the graph almost always stores the right number, but often loses what the number compares. Of 33 graph findings we checked by hand, 19 needed their comparator, time point or label restored. We show every number with its comparator, setting and time window, and with its provenance.

## 2. Getting the files

- **Repo:** `https://github.com/DAzyyyyy/Hackiller_V2PATH` (private; ask the user for access).
  - Use `main` once PR #5 is merged; until then use branch `evidence-pipeline`.
  - Create your own branch `frontend` from it.
- **Read first, in this order:**
  1. `AI_HANDOFF.md` (repo root): context, shared vocabularies, science rules.
  2. `what-works-where/docs/DATA_DICTIONARY.md`: every field you can use.
  3. `what-works-where/docs/FINDINGS.md`: the numbers and stories.
  4. `what-works-where/docs/AI1_WORK_SUMMARY.md`: what exists, plus the unfinished draft HTML/CSS (§4 of that file). You may reuse or discard the draft.
- **Your working folder:** `what-works-where/site/`.
  - Data you read lives in `what-works-where/site/data/`. **Do not edit or regenerate the data.**
  - Do not run the Python pipeline; it needs API keys.
  - If you need a data change, write it under *Requests* in `COORDINATION.md` and tell the user.
- **Never touch:** `scripts/`, `data/`, `what-works-where/pipeline/`, `what-works-where/data/`, `docs/`.
- **Local preview:** `python3 -m http.server -d what-works-where/site 8000`, then open `http://localhost:8000`. The JSON must be fetched over http(s), not `file://`.

## 3. Hard constraints

1. **Deployment target: GitHub Pages on the official public fork.**
   - The site will live at `https://<user>.github.io/system-public-challenge-2026/projects/<team-name>/site/`.
   - Use **relative paths only** (`./data/verified.json`, never `/data/...`). The site must work from that sub-path and from `http.server` locally.
2. **Static only.** No server, no runtime calls to any API, no API keys anywhere. The site reads only `./data/*.json`.
3. **Every file must be under 25 MB.** The data is about 1.2 MB in total.
4. **Libraries:** load from `cdn.jsdelivr.net`, `unpkg.com` or `cdnjs` with **exact pinned versions** (e.g. `@observablehq/plot@0.6.16`, `d3@7.9.0`), or vendor them into `site/vendor/`.
5. **Stack:** your choice. Pick one in the first 10 minutes, write the choice in `COORDINATION.md`, and tell the user.

| Option | Upside | Downside |
|---|---|---|
| **A. Plain HTML + ES modules + Observable Plot/D3 from CDN** *(recommended for time)* | No build step, nothing to break, trivial deploy | You hand-write the state and the DOM |
| **B. React/Svelte + Vite** | Nicer component state | Must build to static files with `base: './'`, and you must commit the built `dist/` contents into `site/` (or `site/app/`). Pages will not run your build. Higher deploy risk |

6. **Language:** English UI. Plain words, sentence case.
7. **Must work:** desktop 1280–1920 px for the pitch projector, and a phone at 375 px with no horizontal page scroll (tables may scroll inside their own box). Light and dark mode. Keyboard focus visible.

## 4. The data (what each file contains)

All four files are JSON arrays or objects. Field types matter:
- `ci_level` is a **string** like `"0.95"`;
- `ci_excludes_null` is the **string** `"True"`/`"False"`;
- `release` in `country_year` is a float (`202608.0`);
- blank or `null` means **missing**, never zero.

### 4.1 `data/verified.json` — 20 results checked against the paper (11 also checked in full text)

The strongest layer: lead with it.

```json
{"result_id":"BJ24-CFP","trial_family_id":"benin-zou-dualAI","registration":"NCT03931473","pmid":"36706778",
 "short_ref":"Accrombessi 2023 Lancet","intervention_class":"nets","intervention":"chlorfenapyr-pyrethroid net",
 "comparator":"standard pyrethroid net","country":"Benin","iso3":"BEN","site":"Zou Department",
 "population":"children 6 mo - 10 y","outcome_tier":"clinical malaria",
 "outcome_definition":"clinical malaria case incidence (cohort)","effect_measure":"hazard ratio",
 "estimate":0.54,"ci_lower":0.42,"ci_upper":0.7,"ci_level":"0.95","p_operator":"<",
 "followup_label":"years 1-2 (0-24 months)","followup_months":24.0,"publication_year":2023,
 "origin":"graph + paper","graph_association_id":"5uTwNLWhey","graph_original_label":"chlorfenapyr-pyrethroid net",
 "verification_status":"checked against paper","verification_note":"API + CSV + paper agree…",
 "source_url":"https://pubmed.ncbi.nlm.nih.gov/36706778/",
 "fulltext_location":null,"fulltext_quoted_text":null,"fulltext_matches_our_value":null}
```

**Contents by class**
- **nets** (12 rows): Tanzania 24 and 36 mo × 3 net types; Benin years 1–2 and year 3 × chlorfenapyr and pyriproxyfen; 2 Cochrane review rows (ITN vs no net).
- **smc** (4): ACCESS-SMC case-control and population reductions for Nigeria and The Gambia; Mali 5th round.
- **vaccines** (3): R21 seasonal and standard sites; RTS,S vs SMC.
- **combination** (1): RTS,S + SMC vs SMC alone.

**Value rules**
- `estimate`/`ci_*` are on a **ratio scale where < 1 = fewer events with the intervention**.
- Rows whose `effect_measure` contains "from VE = 1 − HR" or "(as 1 − ratio)" came from a published percentage. Show the original percentage in the tooltip: percentage = (1 − estimate) × 100, with the CI bounds swapped.
  - R21 seasonal: 0.25 (0.21–0.29) = VE 75% (71–79).
- `iso3` is **empty for multi-country rows and reviews** (the Cochrane rows, ACCESS-SMC-CC). Display them as "Multi-country".

### 4.2 `data/graph_checked.json` — 33 graph findings checked against the abstract

Each row adds `graph_association_id`, `graph_original_label` (exactly what the graph stored), `graph_statistic`, `source_location` (`"Abstract"`), `source_quote` (the sentence), and `doi`.

**Status values**
- `checked against abstract`
- `comparator restored`
- `time point restored`
- `label corrected`
- `excluded: not an intervention effect`: **1 row; never plot it as an effect.** It can appear in the "what we fixed" list.

`followup_label` can be empty (6 observational rows): show "not reported".

**Highlights**
- SMC time since dose: Burkina Faso and Mali IRR 0.13; Burkina Faso 1 month 0.29, 2 months 0.33; Nigeria 0.49.
- Ghana RCT 0.62; Mali year-after 1.09; Mali routine year 1 and 2.
- LLINEUP PBO 0.80 at 25 months (Uganda).
- ITN and child mortality: Kenya, Malawi, Congo, Tanzania HDSS.
- Burkina Faso birth cohort 1.05.
- Cambodia under-5s 0.63.
- RTS,S 62.7% stored as "HR 62.7" (label corrected).

### 4.3 `data/graph.json` — all 481 graph candidates (raw, unreviewed)

- **Key fields:** `system_id`, `pubmed_id`, `title`, `year`, `doi`, `iso3`, `countries`, `intervention_class`, `intervention_subtype`, `role`, `outcome_tier`, `system_statistic_type`, `statistic_value`, `ci_lower`, `ci_upper`, `plottable_ratio`, `qc_flags`, `teammate_flags`, `variable_1_name`, `variable_2_name`, `population`, `in_verified_set`.
- **`intervention_subtype` values:**
  - `chlorfenapyr-pyrethroid net`
  - `PBO-pyrethroid net`
  - `pyriproxyfen-pyrethroid net`
  - `insecticide-treated net (standard / unspecified)`
  - `SMC (SP+AQ / IPTc)`
  - `RTS,S/AS01`
  - `R21/Matrix-M`
  - `malaria vaccine (unspecified)`
  - `RTS,S + SMC`
- **`role` values:**
  - `effect on outcome`
  - `use or coverage as exposure (observational)`
  - `uptake / behaviour` (not effect evidence: hide by default)
- **`outcome_tier`:** `vector / entomological`, `infection`, `clinical malaria`, `severe / hospital`, `anaemia & growth`, `mortality`, `other`.
- Only draw a CI mark if `plottable_ratio === true`. Otherwise show the raw value as text.
- **Always label this layer "as extracted from the graph — not yet reviewed".**

### 4.4 `data/context.json` (object)

| Key | Contents |
|---|---|
| `summary` | Headline counts: `snapshot_rows` 1,999,877; `candidate_associations` 481; `candidate_papers` 273; `effect_associations` 379; `plottable_ratio_associations` 375; `verified_results` 20; `verified_trials` 7; `graph_rows_abstract_checked` 33; `graph_rows_needing_context` 19 |
| `countries` | 11 rows: `iso3,name,region,seasonality,showcase,in_who,in_map,in_pf8,notes`. Core: TZA (`east_africa_perennial`), BEN (`west_africa_coastal`), BFA, MLI, NGA (`sahel_seasonal`). Supporting: GHA, GMB, TCD, UGA, KEN, SEN |
| `country_year` | 721 rows, 2000–2025, five core countries: `iso3,year,source(WHO/MAP),indicator,value,lower,upper,unit,estimate_type,release,flags` |
| `pf8_sp` | 332 rows: `iso3,year,drug,n_determined,n_resistant,n_sensitive,n_undetermined,resistant_share,scope`. Drugs: Sulfadoxine, Pyrimethamine, SP (uncomplicated), SP (IPTp). **Sampled cases, not prevalence. BFA has 2008 only** |
| `pf8_aq_markers` | 166 rows: crt K76T / mdr1 N86Y variant carriage share. **Not an amodiaquine-resistance classification** |
| `malaria_neighbourhood` | 300 relationships of the graph concept `malaria`: `other_label`, `direction` (`"other → anchor"` = upstream factor, `"anchor → other"` = downstream), `num_studies` |
| `intervention_neighbourhoods` | Same for `mosquito net`, `malaria vaccine` |
| `anchor_coverage` | 9 landmark papers: `api_study`, `api_associations`, `csv_associations`. Shows that several trials exist in the graph with zero extracted findings |

**`country_year` indicators and units** — keep them as given:

| Source | Indicator | Unit |
|---|---|---|
| MAP | `ITN_use-rate` | proportion |
| MAP | `Pf_PR-rate` | proportion, children 2–10 |
| MAP | `Pf_incidence-rate` | per 1,000 per year |
| WHO | `MALARIA_ITN_USE` | percent |
| WHO | `MALARIA_ITN_COVERAGE` | percent |
| WHO | `MALARIA_EST_INCIDENCE` | per 1,000 at risk |
| WHO | `MALARIA_IRS_COVERAGE` | **people, not percent** |

All are `estimate_type: modelled`, except WHO IRS, which is `reported_programme`.

## 5. Science display rules (non-negotiable)

1. **No pooling, no ranking, no "best intervention".** Never compute an average effect across studies.
2. **Separate panels** for different outcomes and different effect measures. Tanzania (infection, OR) and Benin (clinical cases, HR) sit **side by side, never in one combined estimate**. Mosquito outcomes are never on the same axis as human outcomes.
3. **Every effect mark shows**:
   - the effect-measure badge (OR, aOR, HR, IRR, RR, PR)
   - the comparator ("vs standard pyrethroid net", "vs SMC alone", …)
   - the time window
   - the setting (country or site)
4. **Ratio axes are logarithmic**, with a reference line at 1 labelled "no difference". Left of 1 = "fewer [events] with the intervention".
5. **Wording.**
   - A CI crossing 1 = "not shown to differ" or "uncertain", **never "no effect" or "doesn't work"**.
   - Never claim one country differs from another because one result is significant and the other isn't.
6. **Three evidence layers, always visually distinct**:
   - checked against paper / full text (`verified`)
   - checked against abstract (`graph_checked`)
   - as extracted, unreviewed (`graph`)
   Use a status icon + text label, never colour alone.
7. **Context data** (WHO, MAP, Pf8) is labelled "modelled national estimate" or "sampled cases". It is background, never presented as the cause of a trial result. Show units.
8. **Provenance on demand:** every effect mark opens its source (see §6, M6).

## 6. What to build

### Must-have modules (M1–M8)

**M1 — Header + thesis + evidence funnel**
- Title and the thesis sentence.
- A funnel from `context.summary`, shown as small numbers with units:

  1,999,877 graph findings scanned → 481 about nets, SMC or vaccines (273 papers) → 33 checked against the abstract (19 needed context restored) → 20 checked against the paper (7 trials).

**M2 — "The same nets, two countries, three years"**
- Forest plot from `verified.json`, `intervention_class === "nets"`, trial families `tanzania-misungwi-dualAI` and `benin-zou-dualAI`.
- **Facet by trial** (Tanzania: infection aOR/OR; Benin: clinical HR).
- Rows = net type × follow-up (24/36 mo; years 1–2 / year 3).
- **Colour by net type** (validated palette below) **plus a direct text label**.
- Status icon per row. Hover shows the full row; click opens the source drawer.
- Takeaway text: "The chlorfenapyr net cut infection and clinical cases in both trials in the first two years. By year 3 in Benin the interval crosses 1."
- Optionally add the Cochrane ITN-vs-no-net rows as a reference ("older trials, standard nets vs no net"). Use a separate group with a diamond marker, and label it as a systematic review.

**M3 — "Same intervention, different question"**
- SMC and vaccines from `verified.json` + `graph_checked.json`, grouped by question, each group with a one-line explainer:
  - *Time since an SMC dose*:
    - Burkina Faso/Mali IRR 0.13 (≤28 d vs >35 d)
    - Burkina Faso OR 0.29 (1 mo) → 0.33 (2 mo)
    - Nigeria 0.49 (1 mo, uncertain)
    - Mali year after stopping 1.09
  - *Individual vs population effect (ACCESS-SMC)*:
    - 28-day protective effectiveness 88.2% vs population outpatient reduction Nigeria 25.5% / The Gambia 55.2%
    - Show as percentages here: the story is "88% or 26%? Both are true".
  - *Vaccine by transmission setting*: R21 seasonal (BFA, MLI) VE 75% vs standard (BFA, KEN, TZA) VE 68%.
  - *Combination*: RTS,S + SMC vs SMC alone 62.8%; RTS,S alone vs SMC HR 0.92 (non-inferior; the comparator is SMC, not placebo).

**M4 — Settings: three transmission zones, five countries**
- Group the 5 core countries by `region` (east Africa perennial / west Africa coastal / Sahel seasonal).
- Each country card shows:
  - the number of checked results (`verified` + non-excluded `graph_checked` whose `iso3` contains it);
  - small multiples from `country_year`: MAP `ITN_use-rate` and `Pf_PR-rate` over 2000–2025, with uncertainty band, clearly "modelled";
  - Pf8 SP note for Sahel countries, "sampled cases".
- Clicking a country filters M2/M3/M5 to that country.
- Supporting countries are listed below as chips.
- A map is optional (see §6 nice-to-haves). If you draw one, do not shade countries by "effectiveness".

**M5 — Evidence index (the graph layer)**
- Matrix: rows = `intervention_subtype`, columns = `outcome_tier`.
- Cell = **number of distinct papers** (`pubmed_id`), not rows. Circle area ∝ papers. Empty cells are hatched with the label "no findings in the graph".
- Filters in one row above the matrix:
  - intervention class
  - country (ISO3 → name)
  - role (default: effect + observational; uptake hidden)
  - "only rows with a usable CI"
- Clicking a cell shows a table:
  - year, country, raw intervention text → raw outcome text, measure, value (CI);
  - an inline mini CI bar on a log axis if `plottable_ratio`;
  - flags; a status chip ("unreviewed", or "checked" if `system_id` appears as a `graph_association_id` in `graph_checked`/`verified`);
  - a "source" button.

**M6 — Source drawer** (shared by all modules)

| Layer | What the drawer shows |
|---|---|
| verified rows | Short ref, intervention vs comparator, population, site/country, outcome definition, measure + estimate (CI), follow-up, publication year, registration. **What the graph had** (`graph_original_label`, `graph_api_status`, `graph_csv_status`) vs what we verified (`verification_status`, `verification_note`). Full-text check (`fulltext_location`, `fulltext_quoted_text`, `fulltext_matches_our_value`). Links: PubMed (`source_url`) |
| graph_checked rows | Same, plus `graph_statistic` and the **abstract quote** (`source_quote`), and a DOI link |
| graph rows | Title, journal, year, DOI, PubMed link, population, raw variable names, statistic, flags, and "Not yet reviewed against the paper" |

**M7 — "How the graph sees malaria"** (shows meaningful use of the Graph)
- Horizontal bars: top ~20 **upstream** factors (`direction === "other → anchor"`) of `malaria` by `num_studies`.
- Colour 3 categories with a legend + labels:
  - **interventions** (bednet, mosquito net, insecticide, antimalarial…)
  - **climate & environment** (rain, temperature, humidity, forest…)
  - **people & place** (age, gender, education, rural…)
  - everything else in muted grey
- Takeaway: "Bed nets are the most-studied intervention linked to malaria in the graph; rain and temperature are close behind. SMC has no concept of its own in the graph."
- Below: the `anchor_coverage` table (paper | in API | API findings | in filtered snapshot), with the caption "Several landmark trials are in the graph with no extracted findings; we filled them from the papers".

**M7b — "What we fixed"**
- A list (or small table) of `graph_checked` + `verified` rows whose status is `label corrected`, `comparator restored`, `time point restored` or `excluded…`.
- Show: graph's original label → corrected meaning → reason.
- This is our strongest "technical execution + graph use" proof. Example: "Graph: RTS,S → clinical malaria, hazard_ratio 62.7. Paper: vaccine efficacy 62.7%, i.e. HR 0.37."

**M8 — Method, limits, credits** (short)
- **Method (4 steps):** find in the graph → describe (PubMed, offline study table) → check (abstract, paper, full text) → show without pooling.
- **Limits:**
  - open-access papers only;
  - keyword discovery can miss studies;
  - the graph layer is unreviewed;
  - context data is modelled or sampled.
- **Credits:**
  - System Public Graph (CC BY-NC 4.0), WHO GHO, Malaria Atlas Project, MalariaGEN Pf8 (CC BY 4.0), PubMed / Europe PMC.
  - Code MIT.
  - "Built with AI coding tools (Claude Code, OpenAI Codex)."

### Nice-to-have (only after M1–M8 work)

- **Story presets:** 3–4 buttons that set filters and scroll, with state in the URL hash (e.g. `#story=nets-over-time`). These drive the live pitch.
- "Download filtered rows as CSV" in M5.
- A simple Africa map of the 5 core + 6 supporting countries, coloured by **region** (categorical), never by effect.
- A print/screenshot mode for the slides.

## 7. First screen and pitch path — your decision

The team lead wants **you** to choose the opening view. Decide in the first 15 minutes, tell the user, and design the page order around it. Options:

| Option | Strength | Risk |
|---|---|---|
| **a. Nets over time (M2 first)** | Answers "over time" and "setting" instantly with the strongest verified data | Starts with a chart; needs a crisp title |
| **b. Settings overview (M4 first)** | Answers "where"; the three zones are memorable | Effects only appear one click later |
| **c. "The number survives, the comparison doesn't" (M1 funnel + M7b first)** | Strongest graph-use story for System's judges | Can sound like criticism of the graph. Frame it as "we restore context", not "the graph is wrong" |

Whichever you choose, the 3-minute pitch needs a path:

| Time | Beat |
|---|---|
| 0:00 | Hook: "88% or 26%? Both are true" (ACCESS-SMC) |
| 0:20 | The problem |
| 0:40 | Live demo: 3 clicks (M2 → M3 → drawer) |
| 1:50 | How the graph made it possible (M7, M7b) |
| 2:20 | Integrity rules |
| 2:40 | What PATH can do with it |

Design the site so these clicks are obvious.

## 8. Visual design system

Make it look intentional and specific to the subject, not a generic SaaS template:
- avoid identical rounded cards everywhere, decorative gradients, and an all-caps eyebrow over every heading;
- one memorable element (e.g. the funnel or the M2 chart), everything else quiet;
- left-aligned text, line length under about 75 characters.

**Typography**
- `system-ui, -apple-system, "Segoe UI", sans-serif` throughout.
- Tabular numerals (`font-variant-numeric: tabular-nums`) for every number.
- Type scale: about 48/28/20/16/14/12 px.

**Colour tokens** (validated with a colour-blindness checker; define them as CSS variables on `:root`)

| Role | Light | Dark |
|---|---|---|
| page | `#f9f9f7` | `#0d0d0d` |
| surface | `#fcfcfb` | `#1a1a19` |
| ink | `#0b0b0b` | `#f0efec` |
| ink-2 | `#52514e` | `#c3c2b7` |
| muted | `#898781` | `#898781` |
| grid | `#e1e0d9` | `#2c2c2a` |
| axis | `#c3c2b7` | `#383835` |
| series 1: chlorfenapyr net, or "interventions" in M7 | `#2a78d6` | `#3987e5` |
| series 2: PBO net, or "people & place" | `#eb6834` | `#d95926` |
| series 3: pyriproxyfen net, or "climate & environment" | `#1baf7a` | `#199e70` |
| standard net / other | `#6f6e69` | `#a3a29b` |
| sequential (matrix circles), light → dark | `#cde2fb`, `#86b6ef`, `#2a78d6`, `#184f95` | same, reversed for dark |

- **Colour rules**
  - Series 3 aqua is below 3:1 contrast on light, so **always add a direct text label** next to aqua marks.
  - Status colours are used only with icon + text: good `#0ca30c` (✓ checked), serious `#ec835a` (✎ corrected or restored), muted grey (from paper only), critical `#d03b3b` (flag).
  - Dark mode: add `@media (prefers-color-scheme: dark)` plus `:root[data-theme="dark"]` overrides. A theme toggle is optional.
- **Marks**
  - CI line 2 px; point marker ≥ 8 px.
  - Square marker for trials, diamond for systematic reviews, hollow marker for "CI crosses 1" (it is still shown).
  - Recessive grid; reference line at 1 dashed.
  - No dual axes. Use small multiples instead.
- **Interaction**
  - Hover tooltip on every mark: what, vs what, where, when, measure, value (CI), status.
  - Click opens the drawer.
  - Hit targets ≥ 24 px. Filters in one row above the chart.
  - Respect `prefers-reduced-motion`.
- **Accessibility**
  - Identity is never colour-only (labels or a legend).
  - Every chart has a table equivalent (the M5 table; M2 rows are table rows).
  - Visible focus, aria-labels on icon buttons.

## 9. Copy (exact phrases to reuse)

- **Thesis:** "Malaria prevention evidence depends on the comparison, the setting and the follow-up period."
- **Axis:** "← fewer [infections | cases | deaths] with the intervention" … "no difference" … "more →".
- **Layer labels:**
  - "Checked against the paper"
  - "Checked against the abstract"
  - "As extracted from the graph — not yet reviewed"
- **CI crossing 1:** "Uncertain: the interval includes no difference."
- **Context:** "Modelled national estimate (WHO / MAP). Background, not a cause of any trial result."
- **Pf8:** "Share of sampled parasites with SP-resistance markers. Not national prevalence, not SMC efficacy."
- **Empty cell:** "No findings in the graph for this combination."
- **Avoid** "effective", "ineffective", "works", "proven", "best". Say what was measured.

## 10. Acceptance checklist (run before 13:45)

- [ ] Spot-check these numbers on screen against the JSON:
  - Tanzania 24 mo chlorfenapyr 0.45 (0.30–0.67)
  - Benin years 1–2 chlorfenapyr HR 0.54 (0.42–0.70)
  - Benin year 3 chlorfenapyr 0.80 (0.56–1.17)
  - R21 seasonal VE 75% / standard 68%, with sites BFA;MLI and BFA;KEN;TZA
  - ACCESS-SMC 88.2% with comparator "no SMC in the previous 42 days"
  - SMC IRR 0.13
  - LLINEUP 0.80 at 25 mo
- [ ] The excluded row never appears as an effect.
- [ ] Multi-country rows show "Multi-country", not blank.
- [ ] No pooled or averaged effect anywhere; each panel has a single outcome type + measure.
- [ ] The funnel numbers equal `context.summary`.
- [ ] Every mark has a tooltip; every effect opens a drawer with a working PubMed/DOI link.
- [ ] Works at 375 px and 1440 px; light and dark; keyboard tab order is sensible.
- [ ] Relative paths only. It works when served from a sub-folder: run `python3 -m http.server` one level up and open `/site/`.
- [ ] No console errors.
- [ ] Optional: a Playwright script that loads the page, waits for `networkidle`, takes 375 px and 1440 px screenshots, and checks there are no console errors.

## 11. Git and handoff

- Work on branch `frontend`. Commit with prefix `[FE]`. Push often. Never force-push. Never commit secrets.
- Edit only `what-works-where/site/` (except `site/data/`), plus your own row in `COORDINATION.md` (add a row "FE").
- At **13:45**: open a PR `frontend` → `main`, and tell the user the local preview command plus 2 screenshots.
- At **14:15** the user (or AI-1) copies `what-works-where/` into the official fork under `projects/<team-name>/`. Your site must work there unchanged.
- Fill the screenshot section of `what-works-where/README.md` only if asked.

## 12. Ask the user before deciding

1. **Team name.** It is needed for the fork folder and the site title/footer.
2. **Stack** (§3): confirm A or B after your first 10 minutes.
3. **Opening view** (§7): confirm your choice.
4. Do they want team member names on the site?
5. May you use a map library (Leaflet/topojson from CDN)? Default: no map, or a simple static SVG.
6. Anything in the data that looks wrong: ask, don't fix.
