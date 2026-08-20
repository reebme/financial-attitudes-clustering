from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import Any

import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib as mpl
import matplotlib.colors as mcolors
from matplotlib.axes import Axes
from matplotlib.gridspec import GridSpec

import pandas as pd
import numpy as np
import numpy.typing as npt

from sklearn.metrics import silhouette_score, silhouette_samples

import plotting_utils

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
        ax.text(
            0.02,
            (y_lower + y_upper) / 2,
            str(k),
            fontsize=14,
            ha="left",
            va="center"
        )

        y_lower = y_upper + gap

    ax.axvline(mean_silh_score, c="red", linestyle='--', linewidth=0.5)
    ax.set_yticks([])
    for spine in ("top", "right", "left"):
        ax.spines[spine].set_visible(False)

    return ax


def plot_clustering_metrics(
    results: Mapping[str, Mapping[str, Any]],
    ks: Sequence[int],
) -> None:
    """Plot K-means evaluation metrics for one or more clustering results.

    Each result must provide ``data``, labels keyed by cluster count, fitted
    models keyed by cluster count, and a Matplotlib-compatible ``color``.
    The figure compares within-cluster sum of squares, mean silhouette score,
    and the share of observations with negative silhouette values.

    Parameters
    ----------
    results : mapping of str to mapping
        Named clustering results containing ``data``, ``labels``, ``models``,
        and ``color`` entries.
    ks : sequence of int
        Cluster counts to plot, in display order.
    """
    fig, axs = plt.subplots(
        nrows=1,
        ncols=3,
        figsize=(20, 5),
        layout="constrained",
        sharex=True,
    )
    fig.supxlabel("Number of clusters")

    plotting_utils.pretty_plot(
        axs[0],
        ks,
        [
            ([result["models"][k].inertia_ for k in ks], name, result["color"])
            for name, result in results.items()
        ],
        title="WGSS",
        y_axis_title="WGSS",
    )
    plotting_utils.pretty_plot(
        axs[1],
        ks,
        [
            (
                [silhouette_score(result["data"], result["labels"][k]) for k in ks],
                name,
                result["color"],
            )
            for name, result in results.items()
        ],
        title="Silhouette score",
        y_axis_title="Mean silhouette score",
    )
    plotting_utils.pretty_plot(
        axs[2],
        ks,
        [
            (
                [
                    np.mean(
                        silhouette_samples(result["data"], result["labels"][k]) < 0
                    )
                    for k in ks
                ],
                name,
                result["color"],
            )
            for name, result in results.items()
        ],
        title="Negative silhouettes",
        y_axis_title="Share of samples [%]",
    )
    axs[1].yaxis.set_major_formatter(mpl.ticker.StrMethodFormatter("{x:.2f}"))
    axs[2].yaxis.set_major_formatter(
        mpl.ticker.PercentFormatter(xmax=1, symbol=None)
    )
    plt.show()


def plot_silhouette_and_cluster_map(
    data: npt.ArrayLike,
    labels_by_k: pd.DataFrame,
    k: int,
    colors: Sequence[Any],
    title: str,
) -> None:
    """Plot silhouette diagnostics and a country cluster map for one K.

    The left column shows negatively silhouetted observation identifiers,
    grouped by assigned cluster, and the silhouette distribution. The right
    column shows the corresponding country cluster map.

    Parameters
    ----------
    data : array-like of shape (n_samples, n_features)
        Feature matrix used to compute silhouette values.
    labels_by_k : pandas.DataFrame
        Cluster assignments indexed by observation, with cluster counts as
        columns.
    k : int
        Cluster count to visualize.
    colors : sequence
        Matplotlib-compatible colors, one for each cluster.
    title : str
        Cluster-map title.
    """
    fig = plt.figure(figsize=(22, 10), layout="tight")
    gs = GridSpec(3, 2, figure=fig, width_ratios=[1, 4.75])
    negative_items_ax = fig.add_subplot(gs[0, 0])
    silhouette_ax = fig.add_subplot(gs[1:, 0])
    map_ax = fig.add_subplot(gs[:, 1])

    plotting_data = labels_by_k[k]
    clusters = np.sort(plotting_data.unique())
    negative_assignments = plotting_data[
        silhouette_samples(data, plotting_data) < 0
    ]
    palette = {
        cluster: mcolors.to_hex(color)
        for cluster, color in zip(clusters, colors)
    }

    plot_silhouette_scores_distribution(
        silhouette_ax, k, np.asarray(data), plotting_data.to_numpy(), np.asarray(colors[:k])
    )
    if len(negative_assignments) > 0:
        negative_items_ax.set_title("Negative silhouettes", fontsize=18, pad=14)
        negative_items_ax.text(
            0,
            1,
            "\n\n".join(
                f"Cluster {cluster}:\n" + "\n".join(map(str, assignments.index))
                for cluster, assignments in negative_assignments.groupby(
                    negative_assignments
                )
            ),
            fontsize=14,
            ha="left",
            va="top",
            transform=negative_items_ax.transAxes,
        )
    negative_items_ax.axis("off")

    plotting_utils.plot_cluster_map(
        map_ax,
        plotting_data,
        {label: str(label) for label in clusters},
        palette,
        title=title,
    )
    map_ax.set_anchor("W")
    plt.show()


