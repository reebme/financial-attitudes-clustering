import numpy as np
from sklearn.metrics import confusion_matrix
from scipy.optimize import linear_sum_assignment

def find_label_alignement(reference, labels):
    """
    Align cluster labels to match a reference labeling.

    When K-means clustering is performed multiple times, the numerical labels assigned to clusters
    can differ between runs even if the cluster assignments are effectively the same. This function
    realigns the labels in `labels` to best match the `reference` labels by finding an optimal
    permutation of label assignments that maximizes the correspondence between clusters.

    This function uses a confusion matrix to evaluate the correspondence between clusters and applies
    the Hungarian algorithm (linear_sum_assignment) to find the optimal label permutation.

    Parameters:
    - reference : array-like of shape (n_samples,)
        The reference labels to which the cluster labels should be aligned. This could be the true
        labels in a supervised setting or a consistent labeling from a previous clustering run.

    - labels : array-like of shape (n_samples,)
        The cluster labels obtained from a K-means clustering run that need to be realigned to match
        the reference labels.

    Returns:
    - mapping (tuple of array-like): A tuple containing two lists or arrays:
            - mapping[0]: Desired labels.
            - mapping[1]: Current labels to be replaced.
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

def relabel_clustering(reference, labels, mapping):
    """
    Relabel cluster assignments to align with a reference using a provided mapping.

    This function updates the cluster labels in `labels` based on the `mapping` to match
    the `reference` labels. If the current labels already align with the reference, it
    returns the original labels. Otherwise, it replaces labels according to the mapping.

    Parameters:
    - reference (array-like): The reference labels to align to.
    - labels (array-like): The current cluster labels to be relabeled.
    - mapping (tuple of array-like): A tuple containing two lists or arrays:
            - mapping[0]: Desired labels.
            - mapping[1]: Current labels to be replaced.

    Returns:
        numpy.ndarray: The relabeled cluster assignments aligned to the reference.
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

def align_labels(clusters):
    """
    Aligns cluster labels across multiple clustering iterations to ensure consistency.

    Uses the first clustering iteration as a reference and realigns subsequent cluster
    labels to match the reference. This is useful when different clustering runs assign
    different numerical labels to the same clusters.

    Parameters:
    - clusters (list of numpy.ndarray): A list where each element is a NumPy array containing
            cluster labels from a clustering iteration. All arrays should have the same length,
            corresponding to the number of data points.

    Returns:
    - numpy.ndarray: A 2D NumPy array of shape (n_iterations, n_data_points) with aligned
            cluster labels, where each row represents a clustering iteration.
    """
    reference_labels = clusters[0]
    aligned_clusters = [clusters[0]]
    for n in range(1, len(clusters)):
        mapping = find_label_alignement(reference_labels, clusters[n])
        aligned_clusters.append(relabel_clustering(reference_labels, clusters[n], mapping))
    # each effect of the clustering is in a row
    aligned_clusters = np.array(aligned_clusters)
    return aligned_clusters
