from __future__ import annotations

from os import PathLike

import pandas as pd
import numpy as np

from sklearn.preprocessing import StandardScaler

def import_bicliques(
    processed_data_file: str | PathLike[str],
    bicliques_file: str | PathLike[str],
    standardized: bool = False,
) -> tuple[pd.DataFrame, list[pd.DataFrame]]:
    """Load a processed feature matrix and extract its complete submatrices.

    Parameters
    ----------
    processed_data_file : str or path-like
        Parquet file containing the country-by-indicator matrix, including its
        missing values.

    bicliques_file : str or path-like
        CSV file containing serialized row and column index arrays for complete
        submatrices.

    standardized : bool, default=False
        Whether to standardize every feature before extracting submatrices.

    Returns
    -------
    data : pandas.DataFrame
        Loaded feature matrix, standardized when requested.

    complete_data : list of pandas.DataFrame
        Complete submatrices described by the biclique file.

    Raises
    ------
    ValueError
        If any extracted submatrix contains a missing value.
    """
    bicliques = pd.read_csv(bicliques_file, index_col=0)

    # bicliques are written in the file as strings separated with whitespace, with occasional \n
    bicliques['found_rows'] = bicliques['found_rows'].map(
        lambda s: np.fromstring(s.strip("[ ]").replace('\n', ''), sep=' ', dtype=int)
    )
    bicliques['found_cols'] = bicliques['found_cols'].map(
        lambda s: np.fromstring(s.strip("[ ]").replace('\n', ''), sep=' ', dtype=int)
    )

    data = pd.read_parquet(processed_data_file)

    if standardized:
        scaler = StandardScaler().set_output(transform="pandas")
        data = scaler.fit_transform(data)

    complete_data = []
    for _, bc in bicliques.iterrows():
        rows, cols = bc[["found_rows", "found_cols"]]
        complete_data.append(data.iloc[rows, cols])

    if not all(df.notna().all().all() for df in complete_data):
        raise ValueError("Bicliques contain missing elements")

    return data, complete_data
