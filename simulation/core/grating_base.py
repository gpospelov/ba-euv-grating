"""
Base class for all grating builders.
"""
import bornagain as ba
from bornagain import deg
from .material_library import MaterialLibrary


class GratingBase:
    def __init__(self, exp_setup, sample_setup):
        self.m_rotation_angle = exp_setup["sample_rotation"]
        self.material_library = MaterialLibrary()
        self.interference_function = None

    def grating_period(self):
        raise Exception("Raise not implemented")

    def rotation_angle(self):
        return self.m_rotation_angle*deg

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
        elif decay_type == "triangle":
            return ba.FTDecayFunction1DTriangle(decay_value)
        else:
            raise Exception("Unknown decay function type")

    def probability_distribution(self, distr_type, omega):
        if distr_type == "gauss":
            return ba.FTDistribution1DGauss(omega)
        elif distr_type == "gauss2d":
            return ba.FTDistribution2DGauss(omega, omega)
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

    def init_interference(self, interf_setup):
        self.m_interftype = interf_setup["type"]
        if interf_setup["type"] == "1dlattice":
            self.interference_function = ba.InterferenceFunction1DLattice(self.grating_period(), 90.0*deg - self.rotation_angle())
            self.m_decay_type = interf_setup["decay_type"]
            self.m_decay_length = interf_setup["decay_length"]
            self.interference_function.setDecayFunction(self.decay_function(self.m_decay_type, self.m_decay_length))
            self.interference_function.setPositionVariance(10.0)
        elif interf_setup["type"] == "1dpara":
            self.m_distr_type = interf_setup["distr_type"]
            self.m_damping_length = interf_setup["damping_length"]
            self.m_domain_size = interf_setup["domain_size"]
            self.m_omega = interf_setup["omega"]
            self.interference_function = ba.InterferenceFunctionRadialParaCrystal(self.grating_period(), self.m_damping_length)
            self.interference_function.setProbabilityDistribution(self.probability_distribution(self.m_distr_type, self.m_omega))
            if self.m_domain_size != 0.0:
                self.interference_function.setDomainSize(self.m_domain_size)
        elif interf_setup["type"] == "2dpara":
            self.m_distr_type = interf_setup["distr_type"]
            self.m_damping_length = interf_setup["damping_length"]
            self.m_domain_size = interf_setup["domain_size"]
            self.m_omega = interf_setup["omega"]
            self.interference_function = ba.InterferenceFunction2DParaCrystal.createHexagonal(self.grating_period(), self.m_damping_length, self.m_domain_size, self.m_domain_size)
            distr = self.probability_distribution(self.m_distr_type, self.m_omega)
            self.interference_function.setProbabilityDistributions(distr, distr)
        else:
            raise Exception("Unknown interference function")