def plot_refinement(
    purity_scores: Mapping[str, float],
    title: str = "",
) -> None:
    """Plot reassignment purity between successive cluster counts.

    Parameters
    ----------
    purity_scores : mapping of str to float
        Transition labels mapped to reassignment-purity values.
    title : str, default=""
        Optional title. A descriptive default is used when omitted.
    """
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(
        purity_scores.keys(),
        purity_scores.values(),
        "o--",
        linewidth=1,
        markersize=5,
    )
    ax.set_title(title or "Refinement between successive K-means partitions")
    ax.set_ylabel("Refinement purity")

    pad = 0.01
    max_purity = 1
    min_purity = min(purity_scores.values())
    for offset in (0, 0.05, 0.1):
        ax.axhline(
            max_purity - offset,
            linestyle="--",
            linewidth=1,
            c="grey",
            alpha=0.5,
        )
    ax.axhspan(max_purity - 0.05, max_purity, color="gainsboro", zorder=0)
    ax.axhspan(
        max_purity - 0.10,
        max_purity - 0.05,
        color="whitesmoke",
        zorder=0,
    )
    ax.set_ylim(min_purity - pad, max_purity + pad)
    ax.tick_params("x", rotation=45)
    ax.grid(True, alpha=0.2)
    for spine in ("top", "right"):
        ax.spines[spine].set_visible(False)
    plt.show()


def draw_marked_clusters(
    ax: Axes,
    cluster_labels: pd.Series,
    coords_x: npt.ArrayLike,
    coords_y: npt.ArrayLike,
    colors: Sequence[Any] | Mapping[int, Any],
    markers: Sequence[str] | Mapping[int, str],
    title: str = "",
    x_axis_title: str = "",
    y_axis_title: str = "",
    aspect_equal: str = "",
) -> Axes:
    """Draw labeled clusters using distinct colors and marker shapes.

    Parameters
    ----------
    ax : matplotlib.axes.Axes
        Axes on which to draw the clusters.
    cluster_labels : pandas.Series
        Integer cluster assignment for each coordinate pair.
    coords_x, coords_y : array-like of shape (n_samples,)
        Projection coordinates.
    colors : sequence or mapping
        Matplotlib-compatible color indexed by cluster identifier.
    markers : sequence or mapping
        Marker style indexed by cluster identifier.
    title, x_axis_title, y_axis_title : str, default=""
        Plot and axis titles.
    aspect_equal : str, default=""
        When nonempty, request equal aspect using this adjustable mode.

    Returns
    -------
    matplotlib.axes.Axes
        The modified axes.
    """
    x_values = np.asarray(coords_x)
    y_values = np.asarray(coords_y)
    clusters = np.sort(cluster_labels.unique())
    for cluster in clusters:
        cluster_mask = (cluster_labels == cluster).to_numpy()
        ax.scatter(
            x_values[cluster_mask],
            y_values[cluster_mask],
            color=colors[cluster],
            marker=markers[cluster],
            s=40,
            edgecolor="black",
            linewidth=0.25,
            label=cluster,
        )
    ax.tick_params(
        axis="both",
        which="both",
        bottom=False,
        left=False,
        labelbottom=False,
        labelleft=False,
    )
    if aspect_equal:
        ax.set_aspect("equal", adjustable=aspect_equal)
    ax.set_title(title)
    ax.set_xlabel(x_axis_title)
    ax.set_ylabel(y_axis_title)
    ax.legend()
    return ax

'''Unused functions retained for reference.

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
'''
