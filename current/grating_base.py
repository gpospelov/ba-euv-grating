"""
Base class for all grating builders.
"""
import bornagain as ba
from bornagain import deg
from material_library import MaterialLibrary


class GratingBase:
    def __init__(self, exp_setup, sample_setup):
        self.m_rotation_angle = exp_setup["sample_rotation"]
        self.material_library = MaterialLibrary()
        self.interference_function = None

    def rotation_angle(self):
        return self.m_rotation_angle*deg

    def add_parameters(self, run_parameters):
        run_parameters.add_parameters(self)

    def ambience_material(self, wavelength):
        return self.material_library.get_air(wavelength)

    def substrate_material(self, wavelength):
        return self.material_library.get_si(wavelength)

    def grating_material(self, wavelength):
        return self.material_library.get_au(wavelength)

    def interference(self):
        return self.interference_function

    def decay_function(self, decay_type, decay_value):
        if decay_type == "gauss":
            return ba.FTDecayFunction1DGauss(decay_value)
        elif decay_type == "cauchy":
            return ba.FTDecayFunction1DCauchy(decay_value)
        else:
            raise Exception("Unknown decay function type")

    def probability_distribution(self, distr_type, omega):
        if distr_type == "gauss":
            return ba.FTDistribution1DGauss(omega)
        elif distr_type == "cauchy":
            return ba.FTDistribution1DCauchy(omega)
        elif distr_type == "gate":
            return ba.FTDistribution1DGate(omega)
        elif distr_type == "triangle":
            return ba.FTDistribution1DTriangle(omega)
        elif distr_type == "cosine":
            return ba.FTDistribution1DCosine(omega)
        else:
            raise Exception("Unknown distr function type")


