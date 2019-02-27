"""
Test plotting of peaks
"""
from matplotlib import pyplot as plt
import bornagain as ba
from utils.histogram_utils import plot_surf
from simulation_builder import SimulationBuilder
import numpy as np


def plot_peaks(hist):
    # peaks = ba.FindPeaks(hist, 3, "nomarkov", 0.1)
    # xpeaks = [peak[0] for peak in peaks]
    # ypeaks = [peak[1] for peak in peaks]
    # print(peaks)
    # ba.plot_histogram(hist)
    # plt.plot(xpeaks, ypeaks, linestyle='None', marker='x', color='white', markersize=10)


    fig = plt.figure(figsize=(10.0, 20.0))

    ax = fig.add_subplot(2, 1, 1)
    crop = hist.crop(-2.5, 9.5, 1.5, 11.0)
    ba.plot_histogram(crop)
    ax2 = fig.add_subplot(2, 1, 2, projection='3d')
    plot_surf(crop, ax2)
    #
    # fig2 = plt.figure(figsize=(10.0, 20.0))
    # ax = fig.add_subplot(2, 1, 1)
    #
    # arr = np.log10(crop.array())
    # plt.hist(arr, bins='auto')



if __name__ == '__main__':
    units = ba.AxesUnits.DEGREES
    hist=SimulationBuilder().experimentalData().histogram2d(units)
    plot_peaks(hist)
    plt.show()

