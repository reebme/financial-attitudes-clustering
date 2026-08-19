# AGENTS.md

## Role

Maintain consistency between the code, analysis, and documented conclusions. Improve the repository's readability, inspectability, and reuse through focused software-engineering changes.

Point out inconsistencies and proactively suggest refactoring or analytical changes.

## Changes

- Do not regenerate data or notebook outputs unless the task requires it.

## Project objective

Determine whether Global Findex data supports reproducible country groupings despite structured missingness. The Wave 5 analysis avoids imputation: it clusters complete country-indicator submatrices, combines their co-clustering results into a consensus matrix, and derives final country groups with agglomerative clustering.

## Canonical workflow

1. `Notebooks/01_Data_Preparation.ipynb`: extract base indicators, treat zeros as missing, analyze missingness, and construct complete submatrices.
2. `Notebooks/02_EDA.ipynb`: evaluate candidate K-means structure using silhouettes, PCA, t-SNE, and refinement analysis.
3. `Notebooks/03_Clustering.ipynb`: cluster submatrices, build the consensus matrix, and produce final assignments.
4. `Notebooks/04_Clustering_Analysis.ipynb`: visualize and profile final clusters.
5. `Notebooks/05_correlation_exploration.ipynb`: supplementary experiment, not part of the clustering pipeline.

Reusable code is in `Src/`, extraction queries in `Sql/`, processed artifacts in `Data/Processed/`, and generated outputs in `Results/`.

## Methodological constraints

- Do not impute missing Findex values.
- Treat Findex values encoded as zero as missing.
- Use base/unstratified indicators.
- Standardize before extracting and clustering complete submatrices.
- Normalize pairwise consensus by the number of times each pair was jointly observed.
- Treat `-1` as absence from a submatrix, not as a cluster.
- Preserve country indices and indicator names.
- Do not assume a ground-truth grouping or overstate cluster separation; existing EDA suggests continuous and approximately multiresolution structure.
- Check that code, figures, metrics, and narrative conclusions remain mutually consistent.

## External dependencies

Some notebooks reference resources outside this repository:

- `config_local.py`: databases in the external `Curated_Data_SQLite` project
- Notebook 01: `../../Curated_Data_SQLite` and `../../rabbit_holes`
- Notebook 04: `../../Curated_Data_SQLite`
- Notebook 05: `../../Curated_Data_SQLite` and `../../Medium_Articles`

Do not inspect these resources or execute notebook cells that access them unless
explicitly instructed. A complete workflow run may be unavailable when these
external dependencies are not configured.
Full workflow execution may therefore be unavailable within the permitted boundary.

## Verification

Use checks proportional to the change:

```bash
git status --short
git diff --check
python -c "import ast, pathlib; [ast.parse(p.read_text()) for p in pathlib.Path('Src').glob('*.py')]"
python -c "import json, pathlib; [json.loads(p.read_text()) for p in pathlib.Path('Notebooks').glob('*.ipynb')]"
```

For analytical changes, also verify shapes, indices, missingness, biclique completeness, cluster-label semantics, and agreement between computed results and written conclusions. There is currently no automated test suite or dependency manifest.
