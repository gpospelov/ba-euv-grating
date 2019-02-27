"""
Converts files from experiment into standard numpy text files
"""
import numpy as np
import gzip

nx, ny = 1024, 1024

exp1 = {
    "file_in"  : "grt_scat_par.txt.gz",
    "file_out" : "expdata1.txt.gz",
    "nrot"     : 1
}

exp2 = {
    "file_in"  : "2019-02-15/Exp.II_grating-at-10-deg-lin.asc.gz",
    "file_out" : "expdata2.txt.gz",
    "nrot"     : 2
}

exp3 = {
    "file_in"  : "2019-02-15/Exp.III_grating-at-05-deg-lin.asc.gz",
    "file_out" : "expdata3.txt.gz",
    "nrot"     : 2
}


def convert_file(pars):
    arr = np.zeros((1024, 1024), dtype="float64")

    filename = pars["file_in"]

    with gzip.open(filename, 'r') as f:
        nline = 0
        for l in f.readlines():
            arr[nline] = l.split()[0:1024]
            if nline%100 == 0:
                print(nline)
            nline += 1

    print(pars["nrot"])
    arr = np.rot90(arr, pars["nrot"])
    np.savetxt(pars["file_out"], arr)


if __name__ == '__main__':
    convert_file(exp3)
    print("done")