import pandas as pd
import numpy as np

from sklearn.preprocessing import StandardScaler

def import_bicliques(processed_data_file, bicliques_file, standardized=False):
    '''
    processed_data_file contains the original data with missingness
    it's a pandas dataframe written into a parquet file
    bicliques_file contains a dataframe with found rows and columns of the complete submatrices
    it's a csv file, parquet won't serialize numpy arrays
    '''
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