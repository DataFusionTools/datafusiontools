import matplotlib.pyplot as plt
import numpy as np


def plot_2d_interpolation_results_with_var( points_2d_slice, results_2d_slice, variance ):
    # the results of the variance in 2d using contourf
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 10))
    ax1.set_xlabel("x")
    ax1.set_ylabel("y")
    ax1.set_title("Interpolation results")
    ax2.set_xlabel("x")
    ax2.set_ylabel("y")
    ax2.set_title("Variance results")
    # get the x and y coordinates
    x = points_2d_slice[:, 0]
    y = points_2d_slice[:, -1]
    # get the z coordinates
    z = results_2d_slice
    # get the variance
    variance = np.array(variance)
    # plot the results as scatter
    ax1.scatter(x, y, c=z, cmap="RdBu_r")
    ax2.scatter(x, y, c=variance, cmap="RdBu_r")
    # add the colorbar per subplot
    fig.colorbar(ax1.scatter(x, y, c=z, cmap="RdBu_r"), ax=ax1)
    fig.colorbar(ax2.scatter(x, y, c=variance, cmap="RdBu_r"), ax=ax2)
    # show the plot
    plt.show()