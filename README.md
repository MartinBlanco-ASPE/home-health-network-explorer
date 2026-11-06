# Home Health Network Explorer

Interactive analysis of CMS Home Health Quality, Certification and Oversight Reports (QCOR). Explore care wording in survey narratives, inspect source evidence, compare survey contexts, and browse an issue-to-regulation sunburst.

This is a separate home health study. Its records, vocabulary, policy references and screening rules are specific to home health. The hospice project supplies reusable interface code, not observations or study results.

## Open the dashboard

Download this repository as a ZIP, extract it, and open `index.html` in a modern browser. The dashboard bundles its data and libraries and works offline; regulatory reference links open online. Alternatively, run `python -m http.server 8000` from the repository and visit `http://localhost:8000`.

The dashboard has three tabs: Network graph, Issues & policy, and Methods & limits. The original 48-record pilot is accessible from Issues & policy. Use Calendar year, survey context and the other controls to explore selections; Advanced provides alternative graph constructions and diagnostic settings.

## Data and scope

The source is a home health CMS-2567/QCOR workbook covering survey dates January 2, 2018 through October 23, 2026. The workbook audit preserved 94,856 nonempty rows. This descriptive snapshot uses 54,377 candidate care and organizational records representing 6,122 source CMS Certification Numbers (CCNs). Calendar endpoints are partial years.

All 607 held historical, incomplete or otherwise uncertain records remain excluded. Emergency-preparedness E material and separate G context material are outside the care network. Eligibility and preparation counts are not national failure rates. Source CCNs are workbook identities, not independently reconciled agency histories.

The repository includes compact feature-incidence rows and 451 saved narrative illustrations, including the 48 pilot accounts. Saved examples are not a representative sample. Source workbook hashes and source-row traceability support auditability. The original workbook, full reconstructed narrative corpus, internal notes, archived policy PDFs and other study's data are outside this repository.

## How to read the network

Nodes represent 52 selected wording features. Eight predefined care-issue screening families can also appear as diamonds. Node magnitude counts distinct source CCNs with matching wording in the active selection. Lines describe text associations, not relationships between providers or patient-level joint events.

General and screening views rescale circle sizes to the largest displayed count. A/B comparisons share one size reference, position frame and camera. Compare exact counts across separately filtered views. General views use an elastic layout; distances are browsing aids, not calibrated effect sizes.

Wording Cluster colors use deterministic weighted greedy modularity of the displayed connections. Groups and colors can change with filters, construction and resolution. They are exploratory partitions, separate from the predefined screening families and provisional pilot codes. Condition-level citation color and screening-share color describe different attributes; neither measures confirmed patient harm.

## Text handling

Default evidence-oriented text begins after the first formal “not met as evidenced by” marker. Introductory regulatory wording is removed when that marker exists; quoted policies, goals, negation, clinical history and repeated narratives can remain. Full-text mode restores the leading material.

Identical-text collapse retains the first eligible record for each source CCN and exact normalized full-text combination within the current selection. Identical text at a different CCN remains. It does not merge similar meanings. Screening flags always use the evidence suffix, including when wording uses full text.

Wording uses disclosed case-insensitive regular-expression aliases. Features may overlap. Matching is lexical, with no stemming, embeddings or inferred semantic expansion. Displayed aliases do not automatically assign interpretive pilot codes.

## Connection mathematics

The default general network uses positive pointwise mutual information (PPMI). N includes every eligible selected record, including records with none of the selected wording features.

```text
P(A) = records mentioning A / N
P(A and B) = records mentioning both A and B / N
Lift(A, B) = P(A and B) / (P(A) * P(B))
PPMI(A, B) = max(0, log2(Lift(A, B)))
```

Keep at least 25 shared records and PPMI at least log2(1.5), approximately 0.585. Then retain the union of each endpoint's four strongest qualifying neighbors. The default graph has 52 wording nodes and 136 connections. Scores and cutoffs are display choices, not significance tests or clinical thresholds. Advanced overrides are marked custom.

The weighted alternative uses record weight 1 + screening score. Marginal and joint proportions use those weights; shared-record support remains unweighted. TF-IDF uses TF = 1 + ln(alias occurrences), IDF = ln((N+1)/(record frequency+1)) + 1, record-vector normalization, then cosine between feature columns. CCN-incidence cosine uses binary feature presence by agency and may connect mentions from different records or years.

