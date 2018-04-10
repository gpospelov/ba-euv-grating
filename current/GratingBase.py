"""
Base class for all grating builders
"""
import bornagain as ba
import ctypes
from bornagain import nm, deg, micrometer


class GratingBase(ba.IMultiLayerBuilder):
    def __init__(self):
        ba.IMultiLayerBuilder.__init__(self)

        self.m_grating_length = ctypes.c_double(5.0*micrometer)
        self.m_grating_period = ctypes.c_double(833*nm)

        self.m_decay_length = ctypes.c_double(2200.*nm)
        self.m_rotation_angle = ctypes.c_double(0.0*deg)  # 90.0 - beam is perpendicular to grating lines

        self.registerParameter("grating_length", ctypes.addressof(self.m_grating_length))
        self.registerParameter("grating_period", ctypes.addressof(self.m_grating_period))

        self.registerParameter("decay_length", ctypes.addressof(self.m_decay_length))
        self.registerParameter("rotation_angle", ctypes.addressof(self.m_rotation_angle))

    def grating_length(self):
        return self.m_grating_length.value

    def grating_period(self):
        return self.m_grating_period.value

    def decay_length(self):
        return self.m_decay_length.value

    def rotation_angle(self):
        return self.m_rotation_angle.value

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

    def decay_function(self, decay_type="gauss"):
        if decay_type == "gauss":
            return ba.FTDecayFunction1DGauss(self.decay_length())
        else:
            raise Exception("Unknown decay function type")

    def interference(self):
        interference = ba.InterferenceFunction1DLattice(self.grating_period(), 90.0*deg - self.rotation_angle())
        interference.setDecayFunction(self.decay_function())
        return interference

    def parameters(self):
        result = []
        pool = self.parameterPool()
        names = pool.parameterNames()
        for i in range(0, len(names)):
            value = pool.parameter(names[i]).value()
            result.append((names[i], "{0}".format(value)))
        return result
