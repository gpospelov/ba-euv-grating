"""
Converts files from experiment into standard numpy text files
"""
import numpy as np
import gzip
from matplotlib import pyplot as plt
from bornagain.plot_utils import *

nx, ny = 1024, 1024

exp1 = {
    "file_in"  : "grt_scat_par.txt.gz",
    "file_out" : "expdata1.txt.gz",
    "nrot"     : 1,
    "scale"    : 100.0,
    "flip"     : -1
}

exp2 = {
    "file_in"  : "2019-02-15/Exp.II_grating-at-10-deg-lin.asc.gz",
    "file_out" : "expdata2.txt.gz",
    "nrot"     : 0,
    "scale"    : 100.0,
    "flip"     : 0
}

exp3 = {
    "file_in"  : "2019-02-15/Exp.III_grating-at-05-deg-lin.asc.gz",
    "file_out" : "expdata3.txt.gz",
    "nrot"     : 0,
    "scale"    : 100.0,
    "flip"     : 0
}


def convert_file(pars):
    """
    Reads experimental file, apply threshold, rotate if necessary and save as standard numpy file.
    """
    arr = np.zeros((1024, 1024), dtype="float64")

    filename = pars["file_in"]

    with gzip.open(filename, 'r') as f:
        nline = 0
        for l in f.readlines():
            arr[nline] = l.split()[0:1024]
            if nline%100 == 0:
                print(nline)
            nline += 1

    processed = np.copy(arr)
    if pars["nrot"]>0:
        processed = pars["scale"]*np.rot90(arr, pars["nrot"])

    print(processed)
    if pars["flip"] >= 0:
        processed = np.flip(processed, pars["flip"])

    print(processed)
    processed[processed<0] = 0.0

    np.savetxt(pars["file_out"], processed)

    return arr, processed


def plot_data(raw, processed):
    fig = plt.figure(figsize=(18, 18))

    plt.subplot(2, 2, 1)
    plot_array(raw)

    plt.subplot(2, 2, 2)
    plot_array(processed)

    plt.subplot(2, 2, 3)
    nhist, bin_edges  = np.histogram(raw, bins=1024, range=(-100, 65536.))
    plt.semilogy(bin_edges[:-1], nhist)
    plt.ylim(0, 1e+6)


if __name__ == '__main__':
    raw, processed = convert_file(exp2)
    plot_data(raw, processed)

    # array = np.array([[0, 1, 2, 3, 4],[5, 6, 7, 8, 9], [10, 11, 12, 13, 14]])
    # plt.imshow(array, origin="lower")
    # plot_array(array)


    plt.show()
