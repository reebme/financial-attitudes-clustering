from __future__ import annotations

from collections.abc import Iterable, Sequence
from typing import Any

import numpy as np
import numpy.typing as npt
from sklearn.metrics import confusion_matrix
from scipy.optimize import linear_sum_assignment
from itertools import product
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score, silhouette_samples
from scipy.stats import mode

LabelMapping = tuple[np.ndarray, np.ndarray]
MetricKey = tuple[Any, ...]


def find_label_alignement(
    reference: npt.ArrayLike,
    labels: npt.ArrayLike,
) -> LabelMapping:
    """Find the label permutation that best matches a reference clustering.

    A confusion matrix measures overlap between the two clusterings. The
    Hungarian assignment algorithm then finds the permutation that maximizes
    total overlap.

    Parameters
    ----------
    reference : array-like of shape (n_samples,)
        Reference cluster labels.

    labels : array-like of shape (n_samples,)
        Cluster labels to align with ``reference``.

    Returns
    -------
    tuple of numpy.ndarray
        Row and column indices returned by the Hungarian assignment. The first
        array identifies desired labels and the second identifies labels to
        replace.

    Raises
    ------
    ValueError
        If the two inputs contain different numbers of distinct clusters.
    """
    # the number of clusters
    no_clusters = len(set(labels))
    
    if no_clusters != len(set(reference)):
        raise ValueError("Relabeling impossible: number of clusters in 'labels' differs from the number of labels in 'reference'.")
    
    # build a confusion matrix (C[i,j]: element labeled j is labeled i in the reference
    cm = confusion_matrix(reference, labels)
    # scipy.optimize.linear_sum_assignment solves the assignement problem
    # here is finds such a permutation of the labels, which maximizes the trace (data points correctly assigned)
    return linear_sum_assignment(cm, maximize = True)

def relabel_clustering(
    reference: npt.ArrayLike,
    labels: np.ndarray,
    mapping: LabelMapping,
) -> np.ndarray:
    """Apply a label mapping to a clustering assignment.

    Parameters
    ----------
    reference : array-like of shape (n_samples,)
        Reference labels associated with the mapping. Retained for interface
        compatibility; the implementation does not inspect this argument.

    labels : numpy.ndarray of shape (n_samples,)
        Cluster labels to transform.

    mapping : tuple of numpy.ndarray
        Desired labels followed by the current labels they replace.

    Returns
    -------
    numpy.ndarray
        Labels aligned according to ``mapping``. If the mapping is already the
        identity, the original ``labels`` array is returned.
    """
    labels_match = (mapping[0] == mapping[1])
    if np.all(labels_match):
        #print("Labels match.")
        return labels
    relabeled = np.array(labels, copy = True)
    for i in range(len(mapping[0])):
        if labels_match[i] == False:
            #print("Changing", mapping[1][i], "to", mapping[0][i])
            mask = (labels == mapping[1][i])
            relabeled[mask] = mapping[0][i]
    return relabeled

def align_labels(clusters: Sequence[np.ndarray]) -> np.ndarray:
    """Align labels from repeated clustering runs to the first run.

    Parameters
    ----------
    clusters : sequence of numpy.ndarray
        Nonempty sequence of equal-length label arrays. The first array is used
        as the reference labeling.

    Returns
    -------
    numpy.ndarray of shape (n_iterations, n_samples)
        Label assignments after aligning every run to the first run.
    """
    reference_labels = clusters[0]
    aligned_clusters = [clusters[0]]
    for n in range(1, len(clusters)):
        mapping = find_label_alignement(reference_labels, clusters[n])
        aligned_clusters.append(relabel_clustering(reference_labels, clusters[n], mapping))
    # each effect of the clustering is in a row
    aligned_clusters = np.array(aligned_clusters)
    return aligned_clusters

