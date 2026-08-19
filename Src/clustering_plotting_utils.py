from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import Any

import matplotlib.pyplot as plt
import matplotlib.cm as cm
from matplotlib.axes import Axes

import pandas as pd
import numpy as np

from sklearn.metrics import silhouette_score, silhouette_samples

def plot_silhouette_scores_distribution(
    ax: Axes,
    no_clusters: int, 
    data: np.ndarray, 
    labels: np.ndarray, 
    colors: np.ndarray
) -> Axes:
    """Plot per-cluster silhouette distributions on an axes object.

    Cluster labels must be consecutive integers from zero through
    ``no_clusters - 1``. ``data`` contains observations by row and features by
    column, and ``labels`` must contain one label per observation.

    Parameters
    ----------
    ax : matplotlib.axes.Axes
        Axes on which to draw the distributions.

    no_clusters : int
        Number of clusters represented by ``labels``.

    data : numpy.ndarray of shape (n_samples, n_features)
        Feature matrix used to compute silhouette values.

    labels : numpy.ndarray of shape (n_samples,)
        Cluster label for each observation.

    colors : numpy.ndarray of shape (no_clusters, ...)
        One Matplotlib-compatible color per cluster.

    Returns
    -------
    matplotlib.axes.Axes
        The modified axes.

    Raises
    ------
    ValueError
        If the number of colors differs from ``no_clusters``.
    """
    if len(colors) != no_clusters:
        raise ValueError(f"{no_clusters} clusters and {len(colors)} colors supplied.")

    mean_silh_score = silhouette_score(data, labels)

    gap = 1
    y_lower = gap
    
    ind_silh_score = silhouette_samples(data, labels)
    for k in range(no_clusters):
        ind_k_silh_score = ind_silh_score[labels == k]
        ind_k_silh_score.sort()

        k_size = ind_k_silh_score.shape[0]
        y_upper = y_lower + k_size

        k_color = colors[k]
        ax.fill_betweenx(
            np.arange(y_lower, y_upper),
            0,
            ind_k_silh_score,
            facecolor=k_color,
            edgecolor=k_color
        )

        y_lower = y_upper + gap

    ax.axvline(mean_silh_score, c="red", linestyle='--', linewidth=0.5)

    return ax

def plot_metric_clusters(
    cluster_no: Sequence[int],
    metric: Mapping[tuple[int, Any], float],
    iter_no: int,
    plot_title: str,
    xlabel: str,
    ylabel: str,
) -> None:
    """Plot a clustering metric against a secondary parameter for each K.

    Parameters
    ----------
    cluster_no : sequence of int
        Cluster counts for which to create subplots.

    metric : mapping
        Metric values keyed by ``(cluster_count, parameter_value)``.

    iter_no : int
        Number of K-means iterations represented by the metric. Retained for
        compatibility; the implementation does not inspect this argument.

    plot_title : str
        Figure title.

    xlabel : str
        Label for each subplot's x-axis.

    ylabel : str
        Label for each subplot's y-axis.

    Returns
    -------
    None
        The function creates and configures a Matplotlib figure.
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
    fuzzy_threshold: int = 60,
) -> list[tuple[Any, Any, Any, Any]]:
    """Update country codes in ``df1`` using direct or fuzzy matches in ``df2``.

    ``df1`` is mutated by adding ``updated_code_col``. Direct code matches are
    retained; unmatched codes fall back to fuzzy country-name matching.

    Parameters
    ----------
    df1 : pandas.DataFrame
        DataFrame whose country codes are updated. This object is modified in
        place by adding ``updated_code_col``.

    df2 : pandas.DataFrame
        Reference DataFrame containing the desired country codes.

    df1_code_col : str
        Name of the country-code column in ``df1``.

    df1_name_col : str
        Name of the country-name column in ``df1``.

    df2_code_col : str
        Name of the country-code column in ``df2``.

    df2_name_col : str
        Name of the country-name column in ``df2``.

    updated_code_col : str, default="Updated Country Code"
        Name of the new column in ``df1`` that receives aligned codes.

    fuzzy_threshold : int, default=60
        Minimum accepted fuzzy-match score from 0 to 100.

    Returns
    -------
    list of tuple
        Source name, source code, matched name, and matched code for every row
        whose code changed.
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
