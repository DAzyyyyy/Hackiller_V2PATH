# AI-1 work summary (Evidence & Integration)

What AI-1 (Claude Code) built, where it lives, and the unfinished front-end draft. State as of 11:55 ET on branch `evidence-pipeline` (PR #5 → `main`).

## 1. What exists

| Path | What | Status |
|---|---|---|
| `pipeline/00_download_snapshot.py` | Dataverse snapshot download with SHA-256 check (fallback only) | done |
| `pipeline/01_extract_candidates.py` | Scans 1,999,877 associations offline from the restored tables. Candidate = our rule ∪ teammate rule → **481 rows / 273 papers** (includes all 331 teammate ids) | done |
| `pipeline/02_classify.py` | Intervention subtype, outcome tier, role, statistic family, our QC flags + teammate QC flags | done |
| `pipeline/03_enrich.py` | PubMed title/journal/year/DOI; population + study type from the offline `studies` table; country → ISO3 | done |
| `pipeline/04_graph_context.py` | System API: `malaria` concept neighbourhood; 3-layer coverage of the landmark trials | done |
| `pipeline/05_build_site_data.py` | Writes `site/data/*.json`; merges AI-2 context + full-text checks | done |
| `pipeline/06_review_queue.py` | Single merged review queue: `data/review/review_queue.csv`, 481 rows | done |
| `pipeline/07_abstract_check.py` | Europe PMC abstracts: is the number in the abstract, plus a quote (151 of 185 priority rows found) | done |
| `pipeline/08_graph_checked.py` | Hand-reviewed graph rows → `data/verified/evidence_graph_checked.csv` (**33 rows; 19 needed context restored**) | done |
| `pipeline/validate.py` | Assertions: vocabulary, ISO3, ratio rules, contracts, key scan | passing |
| `data/verified/evidence_verified.csv` | **20 paper-verified results from 7 trials**; 11 also confirmed in full text by AI-2; 3 context corrections applied | done |
| `site/data/{verified,graph_checked,graph,context}.json` | Front-end inputs, ~1.2 MB in total | **frozen for the front end** |
| `docs/FINDINGS.md` | All numbers, failure catalogue, pitch lines | done |
| `docs/DATA_DICTIONARY.md` | Every field the front end can read | done |
| `site/index.html`, `site/styles.css` | Front-end draft, no JS yet | **unfinished — see §4** |

**Rebuild** (needs `what-works-where/.env` with `SYSTEM_API_KEY`):
1. From the repo root: `python3 scripts/restore_system.py`
2. Then: `bash what-works-where/pipeline/run_all.sh`

**The front end never needs to run this.**

## 2. Key decisions

1. **Evidence map, not ranking.** Each number keeps its own effect measure and comparator. No pooling, no voting by significance.
2. **The graph supplies numbers; we restore what they compare.** 19 of the 33 hand-checked graph rows needed a comparator, time point or label restored.
3. **Two checked layers and one raw layer**, kept visually distinct in the UI:
   - `verified` — checked against the paper or full text
   - `graph_checked` — checked against the abstract
   - `graph` — as extracted, unreviewed
4. **Settings = 3 zones / 5 core countries:**
   - `east_africa_perennial`: TZA
   - `west_africa_coastal`: BEN
   - `sahel_seasonal`: BFA, MLI, NGA
   - Supporting: GHA, GMB, TCD, UGA, KEN, SEN
5. **Time = follow-up since deployment or dose**, never publication year.
6. **Context is background, not cause.**
   - WHO and MAP figures are modelled estimates.
   - Pf8 counts sampled cases only. It covers the SP side only (no AQ classification), and has Burkina Faso data for 2008 only.

## 3. Headline numbers (all checked)

**Nets** (vs standard pyrethroid net)

| Trial | Outcome / measure | Chlorfenapyr net | PBO net | Pyriproxyfen net |
|---|---|---|---|---|
| Tanzania, 24 mo | Infection, aOR | 0.45 (0.30–0.67) | 0.99 | 0.79 |
| Tanzania, 36 mo | Infection, OR | 0.57 (0.38–0.86) | — | — |
| Benin, years 1–2 | Clinical, HR | 0.54 (0.42–0.70) | — | 0.86 |
| Benin, year 3 | Clinical, HR | 0.80 (0.56–1.17) | — | 1.02 |

- **PBO in Uganda (LLINEUP):** prevalence ratio 0.80 (0.69–0.93) at 25 months.

**SMC**
- Dose ≤28 days ago vs >35 days ago: hospitalisation or death IRR 0.13 (0.08–0.20).
- Infection OR in Burkina Faso: 0.29 at 1 month, 0.33 at 2 months. Nigeria at 1 month: 0.49 (0.23–1.05).
- ACCESS-SMC protective effectiveness: 88.2% (comparator: no SMC in the previous 42 days). Population-level reduction: Nigeria 25.5%, The Gambia 55.2%.
- No rebound in the year after IPTc stopped (IRR 1.09).

**Vaccines**
- R21: HR 0.25 at seasonal sites (BFA, MLI) vs 0.32 at standard sites (BFA, KEN, TZA).
- RTS,S + SMC vs SMC alone: protective efficacy 62.8%.
- RTS,S alone vs SMC alone: HR 0.92 (non-inferior).

**Nets and child mortality**
- ITN effect on child mortality: Kenya cluster RCT infants HR 0.78; Malawi 0.75; Congo 0.76.
- Burkina Faso birth cohort: nets from birth vs from 6 months, rate ratio 1.05 after 8.3 years (no rebound).

**Graph neighbourhood of malaria**
- Most-studied links: insecticide-treated bednet 63 studies, rain 24, temperature 23.
- The graph has no SMC concept.

## 4. Unfinished front-end draft (verbatim)

- **Status:** HTML skeleton and CSS only; **no `app.js`**.
- **Sections:**
  1. masthead + funnel
  2. "same nets over time"
  3. "same intervention, different question"
  4. evidence index
  5. "how the graph sees malaria"
  6. method
- **Palette:** validated with the dataviz colour checker in light and dark modes.
  - Chlorfenapyr `#2a78d6`, PBO `#eb6834`, pyriproxyfen `#1baf7a`.
  - The aqua is below 3:1 contrast on the light background, so direct text labels are required.
- The front-end team may reuse or discard this draft.

### 4.1 `site/index.html`

```html
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>What Works Where</title>
<meta name="description" content="How malaria prevention effects vary by setting and over time — evidence from the System Public Graph, checked against the original trials.">
<link rel="stylesheet" href="styles.css">
</head>
<body>
<header class="masthead">
  <div class="wrap">
    <h1>What works where</h1>
    <p class="lede">Malaria prevention evidence depends on the comparison, the setting and the follow-up period. This dashboard compares bed nets, seasonal malaria chemoprevention (SMC) and malaria vaccines using findings extracted by the <a href="https://www.system.com/public">System Public Graph</a>, each checked against the original paper.</p>
    <div id="funnel" class="funnel" aria-label="How the evidence set was built"></div>
  </div>
</header>

<nav class="tabs wrap" aria-label="Sections">
  <a href="#time">Over time</a>
  <a href="#setting">By setting and question</a>
  <a href="#index">Evidence index</a>
  <a href="#graph">How the graph sees malaria</a>
  <a href="#method">Method</a>
</nav>

<main class="wrap">

<section id="time" class="panel">
  <h2>The same nets, two countries, three years</h2>
  <p class="intro">Two cluster-randomised trials compared three newer nets with a standard pyrethroid net. Each row is one comparison at one follow-up. Points left of the line mean fewer infections or cases with the newer net. Tanzania measured infection in surveys; Benin counted clinical cases, so the two are shown side by side, not pooled.</p>
  <div class="legend" id="net-legend"></div>
  <div class="facets" id="forest-nets"></div>
  <p class="takeaway" id="net-takeaway"></p>
</section>

<section id="setting" class="panel">
  <h2>Same intervention, different question</h2>
  <p class="intro">A single “effectiveness” number hides what was compared, for whom and over what window. These results come from the same intervention families but answer different questions.</p>
  <div id="forest-questions"></div>
</section>

<section id="index" class="panel">
  <h2>Evidence index: what the graph holds</h2>
  <p class="intro">Every association in the fixed Dataverse snapshot of the System Public Graph that names a net, SMC or a malaria vaccine inside a malaria paper. These rows are <strong>as extracted</strong> and not yet reviewed; open a row to see its source. Circle area shows the number of papers.</p>
  <div class="filters" id="filters"></div>
  <div id="matrix" class="matrix" role="grid" aria-label="Papers by intervention and outcome"></div>
  <div id="cell-detail"></div>
</section>

<section id="graph" class="panel">
  <h2>How the graph sees malaria</h2>
  <p class="intro">Concepts the System Public Graph links directly to <em>malaria</em> as an upstream factor, ranked by number of supporting studies. Bed nets lead the interventions, and climate and environment (rain, temperature, humidity, forest) are among the most-studied settings that shape transmission.</p>
  <div class="legend" id="nb-legend"></div>
  <div id="neighbours" class="bars"></div>
  <h3>Where the landmark trials sit in the graph</h3>
  <p class="intro">The three layers that this dashboard draws on. The Beta API has a study record for every trial; some have no extracted findings, and the filtered snapshot keeps only one of these rows.</p>
  <div id="coverage"></div>
  <h3>Country context (WHO, modelled)</h3>
  <p class="intro">Share of the population sleeping under an insecticide-treated net. Modelled national estimates, a different scale from a village trial: context, not a cause of any trial result.</p>
  <div id="who" class="small-multiples"></div>
</section>

<section id="method" class="panel method">
  <h2>Method and limits</h2>
  <ol>
    <li><strong>Find.</strong> Scanned all 1,999,877 associations in the System Public Graph snapshot (Harvard Dataverse v2.1, CC BY-NC 4.0). Kept rows naming a net, SMC or malaria vaccine in a paper that mentions malaria, Plasmodium or Anopheles.</li>
    <li><strong>Describe.</strong> Added title, journal, year and DOI from PubMed and the study population from the System API. Country comes from the study population or title, never from author affiliations.</li>
    <li><strong>Check.</strong> For the trials shown in the first two sections, every number was compared with the paper. We record the graph’s original label, the corrected label and why it changed.</li>
    <li><strong>Show, don’t pool.</strong> Results are shown with their own effect measure (OR, HR, IRR, rate ratio) and comparator. Different outcomes and measures sit in separate panels. We do not compute pooled effects or vote by statistical significance.</li>
  </ol>
  <p><strong>Limits.</strong> The graph covers open-access papers only. Keyword discovery can miss studies. Rows in the evidence index are unreviewed extractions. A significant result in one country and a non-significant one in another is not evidence that the countries differ.</p>
  <p class="fine">Data: System Public Graph (System, Inc.), CC BY-NC 4.0 · WHO Global Health Observatory · PubMed. Code: MIT.</p>
</section>
</main>

<aside id="drawer" class="drawer" aria-hidden="true" aria-label="Source details">
  <button class="drawer-close" type="button" aria-label="Close source details">Close</button>
  <div id="drawer-body"></div>
</aside>
<div id="tooltip" class="tooltip" role="tooltip" hidden></div>

<script type="module" src="app.js"></script>
</body>
</html>

```

### 4.2 `site/styles.css`

```css
:root {
  color-scheme: light;
  --page: #f9f9f7;
  --surface: #fcfcfb;
  --ink: #0b0b0b;
  --ink-2: #52514e;
  --muted: #898781;
  --grid: #e1e0d9;
  --axis: #c3c2b7;
  --ring: rgba(11, 11, 11, 0.10);
  --accent: #1c5cab;
  --s1: #2a78d6;   /* chlorfenapyr-pyrethroid */
  --s2: #eb6834;   /* PBO-pyrethroid */
  --s3: #1baf7a;   /* pyriproxyfen-pyrethroid */
  --neutral-mark: #6f6e69;
  --good: #0ca30c;
  --warning: #fab219;
  --serious: #ec835a;
  --critical: #d03b3b;
  --seq-1: #cde2fb;
  --seq-2: #86b6ef;
  --seq-3: #2a78d6;
  --seq-4: #184f95;
}
@media (prefers-color-scheme: dark) {
  :root:not([data-theme="light"]) {
    color-scheme: dark;
    --page: #0d0d0d;
    --surface: #1a1a19;
    --ink: #f0efec;
    --ink-2: #c3c2b7;
    --muted: #898781;
    --grid: #2c2c2a;
    --axis: #383835;
    --ring: rgba(255, 255, 255, 0.10);
    --accent: #86b6ef;
    --s1: #3987e5;
    --s2: #d95926;
    --s3: #199e70;
    --neutral-mark: #a3a29b;
    --seq-1: #184f95;
    --seq-2: #256abf;
    --seq-3: #5598e7;
    --seq-4: #9ec5f4;
  }
}
:root[data-theme="dark"] {
  color-scheme: dark;
  --page: #0d0d0d;
  --surface: #1a1a19;
  --ink: #f0efec;
  --ink-2: #c3c2b7;
  --muted: #898781;
  --grid: #2c2c2a;
  --axis: #383835;
  --ring: rgba(255, 255, 255, 0.10);
  --accent: #86b6ef;
  --s1: #3987e5;
  --s2: #d95926;
  --s3: #199e70;
  --neutral-mark: #a3a29b;
  --seq-1: #184f95;
  --seq-2: #256abf;
  --seq-3: #5598e7;
  --seq-4: #9ec5f4;
}

* { box-sizing: border-box; }
html { scroll-behavior: smooth; }
body {
  margin: 0;
  background: var(--page);
  color: var(--ink);
  font: 16px/1.55 system-ui, -apple-system, "Segoe UI", sans-serif;
}
a { color: var(--accent); }
.wrap { max-width: 1120px; margin: 0 auto; padding: 0 16px; }

.masthead { padding: 40px 0 24px; }
.masthead h1 { font-size: clamp(2rem, 5vw, 3.2rem); line-height: 1.05; margin: 0 0 12px; letter-spacing: -0.02em; }
.lede { max-width: 68ch; font-size: 1.1rem; color: var(--ink-2); margin: 0 0 24px; }

.funnel { display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap: 2px; background: var(--ring); border-radius: 8px; overflow: hidden; }
.funnel .step { background: var(--surface); padding: 14px 16px; }
.funnel .num { font-size: 1.6rem; font-weight: 650; font-variant-numeric: tabular-nums; }
.funnel .lab { color: var(--ink-2); font-size: 0.88rem; }
@media (max-width: 720px) { .funnel { grid-template-columns: repeat(2, minmax(0, 1fr)); } }

.tabs { display: flex; gap: 20px; flex-wrap: wrap; padding-top: 8px; padding-bottom: 8px; position: sticky; top: 0; background: var(--page); z-index: 5; border-bottom: 1px solid var(--grid); }
.tabs a { color: var(--ink-2); text-decoration: none; font-size: 0.95rem; padding: 4px 0; }
.tabs a:hover, .tabs a:focus-visible { color: var(--ink); text-decoration: underline; }

.panel { padding: 40px 0 16px; border-bottom: 1px solid var(--grid); }
.panel h2 { font-size: 1.5rem; margin: 0 0 8px; }
.panel h3 { font-size: 1.1rem; margin: 32px 0 6px; }
.intro { max-width: 72ch; color: var(--ink-2); margin: 0 0 16px; }
.takeaway { max-width: 72ch; margin: 16px 0 0; padding-left: 12px; border-left: 3px solid var(--accent); }
.fine { color: var(--muted); font-size: 0.85rem; }

.legend { display: flex; flex-wrap: wrap; gap: 16px; margin: 0 0 12px; font-size: 0.9rem; color: var(--ink-2); }
.legend .key { display: inline-flex; align-items: center; gap: 6px; }
.legend .sw { width: 12px; height: 12px; border-radius: 50%; display: inline-block; }
.legend .sw.diamond { border-radius: 2px; transform: rotate(45deg); width: 10px; height: 10px; }

/* forest tables */
.facets { display: grid; grid-template-columns: repeat(auto-fit, minmax(420px, 1fr)); gap: 24px; }
@media (max-width: 520px) { .facets { grid-template-columns: 1fr; } }
.facet { background: var(--surface); border: 1px solid var(--ring); border-radius: 8px; padding: 16px; min-width: 0; }
.facet h3 { margin: 0 0 2px; font-size: 1.05rem; }
.facet .sub { color: var(--ink-2); font-size: 0.86rem; margin: 0 0 10px; }
.forest { width: 100%; border-collapse: collapse; font-size: 0.88rem; }
.forest th { font-weight: 500; color: var(--muted); text-align: left; padding: 2px 6px; font-size: 0.78rem; }
.forest td { padding: 2px 6px; vertical-align: middle; }
.forest tr.group td { padding-top: 12px; color: var(--ink-2); font-weight: 600; font-size: 0.84rem; }
.forest tr.row { cursor: pointer; }
.forest tr.row:hover td, .forest tr.row:focus-visible td { background: color-mix(in srgb, var(--accent) 8%, transparent); }
.forest tr.row:focus-visible { outline: 2px solid var(--accent); outline-offset: -2px; }
.forest td.plot { width: 46%; min-width: 160px; padding: 0; }
.forest td.plot svg { display: block; width: 100%; height: 26px; overflow: visible; }
.forest td.est { white-space: nowrap; font-variant-numeric: tabular-nums; color: var(--ink); }
.forest td.lab { min-width: 0; }
.forest .axis-row svg { display: block; width: 100%; height: 30px; overflow: visible; }
.status { display: inline-flex; align-items: center; gap: 4px; font-size: 0.76rem; color: var(--ink-2); white-space: nowrap; }
.status .ic { font-weight: 700; }
.status.ok .ic { color: var(--good); }
.status.fix .ic { color: var(--serious); }
.status.paper .ic { color: var(--muted); }
.status.flag .ic { color: var(--critical); }

/* matrix */
.filters { display: flex; flex-wrap: wrap; gap: 12px 20px; align-items: end; margin-bottom: 16px; }
.filters label { display: flex; flex-direction: column; font-size: 0.8rem; color: var(--ink-2); gap: 4px; }
.filters label.check { flex-direction: row; align-items: center; gap: 6px; font-size: 0.88rem; }
.filters select { font: inherit; font-size: 0.9rem; padding: 4px 8px; border-radius: 6px; border: 1px solid var(--axis); background: var(--surface); color: var(--ink); }
.matrix { overflow-x: auto; background: var(--surface); border: 1px solid var(--ring); border-radius: 8px; }
.matrix table { border-collapse: collapse; width: 100%; min-width: 640px; }
.matrix th { font-weight: 500; font-size: 0.8rem; color: var(--ink-2); padding: 8px; text-align: center; }
.matrix th.rowh { text-align: left; color: var(--ink); font-size: 0.88rem; }
.matrix td { text-align: center; padding: 4px; border-top: 1px solid var(--grid); }
.matrix button.cell { all: unset; cursor: pointer; display: inline-grid; place-items: center; width: 64px; height: 52px; border-radius: 6px; position: relative; }
.matrix button.cell:hover, .matrix button.cell:focus-visible { background: color-mix(in srgb, var(--accent) 10%, transparent); }
.matrix button.cell:focus-visible { outline: 2px solid var(--accent); }
.matrix button.cell[aria-pressed="true"] { background: color-mix(in srgb, var(--accent) 16%, transparent); }
.matrix .dot { border-radius: 50%; background: var(--seq-3); }
.matrix .n { position: absolute; right: 6px; bottom: 2px; font-size: 0.72rem; color: var(--ink-2); font-variant-numeric: tabular-nums; }
.matrix .empty { color: var(--muted); font-size: 0.75rem; }
#cell-detail { margin-top: 16px; }
#cell-detail .facet { overflow-x: auto; }
.rawtext { color: var(--ink-2); font-size: 0.82rem; }
.flagtxt { color: var(--critical); font-size: 0.76rem; }

/* neighbour bars */
.bars { display: grid; gap: 4px; max-width: 760px; }
.bar { display: grid; grid-template-columns: 200px 1fr 40px; align-items: center; gap: 8px; font-size: 0.88rem; }
.bar .track { height: 14px; }
.bar .fill { height: 14px; border-radius: 0 4px 4px 0; min-width: 2px; }
.bar .v { color: var(--ink-2); font-variant-numeric: tabular-nums; text-align: right; }
@media (max-width: 520px) { .bar { grid-template-columns: 120px 1fr 32px; } }

.cov { width: 100%; max-width: 900px; border-collapse: collapse; font-size: 0.88rem; background: var(--surface); border: 1px solid var(--ring); border-radius: 8px; overflow: hidden; }
.cov th, .cov td { padding: 6px 10px; border-top: 1px solid var(--grid); text-align: left; }
.cov th { color: var(--muted); font-weight: 500; font-size: 0.78rem; border-top: 0; }
.cov td.num { font-variant-numeric: tabular-nums; }
.small-multiples { display: grid; grid-template-columns: repeat(auto-fit, minmax(230px, 1fr)); gap: 16px; }
.small-multiples figure { margin: 0; background: var(--surface); border: 1px solid var(--ring); border-radius: 8px; padding: 12px; }
.small-multiples figcaption { font-size: 0.9rem; font-weight: 600; }

.method ol { max-width: 76ch; padding-left: 20px; }
.method li { margin-bottom: 8px; }

/* drawer */
.drawer { position: fixed; top: 0; right: 0; height: 100%; width: min(460px, 100%); background: var(--surface); border-left: 1px solid var(--ring); box-shadow: -8px 0 24px rgba(0,0,0,.12); transform: translateX(100%); transition: transform .2s ease; z-index: 20; overflow-y: auto; padding: 20px; }
.drawer.open { transform: none; }
.drawer-close { font: inherit; font-size: 0.9rem; background: none; border: 1px solid var(--axis); color: var(--ink); border-radius: 6px; padding: 4px 10px; cursor: pointer; float: right; }
.drawer h3 { margin: 4px 0 4px; font-size: 1.15rem; }
.drawer dl { display: grid; grid-template-columns: 130px 1fr; gap: 6px 12px; font-size: 0.88rem; margin: 16px 0; }
.drawer dt { color: var(--muted); }
.drawer dd { margin: 0; }
.drawer .box { border: 1px solid var(--ring); border-radius: 6px; padding: 10px 12px; margin: 12px 0; font-size: 0.88rem; }
.drawer .box h4 { margin: 0 0 6px; font-size: 0.85rem; color: var(--ink-2); font-weight: 600; }
@media (prefers-reduced-motion: reduce) { .drawer { transition: none; } html { scroll-behavior: auto; } }

.tooltip { position: fixed; pointer-events: none; z-index: 30; background: var(--surface); color: var(--ink); border: 1px solid var(--ring); box-shadow: 0 4px 16px rgba(0,0,0,.14); border-radius: 6px; padding: 8px 10px; font-size: 0.82rem; max-width: 300px; }
.tooltip b { font-variant-numeric: tabular-nums; }

```
