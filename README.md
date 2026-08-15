# Can consensus across complete submatrices recover coherent country groupings from high-dimensional Global Findex data with structured missingness?
The Global Findex Database is used  to discover if there is a plausible grouping of countries based on available indicators. It is a source of data on how adults around the world access and use financial services.

Wave 5 data is used.
## Project objective
Do the countries form reproducible groups characterized by distinct patterns of financial-service access and use?

Or are the apparent groups arbitrary divisions of a continuous development spectrum, or are sensitive to indicator availability, missingness and the selected number of clusters.

Given the dataset's missigness, ranging from 9% in wave 3 to 42% in wave 5, the project tries to discover the structure of the data in wave 5, using unsupervised clustering.

The aim is to use available data without imputation and examine the robustness of the discovered structure.
## Method overview
Values reported as zero are treated as missing because of their [documented ambiguity](https://medium.com/@embeer/world-bank-data-suggests-0-of-australians-have-a-credit-card-obviously-false-a4d34dafacdf). Preprocessing involves scaling. Data in findex is survey and it is reported as percentages but the values are either fractions (0,1) or integers (0, 100).

The dataset from wave 5 is treated as a feature matrix with countries as rows and indicators as columns. This creates 140 x 280 matrix with 42% missingness.

Each indicator in the Findex DB has a [base value stored with up to 11 indicator values denoting stratification and one optional denominator information indicator](https://medium.com/@embeer/i-asked-ai-what-percentage-of-women-pay-bills-worldwide-1348144642bf). This project uses base values. Even though stratification provides relevant and potentially country differentiating information, it is not included to avoid having to account for groups of indicators with correlation close to 1.

The 140 x 280 feature matrix is used to discover submatrices without missing data. This is akin to tiling idea, even though tiles are not exhaustively enumerated, but a subset of tiles is discovered using randomized algorithm and then used. Those submatrices are then clustered using k-means. Clustering information from all the submatrices is combined into a consensus matrix. It is then clustered using aglomerative clustering, thus combining the clustering results from each separate dataset subset into one global result. This creates one final clustering for 140 countries.
## Main results
### The missingness in the dataset is structured
The Global Findex Database 2025: Connectivity and Financial Inclusion in the Digital Economy:
> Unlike what was the case in previous editions, data collection for The Global Findex 2025 gave priority to low- and middle-income economies. Data on mobile phone ownership, internet use, and account ownership were collected in all economies, but questions on financial use and financial health were asked only in low- and middle-income economies. In addition, in Algeria, China, the Islamic Republic of Iran, Libya, Mauritius, the Russian Federation, and Ukraine, an abridged form of the questionnaire was administered by phone because of economy-specific restrictions.

It is reflected in the data:
39 countries have 6 indicators available.
Overall missingness is 42%.

A complete submatrix (a tile) encompassing 140 countries and 6 indicators was recovered. The largest area-wise matrix is 72 x 208.
### The dataset has a multiresolution structure
### There is a submatrix which encompasses all 140 rows and 6 indicators and it provides a backbone grouping
### The final grouping reasigns countries based on data available in smaller subsets
The final grouping produces weaker separation when evaluated only in the 140 × 6 backbone space. This is expected because the consensus labels also incorporate indicators unavailable in that submatrix.
## Limitations
The main limitation is the property of the chosen method, that is unsupervised clustering. Because there is no known ground-truth country grouping, the result cannot be validated against a single definitive benchmark. One can validate internal cluster metrics and try to find external sources to validate the grouping against (like WB income level, HBR indicator). Ultimately the grouping reflects the dataset structure but it is beyond the scope of this project to assess the semantic meaning and it's releance to financial inclusion or wider econonomic and sociological implications as it is beyond the author's expertise.

The information about the percentage of people using account cannot be successfully recovered from the relevant indicators suggesting a [denominator problem](https://medium.com/@embeer/the-denominator-problem-in-findex-accd68dc3bbe). The account ownership is one of the backbone indicators in the dataset, available throughout all waves and only in the last wave the inconsistencies are present. Nevertheless this data, which is officially available, is used in the analysis.

The project does not model missingness under a specific MAR or MNAR mechanism.

The coverage is uneven. Some countries occur only in one submatrix, other occur in all 60 discovered submatrices. One reason is the dataset structure, where 39 countries are provided with data for 6 indicators and the rest is missing. Another is the randomized algorithm discovers only a subset of tiles.
## Future work
### Even coverage
There can be extensions of biclique selection which provide more even coverage. It is either thorough selecting bicliques through analyzing missingness structure or anchoring required values in the feature matrix and selecting bicliques specifically encompassing them.
## Repository structure
- [`Data/Processed/`](https://chatgpt.com/g/g-p-67c5df224ab08191b8b73edef920ff05/c/Data/Processed/) contains the processed country–indicator matrices, complete submatrices identified for each Findex wave, and the final Wave 5 clustering assignments.
- [`Notebooks/`](https://chatgpt.com/g/g-p-67c5df224ab08191b8b73edef920ff05/c/Notebooks/) contains the analysis workflow:
	- `01_Data_Preparation.ipynb` prepares the data, examines missingness across waves, and identifies complete submatrices. It links to functions outside this repository.
	- `02_EDA.ipynb` explores two of the Wave 5 submatrices and evaluates candidate cluster counts using K-means, silhouette diagnostics, PCA, and t-SNE.
    - `03_Clustering.ipynb` clusters individual submatrices, constructs the consensus matrix, and produces the final agglomerative clustering.
    - `04_Clustering_Analysis.ipynb` visualizes and profiles the final clusters and evaluates their relationships with individual indicators.
    - `05_correlation_exploration.ipynb` is a separate methodological exploration of Pearson correlations and is not part of the clustering pipeline. It is included because a Towards Data Science article is linking to it.
- [`Src/`](https://chatgpt.com/g/g-p-67c5df224ab08191b8b73edef920ff05/c/Src/) contains reusable functions for importing complete submatrices, evaluating clustering solutions, aligning cluster labels, and plotting clustering diagnostics.
- [`Sql/`](https://chatgpt.com/g/g-p-67c5df224ab08191b8b73edef920ff05/c/Sql/) contains queries used to extract the unstratified Findex indicators and inspect indicator coverage, population, and zero values.
- [`config.py`](https://chatgpt.com/g/g-p-67c5df224ab08191b8b73edef920ff05/c/config.py) defines paths to the local data sources and supports machine-specific overrides through `config_local.py`.
The main clustering workflow follows notebooks `01` through `04`; notebook `05` is supplementary.