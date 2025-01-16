import matplotlib.pyplot as plt
import pandas as pd
import geopandas as gpd
from rapidfuzz import process, fuzz

def plot_metric_clusters(cluster_no, metric, iter_no, plot_title, xlabel, ylabel):
    """
    Plots the metric value for different cluster numbers
    across various iterations of K-means clustering.

    Parameters:
    - cluster_numbers (list or iterable): A list of cluster numbers to plot.
    - metric (dict): A dictionary where keys are tuples (cluster_number, parameter) and values are the metric.
    - iter_no (int): The number of K-means iterations.
    - plot_title (str): The main title for the entire plot.
        - plot_title (str): The main title for the entire plot.

    Returns:
    - None
    """
    subplot_height = 5

    plot_no = len(cluster_no)
    fig, ax = plt.subplots(plot_no, figsize = (10, subplot_height * plot_no))

    # If there's only one subplot, make ax iterable
    if plot_no == 1:
        ax = [ax]

    fig.suptitle(plot_title)
    fig.subplots_adjust(top = 0.94, hspace = 0.4)

    for i in range(plot_no):
        temp = {key[1]: val for key, val in metric.items() if key[0] == cluster_no[i]}
        ax[i].plot(temp.keys(), temp.values(), 'bx-')
        subplot_title = " ".join([str(cluster_no[i]), "clusters"])
        ax[i].set_title(subplot_title)
        ax[i].set_xlabel(xlabel)
        ax[i].set_ylabel(ylabel)
        ax[i].grid(True)

def align_country_codes(
    df1: pd.DataFrame,
    df2: pd.DataFrame,
    df1_code_col: str,
    df1_name_col: str,
    df2_code_col: str,
    df2_name_col: str,
    updated_code_col: str = "Updated Country Code",
    fuzzy_threshold: int = 60):
    """
    Aligns country codes in df1 with codes from df2.
    Uses direct code matching first, and falls back to fuzzy matching on the
    name columns if direct match is not found in df2.
    
    Parameters:
    - df1 : pd.DataFrame
        The primary DataFrame whose code column is updated.
    Must contain:
          - df1_code_col
          - df1_name_col
    - df2 : pd.DataFrame
        The secondary DataFrame that contains the desired codes.
        Must contain:
          - df2_code_col
          - df2_name_col
    - df1_code_col : str
        Name of the column in df1 that holds the initial codes.
    - df1_name_col : str
        Name of the column in df1 that holds the country names (for fuzzy matching).
    - df2_code_col : str
        Name of the column in df2 that holds the codes.
    - df2_name_col : str
        Name of the column in df2 that holds the country names (for fuzzy matching).
    - updated_code_col : str, optional
        Name of the new column in df1 that will store the updated codes.
        Defaults to "Updated Country Code".
    - fuzzy_threshold : int, optional
        Minimum fuzzy ratio to accept a match when direct code lookup fails,
        between 0 and 100. Defaults to 60.

    Returns:
    - changed_codes : list of tuples
        List of (df1_country_name, old_code, matched_country_name, matched_code)
        for each row where the code was changed.
    """

    # Initialize the updated code column
    df1[updated_code_col] = df1[df1_code_col].copy()

    # Keep track of changes
    changed_codes = []

    # Iterate through rows of df1 by index
    for idx in df1.index:
        df1_code = df1.at[idx, df1_code_col]
        df1_name = df1.at[idx, df1_name_col]

        code_data_exists = df2[df2_code_col] == df1_code

        if code_data_exists.sum() == 0:
            # Fuzzy match fallback on country name
            best_match = process.extractOne(
                query = df1_name,
                choices = df2[df2_name_col],
                scorer = fuzz.ratio,
                score_cutoff = fuzzy_threshold,
            )
            if best_match:
                # best_match => (matched_name, score, matched_index)
                matched_index = best_match[2]
                matched_name = df2.iloc[matched_index][df2_name_col]
                matched_code = df2.iloc[matched_index][df2_code_col]

                # Record the change
                changed_codes.append(
                    (df1_name, df1_code, matched_name, matched_code)
                )

                # Update df1 with the matched code
                df1.at[idx, updated_code_col] = matched_code

    return changed_codes

def plot_choropleth_map(
    countries_labels,
    world_shapefile_path,
    merge_column : str,
    cluster_column,
    output_filename="world_map.png",
):
    """
    Creates a choropleth map based on the specified cluster column in `countries_labels`.

    Parameters
    - countries_labels : pd.DataFrame
        Must have at least:
          - merge_column: the aligned SOV_A3 codes
          - The `cluster_column` containing the values to visualize
    - world_shapefile_path : str
        Path to the .shp file for the world shapefile
    - merge_column: str
        Column from countries_labels to merge on (right_on).
    - cluster_column : str
        The name of the column in `countries_labels` with clustering information
    - output_filename : str, optional
        Where to save the resulting PNG
    """

    # Load the shapefile
    world = gpd.GeoDataFrame.from_file(world_shapefile_path)

    # Merge shapefile with your labeled data
    # left_on: SOV_A3 in shapefile
    # right_on: "World Country Code" in countries_labels
    labeled_world = world.merge(
        countries_labels,
        how="left",
        left_on="SOV_A3",
        right_on = merge_column,
    )

    # Create the plot
    fig, ax = plt.subplots(figsize = (20,20))
    labeled_world.plot(
        ax=ax,
        column=cluster_column,
        edgecolor="darkgrey",
        categorical = True,
        legend=True,
        missing_kwds={
            "color": "lightgrey",
            "edgecolor": "darkgrey",
            "hatch": "///",
            "label": "Missing values",
        },
    )
    ax.set_axis_off()

    plt.savefig(output_filename)

    plt.show()
