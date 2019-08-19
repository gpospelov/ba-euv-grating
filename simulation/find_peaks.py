"""
Reads experimental data and searches peaks on the plot.

Info is used to manually update experiments.json
"""
from experimental_setup import ExperimentalSetup
from matplotlib import pyplot as plt
from bornagain.plot_utils import *
from utils.json_utils import load_experimental_setup


def find_peaks(exp_config):
    setup = ExperimentalSetup(exp_config)
    hist = setup.get_histogram()

    # peaks = ba.FindPeaks(hist, 3, "nomarkov", 0.1)
    # peaks = ba.FindPeaks(hist, 5, "nobackgroundnomarkov", 0.01)
    peaks = ba.FindPeaks(hist, 4, "nobackgroundnomarkov", 0.01)
    xpeaks = [peak[0] for peak in peaks]
    ypeaks = [peak[1] for peak in peaks]

    ba.plot_histogram(hist)
    plt.plot(xpeaks, ypeaks, linestyle='None', marker='x', color='white', markersize=10)
    return xpeaks, ypeaks


def array_string(arr):
    """
    Return string representing array with limited precision
    """
    return str(["{0:0.2f}".format(i) for i in arr]).replace("'", "")


if __name__ == '__main__':

    cfg = load_experimental_setup("exp3")
    xp, yp = find_peaks(cfg)
    print("    \"xpeaks\"     : " + array_string(xp)+",")
    print("    \"ypeaks\"     : " + array_string(yp)+",")

    plt.show()