The 18 saved construction sensitivities vary support, lift, text scope, deduplication, survey-group balancing, long-record exclusion, connection method, screen weighting and clustering resolution. Adjusted Rand Index measures partition agreement, not thematic validity. See [construction sensitivities](methods/construction_sensitivities.json) and [the frozen default graph](methods/default_graph.json).

## Care-issue screening

Eight rule-based families flag service delivery, assessment, plans/orders, medication practice, clinical communication, infection prevention, competency/supervision, and discharge/transfer concerns. Patterns and context limits are included in [screening rules](methods/screening_rules.json).

```text
screening score = min(3, number of matched families)
weighted-network record weight = 1 + screening score
```

Each family has equal weight. This score measures the breadth of matched deficit wording, not clinically validated severity or immediate jeopardy (IJ). High score means 3; Moderate or High means 2–3; Any positive means 1–3. No screen match does not establish harmless care or paperwork-only findings. Documentation absence, quoted requirements and clinical context require source reading.

Severity-share color is the share of matching source CCNs with any positive screen: gray below 25%, light teal from 25% to below 50%, dark teal from 50% to 100%. Darker color means a larger screened share, not greater clinical severity.

## Issues and policy

The sunburst maps all 60 wording/screen features to 81 distinct issue–section relationships across 12 sections. Eleven sections belong to [42 CFR Part 484 — Home Health Services](https://www.ecfr.gov/current/title-42/chapter-IV/subchapter-G/part-484). Respirator fit testing also has a separate OSHA 29 CFR 1910.134 reference with occupational and historical scope limits.

Each outer slice is one issue linked to one section; an issue can appear in several branches. Inner branch size counts those mappings. Arc size does not measure agency coverage, clinical seriousness, regulatory importance or harm. Colors identify sections.

Hover for the styled tooltip. Click a section or issue to lock its highlight and lighten other branches while preserving the full chart. Clear highlight, the center or Escape restores colors. The regulation dropdown filters explicitly. The detail panel provides plain-language explanations, exact policy links, related issues and saved evidence with CCNs and source rows.

This reference map uses full-corpus evidence-oriented counts independently of network filters. Export mapping downloads the displayed reference relationships. These are research reference links, not source-reported citations or verified violations. Existing policy anchors were checked November 5, 2026; survey-date applicability remains incomplete. Mapping is not a Phase 4 policy-result synthesis.

## Downloads and traceability

Export edges creates an Excel workbook with Edges, CCN and year, and Export settings sheets. Edges assigns an edge_id. CCN and year lists supporting records, source CCNs, survey dates/years, source workbook rows and supported_edge_ids. Join on edge_id to identify the source agencies behind a connection. CCNs are text cells so leading zeros remain intact.

For same-record constructions, each supporting record contains both endpoint features. Same-CCN incidence may join mentions from different records or dates; those exports identify the distinction. Filters, comparison selection, text scope and within-CCN duplicate handling carry into the export. Edges CSV retains the original single-sheet option, and source-row CSV remains available. Excel is generated in the browser without a server or spreadsheet dependency.

Repeat appearances count matching CCNs on at least two distinct source survey dates in the selected view. Multiple rows on one date count once. Reused wording and follow-up citations can contribute; this is not a recurrence rate or a count of new failures.

## Reading coverage and limitations

One AI-assisted reading/coding pass covers 48 complete pilot accounts from 24 source CCNs, producing 91 provisional assignments across 15 concepts. Their 24 G cover memos and 11 separate E cover memos were read for context; E did not enter care coding or networks. Other saved source illustrations are automatically selected examples, not additional completed AI coding.

There is no independent human semantic validation, representative sampling or saturation claim. Vocabulary, codes, screening rules and clusters remain exploratory. There are no dedicated workbook fields for accreditor/surveyor, structured IJ, or original-report URLs; missing values are not recreated or classified as No. Source Condition/Standard hierarchy remains distinct from the screen.

The analysis does not establish patient-harm prevalence, provider ties, nationally representative noncompliance rates, causal policy effects, or policy recommendations. Historical amendments, waivers and state-specific applicability are not fully reconciled. Phase 4 synthesis remains gated.

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
