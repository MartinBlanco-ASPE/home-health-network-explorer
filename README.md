# Home Health Network Explorer

[Open the interactive dashboard](https://martinblanco-aspe.github.io/home-health-network-explorer/) · [Detailed methodology](https://martinblanco-aspe.github.io/home-health-network-explorer/methodology.html)

Interactive analysis of CMS Home Health Quality, Certification and Oversight Reports (QCOR). Explore care wording in survey narratives, inspect source evidence, compare survey contexts, and browse an issue-to-regulation sunburst.

This is a separate home health study. Its records, vocabulary, policy references and screening rules are specific to home health. The hospice project supplies reusable interface code, not observations or study results.

## Version covered by these methods

Dashboard and methodology release: November 13, 2026. This repository reproduces the current reviewed dashboard, including target-specific care-concern simulations, four wording-removal strategies, the compact care-wording policy sunburst, agency-based ray extensions, within-category record-frequency shades, and layered hover/click highlighting.

## Open the dashboard

Download this repository as a ZIP, extract it, and open `index.html` in a modern browser. The dashboard bundles its data and libraries and works offline; regulatory reference links open online. Alternatively, run `python -m http.server 8000` from the repository and visit `http://localhost:8000`.

The dashboard has three tabs: Network graph, Issues & policy, and Methods & limits. The original 48-record pilot is accessible from Issues & policy. Use Calendar year, survey context and the other controls to explore selections; Advanced provides alternative graph constructions and diagnostic settings.

## Data and scope

The source is a home health CMS-2567/QCOR workbook covering survey dates January 2, 2018 through October 23, 2026. The workbook audit preserved 94,856 nonempty rows. This descriptive snapshot uses 54,377 candidate care and organizational records representing 6,122 source CMS Certification Numbers (CCNs). Calendar endpoints are partial years.

All 607 held historical, incomplete or otherwise uncertain records remain excluded. Emergency-preparedness E material and separate G context material are outside the care network. Eligibility and preparation counts are not national failure rates. Source CCNs are workbook identities, not independently reconciled agency histories.

The repository includes compact feature-incidence rows and 451 saved narrative illustrations, including the 48 pilot accounts. Saved examples are not a representative sample. Source workbook hashes and source-row traceability support auditability. The original workbook, full reconstructed narrative corpus, internal notes, archived policy PDFs and other study's data are outside this repository.

## From narratives to AI-assisted coding

Narrative text is organized in a dataframe: one source record per row, with agency ID, survey date, tag and narrative text. Derived columns store word/phrase occurrences, feature presence and rule-based screening flags. Counts support structured exploration; contextual reading supports provisional thematic interpretation.

We guided AI to read complete narratives, propose codes, preserve supporting excerpts and consider counterexamples. The documented pilot covers 48 accounts, not the whole corpus. This is AI-assisted analysis using task instructions and a provisional codebook; model fine-tuning is not documented. Literal pattern matching across the corpus does not turn every record into an AI-coded case. Wording clusters, screening families and interpretive codes remain separate.

[42 CFR Part 484](https://www.ecfr.gov/current/title-42/chapter-IV/subchapter-G/part-484) supplies Medicare home health participation requirements; [CMS State Operations Manual Appendix B](https://www.cms.gov/Regulations-and-Guidance/Guidance/Manuals/Downloads/som107ap_b_hha.pdf) supplies surveyor guidance. Existing issue-to-policy references anchor interpretation and source review. They do not establish that a matched word is a verified violation. The policy version in force at the survey date still requires checking.

## How to read the network

Nodes represent 52 selected wording features. Eight predefined care-issue screening families can also appear as diamonds. Node magnitude counts distinct source CCNs with matching wording in the active selection. Lines describe text associations, not relationships between providers or patient-level joint events.

General and screening views rescale circle sizes to the largest displayed count. A/B comparisons share one size reference, position frame and camera. Compare exact counts across separately filtered views. General views use an elastic layout; distances are browsing aids, not calibrated effect sizes.

Wording Cluster colors use deterministic weighted greedy modularity of the displayed connections. Groups and colors can change with filters, construction and resolution. They are exploratory partitions, separate from the predefined screening families and provisional pilot codes. Condition-level citation color and screening-share color describe different attributes; neither measures confirmed patient harm.

```math
\operatorname{coverage}(A)=\frac{c_A}{C},\qquad r_A=\max\left(8,42\sqrt{\frac{c_A}{c_{\max}}}\right)
```

Here c_A is the number of selected source CCNs mentioning A, C is all selected source CCNs, and c_max is the largest count among displayed nodes. In A/B comparison, both sides share c_max. Radius has a minimum visible size of 8; area follows count above that floor. Coverage uses distinct agencies even when connections use records.

## Text handling

Default evidence-oriented text begins after the first formal “not met as evidenced by” marker. Introductory regulatory wording is removed when that marker exists; quoted policies, goals, negation, clinical history and repeated narratives can remain. Full-text mode restores the leading material.

Identical-text collapse retains the first eligible record for each source CCN and exact normalized full-text combination within the current selection. Identical text at a different CCN remains. It does not merge similar meanings. Screening flags always use the evidence suffix, including when wording uses full text.

Wording uses disclosed case-insensitive regular-expression aliases. Features may overlap. Matching is lexical, with no stemming, embeddings or inferred semantic expansion. Alias definitions do not automatically assign interpretive pilot codes.

## Connection mathematics

The default general network uses positive pointwise mutual information (PPMI). N includes every eligible selected record, including records with none of the selected wording features.

```math
\operatorname{PPMI}(A,B)=\max\left(0,\log_2\frac{N n_{AB}}{n_A n_B}\right)
```

Here n_A and n_B count records mentioning each feature, n_AB counts records mentioning both, and N is all eligible selected records. Counts use binary presence per record. PPMI is the base-2 log of observed joint presence relative to the product of marginal proportions, floored at zero. For example, N = 1,000, n_A = 200, n_B = 100 and n_AB = 50 gives lift = 2.5 and PPMI ≈ 1.322. Records with neither feature still contribute to N. If either marginal is zero, no connection is constructed.

Keep at least 25 shared records and PPMI at least log2(1.5), approximately 0.585. Then retain the union of each endpoint's four strongest qualifying neighbors. The default graph has 52 wording nodes and 136 connections. Scores and cutoffs are display choices, not significance tests or clinical thresholds. Advanced overrides are marked custom.

The care-concern network uses weighted PPMI. Each narrative receives weight 1 + screening breadth; a feature still counts as present or absent within that narrative. Shared-record support remains unweighted.

```math
W=\sum_r w_r,\quad m_A=\sum_r w_r x_{rA},\quad m_{AB}=\sum_r w_r x_{rA}x_{rB}
```

Here x_rA equals 1 when narrative r mentions A and 0 otherwise. The same definition gives m_B. W includes all selected records, including records without a selected feature.

```math
\operatorname{PPMI}_w(A,B)=\max\left(0,\log_2\frac{W m_{AB}}{m_A m_B}\right)
```

With all weights equal to 1, this reduces to ordinary PPMI. Weighting describes breadth of matched wording, not patient harm or clinically validated severity.

### Alternative connection methods

```math
t_{rA}=(1+\ln c_{rA})\left(1+\ln\frac{N+1}{df_A+1}\right)
```

Here c_rA is the number of disclosed alias occurrences of A in record r, and df_A is the number of selected records containing A. The formula applies only to positive counts; absent features receive zero. First divide each record vector by its Euclidean length to obtain z. Empty record vectors remain zero.

```math
\operatorname{cos}(A,B)=\frac{\sum_r z_{rA}z_{rB}}{\sqrt{\sum_r z_{rA}^2}\sqrt{\sum_r z_{rB}^2}}
```

This compares normalized feature columns across narratives. It is not the same as comparing whole documents. The alternative cosine display cutoff is 0.12.

```math
\operatorname{cos}_{CCN}(A,B)=\frac{c_{AB}}{\sqrt{c_Ac_B}}
```

Here c_AB counts distinct source CCNs mentioning both features anywhere in the selected records. Unlike same-record PPMI, these mentions may occur in different records or years. Minimum shared support counts CCNs in this view. A zero denominator does not produce an edge.



The 18 saved construction sensitivities vary support, lift, text scope, deduplication, survey-group balancing, long-record exclusion, connection method, screen weighting and clustering resolution. Adjusted Rand Index measures partition agreement, not thematic validity. See [construction sensitivities](methods/construction_sensitivities.json) and [the frozen default graph](methods/default_graph.json).

## Removal simulations

Turn Simulation on in the map title bar. Play/Pause, Reset and the removal slider support deletion-only playback; manual phrase removal and pill restoration work while paused. Neutral colors retain teal phrase circles and red protected concern diamonds. Target-neighbor links receive red emphasis. Playback preserves pan and zoom. The calculations describe connectivity in the displayed text graph, not effects of clinical interventions.

```math
L=\frac{\max_i s_i}{N_0}
```

```math
F=1-\frac{\sum_i s_i(s_i-1)}{n(n-1)}
```

Here s_i is a surviving connected-component size and n is the surviving node count. Wording uses all starting phrases as its largest-piece denominator. The protected-diamond view uses all starting nodes, including diamonds. Wording follows the reviewer engine's F=1 convention when fewer than two nodes remain; the protected-diamond view uses F=0 in that edge case.

## Current simulation behavior

The explorer calls the weighted view Care concern patterns and the score filter Screening breadth. The empirical screening rules and analytical payload are unchanged. The local interface also removes the screening-share color, shows one Top 5 summary table, and hides the ordinary summary during simulation. These controls are included in the November 13 public release and supersede the November 7 interface.

Wording simulation analyzes 0–40 removals with four choices: Separate the wording clusters; Best path to shatter it; Make the largest piece smaller; Most common phrases. The default cluster-boundary separation needs 16 removals, proved optimal by integer programming. Shatter and shrink playback follow one finish-line removal set, so removed phrases do not return during Play. Four solid playback curves and two dotted per-count best-set references distinguish a sequential path from separately optimized sets. Larger best-found sets are not universal optimality claims. Cluster membership stays fixed during playback.

The care-concern simulation chooses one existing concern diamond. Stage 1 minimizes removable phrases separating that selected target from a strict-majority main component; every diamond remains protected, but other diamonds may remain in the main component. This supersedes the November 7 all-diamonds separation objective.

```math
\min_R |R|\quad\text{subject to }R\cap D=\varnothing,\ t\notin C,\ 2|C|>|V|-|R|
```

Here t is the selected target diamond and C is a complete surviving connected component. The strict-majority constraint applies only to Stage 1. Default 60-node/152-link target counts were proved optimal by independent integer programs at zero relative solver gap: service delivery 5; assessment 4; plan/orders 4; medication practice 3; clinical communication 4; infection prevention 3; competency/supervision 3; discharge/transfer 3. These counts are separate target solutions, not a combined removal set.

Stage 2 greedily removes phrases that most increase fragmentation until no surviving links remain, or reports a protected-edge obstruction. It has no minimum-removal guarantee. Changed graph topologies use best-found constrained max-flow cuts rather than inheriting default optimality. Minimum vertex-cut route certificates concern fixed endpoints; a matching certificate alone does not prove the separate majority-constrained optimum. Concern line charts are absent; per-target separation sentences and formulas appear below the map.

Both simulations start from the ordinary settled layout. Filter changes preserve camera position, and playback retains pan/zoom. Manual removal by clicking the map and restoration by pill remain available while paused. These calculations describe text-graph structure, not improvements in care or intervention effects. The edge weights build the displayed graph; surviving-edge connectivity is unweighted in removal calculations.

## Care-issue screening

Eight rule-based families flag service delivery, assessment, plans/orders, medication practice, clinical communication, infection prevention, competency/supervision, and discharge/transfer concerns. Patterns and context limits are included in [screening rules](methods/screening_rules.json).

```math
s_r=\min(3,f_r),\qquad w_r=1+s_r
```

Here f_r is the number of matched screening families in narrative r, s_r is the capped breadth score and w_r is its weight in the weighted network. Weights range from 1 to 4.

Each family has equal weight. This score measures the breadth of matched deficit wording, not clinically validated severity or immediate jeopardy (IJ). High score means 3; Moderate or High means 2–3; Any positive means 1–3. No screen match does not establish harmless care or paperwork-only findings. Documentation absence, quoted requirements and clinical context require source reading.

Severity-share color is the share of matching source CCNs with any positive screen: gray below 25%, light teal from 25% to below 50%, dark teal from 50% to 100%. Darker color means a larger screened share, not greater clinical severity.

## Issues and policy

The compact sunburst shows 52 care-wording phrases in 69 phrase–policy mappings across 12 regulatory sections. Eleven are in [42 CFR Part 484](https://www.ecfr.gov/current/title-42/chapter-IV/subchapter-G/part-484); respirator fit testing also has a separately scoped [OSHA 29 CFR 1910.134](https://www.osha.gov/laws-regs/regulations/standardnumber/1910/1910.134) reference. These are conceptual reference relationships, not adjudicated policy-specific citation counts.

Each ray has equal label space plus an extension proportional to distinct source agencies: extension = 100 × agency count / largest care-phrase agency count. Labels wrap in the compact chart. Equal angles count mappings. Hue identifies policy category. Light-to-dark shade represents matching-record frequency within that category: t = (records − category minimum) / (category maximum − category minimum). The color contribution increases linearly from 22% to 100%; tied/single-value categories use the full category color. Category shade scales are separate and cannot be compared as absolute counts across policies.

Hover previews a phrase or section; click locks it. A pointer-transparent focus layer outlines related sectors and temporarily fades unrelated sectors. A small Clear highlight button appears at the top right of the map only while a highlight is locked. The former highlight-summary card is omitted; hover tooltips and source details supply the information. The floating button, center click or Escape restores the original frequency shades without shifting the chart. The care-wording vocabulary and distinct-agency ray metric are fixed; there is no top filter toolbar. The phrase list, policy legend, exact counts, source evidence and original pilot navigation remain available. A phrase mapped to multiple sections repeats its corpus-wide value under each; do not add those repeated values as unique records.

The map uses the full candidate-care corpus, independently of network filters. Match counts describe wording, not confirmed patient harm, legal re-rating, nationally representative noncompliance or policy effects. Historical applicability and independent semantic validation remain pending.

## Downloads and traceability

Export edges creates an Excel workbook with Edges, CCN and year, and Export settings sheets. Edges assigns an edge_id. CCN and year lists supporting records, source CCNs, survey dates/years, source workbook rows and supported_edge_ids. Join on edge_id to identify the source agencies behind a connection. CCNs are text cells so leading zeros remain intact.

For same-record constructions, each supporting record contains both endpoint features. Same-CCN incidence may join mentions from different records or dates; those exports identify the distinction. Filters, comparison selection, text scope and within-CCN duplicate handling carry into the export. Edges CSV retains the original single-sheet option, and source-row CSV remains available. Excel is generated in the browser without a server or spreadsheet dependency.

Repeat appearances count matching CCNs on at least two distinct source survey dates in the selected view. Multiple rows on one date count once. Reused wording and follow-up citations can contribute; this is not a recurrence rate or a count of new failures.

## Reading coverage and limitations

One AI-assisted reading/coding pass covers 48 complete pilot accounts from 24 source CCNs, producing 91 provisional assignments across 15 concepts. Their 24 G cover memos and 11 separate E cover memos were read for context; E did not enter care coding or networks. Other saved source illustrations are automatically selected examples, not additional completed AI coding.

There is no independent human semantic validation, representative sampling or saturation claim. Vocabulary, codes, screening rules and clusters remain exploratory. There are no dedicated workbook fields for accreditor/surveyor, structured IJ, or original-report URLs; missing values are not recreated or classified as No. Source Condition/Standard hierarchy remains distinct from the screen.

The analysis does not establish patient-harm prevalence, provider ties, nationally representative noncompliance rates, causal policy effects, or policy recommendations. Historical amendments, waivers and state-specific applicability are not fully reconciled. Phase 4 policy-result synthesis is outside this public dashboard release.

## Repository contents

- `index.html`: self-contained dashboard, ready to open locally.
- `methodology.html`: browser-readable version of this README.
- `src/`: page shell, dashboard runtime, community and interaction code.
- `data/`: compact home-health snapshot, survey dates, reference groups, policy anchors and provenance.
- `methods/`: default graph, construction sensitivities and screening definitions.
- `vendor/`: bundled vis-network 9.1.9; see [third-party notices](THIRD_PARTY_NOTICES.md).
- `build.py` and `build_manifest.json`: reproducible build and SHA-256 inventory.
- `validation/`: release validation results.

## Rebuild

Python 3.10 or newer and its standard library are sufficient. No package installation or network access is needed.

```text
python build.py
python build.py --check
```

The build recreates index.html and methodology.html from the included snapshot and implementation, then records file hashes. The check verifies exact output bytes and manifest hashes. This reproduces the released dashboard, not the entire workbook-to-corpus audit or an independent revalidation of qualitative coding.

## Sources and status

Source context: [CMS QCOR](https://qcor.cms.gov/main.jsp), [42 CFR Part 484](https://www.ecfr.gov/current/title-42/chapter-IV/subchapter-G/part-484), and [CMS State Operations Manual Appendix B](https://www.cms.gov/Regulations-and-Guidance/Guidance/Manuals/Downloads/som107ap_b_hha.pdf). External policy pages may change after the release date.

Initial repository release: November 6, 2026. Study stage: Phase 3 descriptive exploration. This repository is a research presentation and is not an official CMS reporting product. Publication does not imply federal endorsement or advancement to Phase 4.

Published simulation/interface release: November 7, 2026. Documentation and readable-equation update: November 10, 2026. The current simulation controls and sunburst revisions are included in the November 13, 2026 release; the underlying home-health feature snapshot and screening definitions are unchanged.
