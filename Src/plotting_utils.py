import matplotlib.pyplot as plt
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
    countries_labels,
    world_shapefile_path,
    country_code_col = "Country Code",
    fuzzy_threshold = 60):
    """
    Aligns custom country codes in `countries_labels` with the shapefile's SOV_A3 codes.
    If no direct match is found, attempts fuzzy matching on the country name.

    Parameters:
    - countries_labels : pd.DataFrame
        DataFrame containing at least:
          - index representing country names (e.g., 'France')
          - a column with the code which is to be aligned, e.g., 'Country Code'
    - world_shapefile_path : str
        Path to the .shp file for the world shapefile
    - country_code_col : str, optional
        Column in `countries_labels` that holds initial codes
    - fuzzy_threshold : int, optional
        Minimum fuzzy ratio to accept a match when direct code lookup fails, between 0 and 100

    Returns:
    - updated_countries_labels : pd.DataFrame
        The same DataFrame with an additional column, e.g. "World Country Code"
    - changed_codes : list of tuples
        List of (country_name, old_code, new_country_name, new_code) for any row that was changed
    """
    # Load the world shapefile
    world = gpd.GeoDataFrame.from_file(world_shapefile_path)

    # Create a new column for SOV_A3 codes (copy from country_code_col).
    world_code_col = "World Country Code"
    countries_labels[world_code_col] = countries_labels[country_code_col].copy()

    changed_codes = []  # Keep track of any changes

    for country in countries_labels.index:
        my_code = countries_labels.loc[country][country_code_col]
        #my_data = " ".join(["My data:", my_code, country])
        
        # Check if SOV_A3 in shapefile matches my_code directly
        world_data_exists = world["SOV_A3"] == my_code
        
        #if world_data_exists.sum() == 1:
        #    world_data_entry = world[world_data_exists]
        #    world_data = " ".join(["World data:", world_data_entry["SOV_A3"].iloc[0], world_data_entry["NAME"].iloc[0]])
        #    print(world_data)
        if world_data_exists.sum() == 0:
            best_match = process.extractOne(
                query = country,
                choices = world['NAME'],
                scorer = fuzz.ratio,
                score_cutoff=fuzzy_threshold,
            )
            #print(my_data)
            if best_match:
                # best_match = (matched_name, score, index_in_world)
                world_code = world.iloc[best_match[2]]["SOV_A3"]
                world_country_name = world.iloc[best_match[2]]["NAME"]
                changed_codes.append((country, my_code, world_country_name, world_code))
                countries_labels.loc[country, world_code_col] = world_code

    return countries_labels, changed_codes

def plot_choropleth_map(
    countries_labels,
    world_shapefile_path,
    cluster_column,
    output_filename="world_map.png",
):
    """
    Creates a choropleth map based on the specified cluster column in `countries_labels`.

    Parameters
    - countries_labels : pd.DataFrame
        Must have at least:
          - "World Country Code" column: the aligned SOV_A3 codes
          - The `cluster_column` containing the values to visualize
    - world_shapefile_path : str
        Path to the .shp file for the world shapefile
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
        right_on="World Country Code"
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
