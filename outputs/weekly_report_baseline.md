# Weekly Research Intelligence — 2026-01-29

## Context

```
Active projects:
- PETase zero-shot variant ranking: protein engineering / BioML using esm, alphafold, pandas, pytorch, evcouplings. Goals: optimize NDCG@10 topK ranking, export act1/act2/expression ranks. Constraints: limited labels, compute-bound.

[Context doc: intelligence/context/docs/alignbio_zero_shot.md]
# Zero-shot phase pipeline (petorg) — CODEx context

## Objective
Produce a strong *ranking* of the Align2025 PETase test set (~5k variants) for **activity_1**, **activity_2**, and **expression**, optimized for **NDCG@10** (ordering matters; absolute calibration does not). The pipeline is: parse tool outputs → build a unified feature table → evaluate/iterate against reference labeled datasets → define scoring/ranking formulas → export ranked predictions for the PETase test set.

## Core modules (execution order)
1) build_features.py
- Role: assemble/merge per-variant features into one table.
- Inputs: standardized outputs produced by per-tool writers.
- Output: a single features TSV/CSV with stable row identity and consistent columns.
- Design rules:
  - Deterministic (same inputs => same output).
  - No “modeling” here; only parsing/merging/QC/normalization/flags.
  - Preserve raw tool columns; add consensus columns (means/medians/ranks) as additional features.
  - Always emit basic diagnostics: mutation_count, missing_* counts, and (if applicable) backbone_id / wt_id.

2) phase_analysis.py
- Role: analysis/QC + comparative dashboards on a features table (optionally joined with labels).
- Typical outputs:
  - Distributions/correlations by feature blocks.
  - TopK overlap / Jaccard between multiple score columns.
  - “Shared candidates” support counts in topK across multiple rankings.
  - (When labels exist) rank-metric evaluation (Spearman; NDCG@K; top-decile enrichment; etc.).

3) scorer.py
- Role: define score formulas that combine selected feature columns into 1+ score columns.
- Output: table with added score columns + ranks; used for ranking/submission-like export.
- Design rules:
  - Keep formulas explicit and versionable.
  - Prefer few ablations (baseline vs +stability penalty vs +evolutionary score) rather than many weights.
  - Optimize for ranking metrics (NDCG@K), not regression fit.

4) *_writer.py modules (one per tool)
- Role: adapters that parse raw tool outputs and write standardized, mergeable per-variant files.
- Must guarantee:
  - Consistent identifiers (variant_id; plus wt_id/backbone_id where relevant).
  - Clear “higher is better” vs “lower is better” sign conventions.
  - Machine-friendly formats (TSV/CSV/Parquet) with stable headers.
  - Explicit missing-value encoding + missingness summary.

## Tool writers currently in scope
- ESM1v writer: exports per-variant LLR-style features + delta-PLL vs WT; includes per-model and consensus aggregates.
- ESM2 writer: same idea; maintain sign conventions consistently across models.
- ESM3 writer: remote API outputs; avoid concurrency/auth failures; keep runs reproducible.
- EVcouplings writer: parses EVcouplings *webserver* outputs (not local compute) into per-variant features:
  - epistatic ΔE aggregates (sum/mean/min/max over mutations)
  - independent ΔE aggregates
  - frequency / conservation aggregates
  - missing-count diagnostics (mutations not scorable due to focus/coverage filtering)

## Ground-truth / benchmark datasets (for evaluation + iteration)
In parallel to feature engineering, we are assembling *reference labeled datasets* to test how well features rank variants on real labels. This is upstream evaluation work to inform the scorer/ranker that will be applied to the Align2025 PETase test set.

Key needs for each benchmark dataset:
- Identify the **wild-type (WT)** sequence and the **variant sequences** (or mutation strings).
- Build a reliable mapping of **WT↔variant** and/or reconstruct variant sequences from mutation codes.
- Understand what each **label** represents (activity/expression/stability, assay conditions, scale).
- Standardize to a consistent schema: (dataset_id, wt_id, variant_id, mutation_str, sequence, labels...).

Current / planned reference sets:
- Align2023 supervised train CSVs (used previously for ESM feature sanity checks):
  - in_silico_supervised/input/amylase/train.csv
  - in_silico_supervised/input/glucosidase/train.csv
- Additional benchmark corpora downloaded / to be integrated:
  - MaveDB (DMS-style datasets)
  - ProteinGym (benchmark collections)
  - Other local benchmark files already in repo (solubility/stability datasets, etc.)

These datasets are *not* the final target; they are used to evaluate whether features (ESM/EVcouplings/etc.) provide ranking signal aligned with experimentally measured properties, and to guide design of score formulas for the PETase Align2025 test set.

## Engineering constraints / repo hygiene
- Large datasets must be gitignored and never committed; history rewrite was already required once.
- Keep build_features deterministic and debuggable.
- Use consistent column naming end-to-end; do not silently rename.
- All stages should be runnable locally with clear CLI args and log output.
- Prefer append-only artifacts in data/processed/ (or similar), not ad-hoc scattered outputs.

---

# How to use CODEx effectively on this project

## What CODEx should do (repo-local work)
- Add/modify CLI args consistently across build_features.py / phase_analysis.py / scorer.py.
- Refactor writers to standardize:
  - identifiers (variant_id, wt_id/backbone_id)
  - sign conventions (“higher is better”)
  - missingness diagnostics
- Trace column usage end-to-end (writer → build_features merge → scorer formulas → phase_analysis plots).
- Implement evaluation harnesses that compute ranking metrics (NDCG@K, Spearman) given (features + labels).
- Enforce style invariants across modules (same headers, same output schema).

## What ChatGPT (this app) should do (analysis/strategy)
- Decide which features are plausible for act1 vs act2 vs expression (and why).
- Decide which benchmark datasets are suitable proxies and how to interpret their labels.
- Propose ablation plans and scorer formula candidates.
- Help debug conceptual issues (e.g., WT mapping, sign flips, label leakage, dataset mismatch).

## Practical CODEx prompt patterns (copy/paste)
- “Search the repo for where 
...[truncated]

```

## Items

### papers: AlphaGenome
- URL: https://www.nature.com/articles/s41586-025-10014-0
- Notes: DNA foundation model for regulatory variant effects; assess if transferable to expression prediction in our setting.
- Relevance: STUB (wire LLM later)
- Why: STUB
- How to leverage (1 month): STUB

### github: facebookresearch/esm
- Notes: ESM protein language models; check updates relevant to embedding extraction / scoring.
- Relevance: STUB (wire LLM later)
- Why: STUB
- How to leverage (1 month): STUB

### github: pandas-dev/pandas
- Notes: Track pandas 3.x changes (copy-on-write) for pipeline performance/memory behavior.
- Relevance: STUB (wire LLM later)
- Why: STUB
- How to leverage (1 month): STUB

### docs: Pandas 3.0 whatsnew
- URL: https://pandas.pydata.org/docs/whatsnew/v3.0.0.html
- Notes: Key API + performance changes; note breaking changes impacting our notebooks.
- Relevance: STUB (wire LLM later)
- Why: STUB
- How to leverage (1 month): STUB
