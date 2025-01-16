import numpy as np
from sklearn.metrics import confusion_matrix
from scipy.optimize import linear_sum_assignment
from itertools import product
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score, silhouette_samples
from scipy.stats import mode

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

def compute_kmeans_metrics(X_PCA, param_grid, iter_no = 1):
    """
    Compute mean Within-Group Sum of Squares (WGSS) and silhouette scores for each KMeans parameter combination.

    Parameters:
    - X_PCA (array-like): PCA-transformed dataset.
    - param_grid (dict): Dictionary of KMeans parameters and their possible values (list or iterable).
    - iter_no (int, optional): Number of iterations to average the metrics over. Defaults to 1.

    Returns:
    - tuple: 
        - mean_wgss (dict): Average WGSS for each parameter combination.
        - mean_silh_score (dict): Average silhouette score for each parameter combination.
        - mean_neg_silh_score (dict): Average fraction of samples with a negative silhouette score
                                        for each parameter combination.
        - labels (dict): Clustering labels for each parameter combination.
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
        
        if np.all(aligned_labels[0, :] == aligned_labels):
            # if the labels are the same return them
            # print("All labeled the same.")
            labels[param_key] = aligned_labels[0,:]
        else:
            # if the labels differ return the most frequent ones
            # TODO substitute with consesus clustering
            # or add a possibility of consesus lustering through a parameter
            # print(param key)
            # print("There are differences in labeling.")
            labels[param_key], counts = mode(aligned_labels, axis=0)
        
        # TODO add a frequency matrix
        # frequency of labeling matrix
        # label_freq_arr = np.zeros((aligned_clusters.shape[1], K))
        # for l in range(K):
        #    label_freq_arr[:, l] = np.sum(aligned_clusters == l, axis = 0).T
        # label_freq[K] = label_freq_arr/N

    return (mean_wgss, mean_silh_score, mean_neg_silh_score, labels)
