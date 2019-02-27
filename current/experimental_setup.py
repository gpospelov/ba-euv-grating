"""
Experimental setup.

Contains detector geometry description for all 3 experiments and set of functions
to load experimental data and to build corresponding RectangularDetector.
"""
import os
import bornagain as ba
from bornagain import deg
from bornagain.plot_utils import *
import json
import numpy as np
import gzip
from matplotlib import pyplot as plt


DESCRIPTION = os.path.join(os.path.dirname(os.path.abspath(__file__)), "experiments.json")


class ExperimentalSetup:
    def __init__(self, setup_name):
        self.nx = 1024
        self.ny = 1024
        self.pixel_size = 13*1e-03  # mm
        self.alpha_inc = None
        self.beta_a = None
        self.beta_b = None
        self.length_ccd = None
        self.spec_u = None
        self.spec_v = None
        self.m_arr = None
        self.filename = None
        self.xpeaks = None
        self.ypeaks = None

        self.load_setup(setup_name)
        self.print()

    def print(self):
        print("alpha_inc     : {0}".format(self.alpha_inc/deg))
        print("normal        : {0}".format(self.det_normal()))
        print("u0, v0        : {0}, {1}".format(self.det_u0(), self.det_v0()))

    def load_setup(self, setup_name):
        """
        Loads json description of 3 experiments from current directory.
        """
        print("{0}\n{1}: '{2}'\n{3}".format('-'*80, "Experiment", setup_name, '-'*80))

        with open(DESCRIPTION) as json_file:
            setup = json.load(json_file)[setup_name]
            self.alpha_inc = setup["alpha_inc"]*deg
            self.beta_a = setup["beta_a"]*deg
            self.beta_b = setup["beta_b"]*deg
            self.length_ccd = setup["length_ccd"]
            self.spec_u = setup["spec_y"]*self.pixel_size
            self.spec_v = setup["spec_x"]*self.pixel_size
            self.filename = setup["filename"]
            self.xpeaks = setup["xpeaks"]
            self.ypeaks = setup["ypeaks"]

    def det_normal(self):
        norm = np.cos(self.det_alpha_sm())*self.det_c_length()
        n_x = norm*np.cos(self.det_alpha_sm())
        n_y = 0.0
        n_z = -1.0*norm*np.sin(self.det_alpha_sm())
        return [n_x, n_y, n_z]

    def det_beta_ccd(self):
        return 180.0*deg - self.beta_b - self.alpha_inc

    def det_pb_length(self):
        a = np.sin(self.alpha_inc)*self.length_ccd/np.sin(self.det_beta_ccd())
        da = np.sin(self.det_alpha_sm())*self.det_c_length()
        return a + da

    def det_c_length(self):
        return np.sin(self.beta_b) * self.length_ccd / np.sin(self.det_beta_ccd())

    def det_alpha_sm(self):
        return 180.0*deg - self.alpha_inc -self.beta_b - 90.0*deg

    def det_u0(self):
        return self.spec_u

    def det_v0(self):
        return self.spec_v-self.det_pb_length()

    def det_width(self):
        return self.nx*self.pixel_size

    def det_height(self):
        return self.ny*self.pixel_size

    def create_detector(self):
        detector = ba.RectangularDetector(self.nx, self.det_width(), self.ny, self.det_height())
        normal = ba.kvector_t(self.det_normal()[0], 0, self.det_normal()[2])
        detector.setPosition(normal, self.det_u0(), self.det_v0())
        return detector

    def get_histogram(self):
        filename = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data", self.filename)
        print("loading histogram from: "+filename)
        result = ba.Histogram2D(self.nx, 0.0, self.det_width(), self.ny, 0.0, self.det_height())

        self.m_arr = np.loadtxt(filename)
        result.setContent(self.m_arr)
        return result

    def apply_masks(self, simulation):
        simulation.maskAll()

        for xp, yp in zip(self.xpeaks, self.ypeaks):
            simulation.addMask(ba.Ellipse(xp, yp, 0.5, 0.5), False)


if __name__ == '__main__':
    setup = ExperimentalSetup("exp1")
    hist = setup.get_histogram()

    fig = plt.figure(figsize=(16, 8))
    plot_histogram(hist)

    plt.show()
