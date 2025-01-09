import matplotlib.pyplot as plt

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
