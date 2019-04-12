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
from utils.json_utils import load_setup
from matplotlib import pyplot as plt
from utils.json_utils import load_experimental_setup


class ExperimentalSetup:
    def __init__(self, setup):
        self.nx = 1024
        self.ny = 1024
        self.pixel_size = 13*1e-03  # mm
        self.m_alpha_inc = setup["alpha_inc"]
        self.m_beta_b = setup["beta_b"]
        self.length_ccd = setup["length_ccd"]
        self.spec_u = setup["spec_y"]*self.pixel_size
        self.spec_v = setup["spec_x"]*self.pixel_size
        self.filename = setup["filename"]
        self.xpeaks = setup["xpeaks"]
        self.ypeaks = setup["ypeaks"]
        self.peak_radius = setup["peak_radius"]
        self.det_dx = setup["det_dx"]

        self.print()

    def alpha_inc(self):
        return self.m_alpha_inc*deg

    def beta_b(self):
        return self.m_beta_b*deg

    def print(self):
        print("alpha_inc     : {0}".format(self.m_alpha_inc))
        print("normal        : {0}".format(self.det_normal()))
        print("u0, v0        : {0}, {1}".format(self.det_u0(), self.det_v0()))
        print("nx, ny        : {0}, {1}".format(self.nx, self.ny))
        print("width, height : {0}, {1}".format(self.det_width(), self.det_height()))

    def det_normal(self):
        norm = np.sin(self.beta_b())*self.length_ccd
        n_x = norm*np.cos(self.det_alpha_sm())
        n_y = 0.0
        n_z = -1.0*norm*np.sin(self.det_alpha_sm())
        return [n_x, n_y, n_z]

    def det_pb_length(self):
        return np.sin(self.alpha_inc() + self.det_alpha_sm())*self.length_ccd

    def det_alpha_sm(self):
        return 180.0*deg - self.alpha_inc() -self.beta_b() - 90.0*deg

    def det_u0(self):
        return self.spec_u + self.det_dx

    def det_v0(self):
        return self.spec_v-self.det_pb_length()

    def det_width(self):
        return self.nx*self.pixel_size

    def det_height(self):
        return self.ny*self.pixel_size

    def create_detector(self):
        detector = ba.RectangularDetector(self.nx, self.det_width(), self.ny, self.det_height())
        n = self.det_normal()
        normal = ba.kvector_t(n[0], n[1], n[2])
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
        # simulation.addMask(ba.Ellipse(self.det_width()/2, self.det_height()*0.02, self.det_width()*0.69, self.det_height()*0.8), False)
        # simulation.addMask(ba.Ellipse(self.det_width()/2, -self.det_height()*0.3, self.det_width()*0.62, self.det_height()*0.8), True)
        for xp, yp in zip(self.xpeaks, self.ypeaks):
            simulation.addMask(ba.Ellipse(xp, yp, self.peak_radius, self.peak_radius), False)


if __name__ == '__main__':

    exp_config = load_experimental_setup("exp2")
    setup = ExperimentalSetup(exp_config)

    hist = setup.get_histogram()

    fig = plt.figure(figsize=(16, 8))
    plot_histogram(hist)

    plt.show()
