from bornagain import ba


class MaterialLibrary:
    def __init__(self):
        pass

    @staticmethod
    def ambience_material(wavelength=1.0):
        # no wavelength dependency for the moment
        return ba.HomogeneousMaterial("air", 0.0, 0.0)

    @staticmethod
    def substrate_material(wavelength=1.0):
        # no wavelength dependency for the moment
        return ba.HomogeneousMaterial("substrate",  0.00111570884, 0.0018275599)  # Si

    @staticmethod
    def grating_material(wavelength=1.0):
        # no wavelength dependency for the moment
        return ba.HomogeneousMaterial("grating",  0.101456583, 0.0521341525)  # Au

    @staticmethod
    def poly_material(wavelength=1.0):
        # no wavelength dependency for the moment
        return ba.HomogeneousMaterial("poly",  0.0234414786, 0.00490225013)  # something