def compute_kmeans_metrics(
    X_PCA: np.ndarray,
    param_grid: dict[str, Iterable[Any]],
    iter_no: int = 1,
) -> tuple[
    dict[MetricKey, float],
    dict[MetricKey, float],
    dict[MetricKey, float],
    dict[MetricKey, np.ndarray],
]:
    """Evaluate K-means parameter combinations over repeated fits.

    K-means is fitted on the selected leading PCA components. Silhouette
    metrics are calculated in the full supplied PCA space.

    Parameters
    ----------
    X_PCA : numpy.ndarray of shape (n_samples, n_components)
        PCA-transformed feature matrix.

    param_grid : dict of str to iterable
        Values to evaluate for each K-means parameter. The optional
        ``pca_components`` entry controls how many leading components are used
        for fitting and is not passed to ``KMeans``.

    iter_no : int, default=1
        Number of fits to average for each parameter combination.

    Returns
    -------
    mean_wgss : dict
        Mean within-cluster sum of squares by parameter combination.

    mean_silh_score : dict
        Mean silhouette score by parameter combination.

    mean_neg_silh_score : dict
        Mean fraction of observations with negative silhouette values.

    labels : dict
        Aligned label arrays for every fit and parameter combination.
    """
    # mean WGSS for each parameter combination
    mean_wgss = {}
    # mean silhouette score for each parameter combination
    mean_silh_score = {}
    # mean fraction of data points with a negative silhouette score
    mean_neg_silh_score = {}
    # clustering labels for each parameter combination
    labels = {}
    
    # exstract the names of the parameters
    param_names = list(param_grid.keys())

    default_param_settings = {}
    if 'n_init' not in param_names:
        default_param_settings['n_init'] = 30
    #the default number of principal components used in KMeans
    no_PCS = 3

    # extract the no of data points
    no_data_points = X_PCA.shape[0]

    # for all combinations of parameters (cartesian product of parameters' values)
    for values in product(*(param_grid[name] for name in param_names)):
        # produce a tuple of Kmeans parameters
        param_settings = dict(zip(param_names, values))
        # extract the number of principal components from parameters
        pcs = param_settings.pop('pca_components', no_PCS)

        iter_wgss = []
        iter_silh_score = []
        iter_neg_silh_score = []

        iter_labels = []

        for _ in range(iter_no):
            kmeans = KMeans(**param_settings, **default_param_settings).fit(X_PCA[:, 0:pcs])
            iter_wgss.append(kmeans.inertia_)
            iter_silh_score.append(silhouette_score(X_PCA, kmeans.labels_))
            iter_neg_silh_score.append(np.sum(silhouette_samples(X_PCA, kmeans.labels_) < 0)/no_data_points)
            iter_labels.append(kmeans.labels_)
        
        # reintroduce the number of principal components
        # if provided in param_grid
        if 'pca_components' in param_names:
            param_settings['pca_components'] = pcs

        param_key = tuple(param_settings.values())
        mean_wgss[param_key] = np.mean(iter_wgss)
        mean_silh_score[param_key] = np.mean(iter_silh_score)
        mean_neg_silh_score[param_key] = np.mean(iter_neg_silh_score)

        # handle labels
        # each row represents a clustering iteration
        aligned_labels = align_labels(iter_labels)

        # return aligned labels matrix for now
        labels[param_key] = aligned_labels
        
#        if np.all(aligned_labels[0, :] == aligned_labels):
#            # if the labels are the same return them
#            # print("All labeled the same.")
#            labels[param_key] = aligned_labels[0,:]
#        else:
#            # if the labels differ return the most frequent ones
#            # TODO substitute with consesus clustering
#            # or add a possibility of consesus lustering through a parameter
#            # print(param key)
#            # print("There are differences in labeling.")
#            labels[param_key], counts = mode(aligned_labels, axis=0)
#        
#        # TODO add a frequency matrix
#        # frequency of labeling matrix
#        # label_freq_arr = np.zeros((aligned_clusters.shape[1], K))
#        # for l in range(K):
#        #    label_freq_arr[:, l] = np.sum(aligned_clusters == l, axis = 0).T
#        # label_freq[K] = label_freq_arr/N

    return (mean_wgss, mean_silh_score, mean_neg_silh_score, labels)
