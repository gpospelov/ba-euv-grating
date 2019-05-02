"""
Base class for all grating builders.
"""
from bornagain import deg
from material_library import MaterialLibrary


class GratingBase:
    def __init__(self, exp_setup, sample_setup):
        self.m_rotation_angle = exp_setup["sample_rotation"]
        self.material_library = MaterialLibrary()

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
