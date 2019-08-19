from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.colors import LightSource
from matplotlib import cm
from matplotlib import colors
import numpy as np


def add_to_histogram(sum_hist, current_hist, weight):
    orig = sum_hist.getArray()
    current = current_hist.getArray()
    res = orig + weight*current
    sum_hist.setContent(res)


def apply_mask_to_histogram(histogram, mask_hist):
    for i in range(0, histogram.getTotalNumberOfBins()):
        if mask_hist.getBinContent(i) == 1:
            histogram.setBinContent(i, 0)


def plot_surf(hist, ax, zmin=None, zmax=None):

    array = hist.array()

    zmax = np.amax(array) if zmax is None else zmax
    zmin = 1e-6*zmax if zmin is None else zmin

    if zmin == zmax == 0.0:
        norm = colors.Normalize(0, 1)
    else:
        norm = colors.LogNorm(zmin, zmax)


    print("1.1 zmin/zmax", zmin, zmax)
    zz = hist.array()
    x = hist.getXaxis().getBinCenters()
    y = hist.getYaxis().getBinCenters()
    xx, yy = np.meshgrid(x, y)
    print("1.2")

    # ls = LightSource(270, 45)
    # rgb = ls.shade(zz, blend_mode='soft', cmap=cm.coolwarm)
    # illuminated_surface = ls.shade(zz, cmap=cm.coolwarm)

    print("1.3")
    # fig = plt.figure(figsize=(9, 8), dpi=80, facecolor='w', edgecolor='k')
    # ax = fig.gca(projection='3d')
    print("1.4")

    # surf = ax.plot_surface(xx, yy, zz, rstride=1, cstride=1, linewidth=0, facecolors=illuminated_surface,
    #                        antialiased=True)

    print("1.5")
    surf = ax.plot_surface(xx, yy, np.log10(zz), cmap=cm.coolwarm,
                       linewidth=0, antialiased=False)
    print("1.6")

