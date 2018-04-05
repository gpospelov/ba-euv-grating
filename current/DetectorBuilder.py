import bornagain as ba
from bornagain.plot_utils import *
from bornagain import nm, deg
import numpy as np
import gzip
from matplotlib import pyplot as plt


class DetectorBuilder:
    def __init__(self):
        self.m_nx = 1024
        self.m_ny = 1024
        self.m_pixel_size = 13*1e-03  # mm
        self.m_alpha_inc = 10.71*deg
        self.m_beta_b = 78.75*deg
        self.m_beta_a = 79.83*deg
        self.m_length_s_ccd = 40.24
        self.m_beta_ccd = 180.0*deg - self.m_beta_b - self.m_alpha_inc
        self.m_a = np.sin(self.m_alpha_inc)*self.m_length_s_ccd/np.sin(self.m_beta_ccd)
        self.m_c = np.sin(self.m_beta_b)*self.m_length_s_ccd/np.sin(self.m_beta_ccd)
        self.m_alpha_sm = 180.0*deg - self.m_alpha_inc -self.m_beta_b - 90.0*deg
        self.m_da = np.sin(self.m_alpha_sm)*self.m_c
        self.m_n = np.cos(self.m_alpha_sm)*self.m_c
        self.m_n_z = -1.0*self.m_n*np.sin(self.m_alpha_sm)
        self.m_n_x = self.m_n*np.cos(self.m_alpha_sm)
        self.m_spec_u = 534*self.m_pixel_size
        self.m_spec_v = 683*self.m_pixel_size
        self.m_u0 = self.m_spec_u
        self.m_v0 = self.m_spec_v-(self.m_da + self.m_a)

    def width(self):
        return self.m_nx*self.m_pixel_size

    def height(self):
        return self.m_ny*self.m_pixel_size

    def print(self):
        print("--- CCDBuilder ---")
        print("m_alpha_inc     : {0}".format(self.m_alpha_inc/deg))
        print("m_beta_b        : {0}".format(self.m_beta_b/deg))
        print("m_beta_a        : {0}".format(self.m_beta_a/deg))
        print("m_length_s_ccd  : {0}".format(self.m_length_s_ccd))
        print("m_beta_ccd      : {0}".format(self.m_beta_ccd/deg))
        print("a               : {0}".format(self.m_a))
        print("c               : {0}".format(self.m_c))
        print("m_alpha_sm      : {0}".format(self.m_alpha_sm/deg))
        print("m_da            : {0}".format(self.m_da))
        print("m_n             : {0}".format(self.m_n))
        print("m_n_x           : {0}".format(self.m_n_x))
        print("m_n_z           : {0}".format(self.m_n_z))
        print("check           : {0}".format(np.sqrt(self.m_n_x**2 + self.m_n_z**2)))
        print("m_spec_u        : {0}".format(self.m_spec_u))
        print("m_spec_v        : {0}".format(self.m_spec_v))
        print("m_u0            : {0}".format(self.m_u0))
        print("m_v0            : {0}".format(self.m_v0))

    def read_file(self):

        arr = np.zeros((1024, 1024), dtype="float64")

        with gzip.open("../data/grt_scat_par.txt.gz", 'r') as f:
            nline = 0
            for l in f.readlines():
                arr[nline] = l.split()
                nline += 1

        arbitrary_scale = 100.0
        arr = arbitrary_scale*np.rot90(arr)

        hist = ba.Histogram2D(self.m_nx, 0.0, self.m_nx*self.m_pixel_size, self.m_ny, 0.0, self.m_ny*self.m_pixel_size)

        hist.setContent(arr)
        hist.save("../data/grt_scat_par.int.gz")
        return hist

    def create_detector(self):
        detector = ba.RectangularDetector(self.m_nx, self.width(), self.m_ny, self.height())
        normal = ba.kvector_t(self.m_n_x, 0, self.m_n_z)
        print("--- Detector created ---")
        print("Size           : {:d}x{:d}, {:6.3f}x{:6.3f}".format(self.m_nx, self.m_ny, self.width(), self.height()))
        print("normal         : {:6.3f} {:6.3f} {:6.3f}".format(self.m_n_x, 0, self.m_n_z))
        print("u0, v0         : {:6.3f} {:6.3f}".format(self.m_u0, self.m_v0))
        detector.setPosition(normal, self.m_u0, self.m_v0)
        return detector

    def get_histogram(self):
        result = ba.Histogram2D(self.m_nx, 0.0, self.width(), self.m_ny, 0.0, self.height())
        result.load("../data/grt_scat_par.int.gz")
        return result

    def apply_masks(self, simulation):
        simulation.maskAll()
        simulation.addMask(ba.Ellipse(self.width()/2, self.height()*0.02, self.width()*0.7, self.height()*0.8), False)
        simulation.addMask(ba.Ellipse(self.width()/2, -self.height()*0.3, self.width()*0.62, self.height()*0.8), True)

        # simulation.addMask(ba.Rectangle(0, 0, self.width()*0.45, self.height()), True)


if __name__ == '__main__':
    ccd = DetectorBuilder()
    ccd.print()

    hist = ccd.read_file()

    fig = plt.figure(figsize=(16, 8))

    plot_histogram(hist)
    plt.show()
