"""
Base class for all grating builders.
"""
from bornagain import deg


class GratingBase:
    def __init__(self, exp_setup, sample_setup):
        self.m_rotation_angle = exp_setup["sample_rotation"]

    def rotation_angle(self):
        return self.m_rotation_angle*deg

    def add_parameters(self, run_parameters):
        run_parameters.add_parameters(self)
