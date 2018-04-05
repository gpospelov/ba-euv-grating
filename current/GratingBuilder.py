import bornagain as ba
from bornagain import deg, micrometer, nm
import ctypes


class GratingBuilder(ba.IMultiLayerBuilder):
    """

    """
    def __init__(self):
        ba.IMultiLayerBuilder.__init__(self)

        self.m_grating_length = ctypes.c_double(5.0*micrometer)
        self.m_grating_period = ctypes.c_double(814*nm)
        self.m_grating_height = ctypes.c_double(200*nm)
        self.m_grating_bulk = ctypes.c_double(200*nm)
        self.m_rotation_angle = ctypes.c_double(0.0)  # 90.0 - perpendicular to grating
        self.m_emulsion_layer_thickness = ctypes.c_double(100.0*nm)
        self.m_substrate = None
        self.m_grating = None
        self.m_ambience = None

        self.m_decay_length = ctypes.c_double(2200.*nm)
        self.m_decay_function_type = "gauss"
        self.m_grating_type = "box"

        self.registerParameter("grating_length", ctypes.addressof(self.m_grating_length))
        self.registerParameter("grating_period", ctypes.addressof(self.m_grating_period))
        self.registerParameter("grating_height", ctypes.addressof(self.m_grating_height))
        self.registerParameter("rotation_angle", ctypes.addressof(self.m_rotation_angle))
        self.registerParameter("decay_length", ctypes.addressof(self.m_decay_length))

        self.init_materials()

    def print(self):
        for p in self.parameters():
            print("{:25} : {:30}".format(p[0], p[1]))

    def parameters(self):
        result = []
        result.append(("grating type", "{0}".format(self.m_grating_type)))
        result.append(("grating length", "{0}".format(self.grating_length())))
        result.append(("grating period", "{0}".format(self.grating_period())))
        result.append(("grating height", "{0}".format(self.grating_height())))
        result.append(("rotation angle", "{0}".format(self.rotation_angle()/deg)))
        result.append(("decay function", "{0}".format(self.m_decay_function_type)))
        result.append(("decay length", "{0}".format(self.decay_length())))
        return result

    def grating_length(self):
        return self.m_grating_length.value

    def grating_period(self):
        return self.m_grating_period.value

    def grating_height(self):
        return self.m_grating_height.value

    def grating_bulk(self):
        return self.m_grating_bulk.value

    def rotation_angle(self):
        return self.m_rotation_angle.value

    def decay_length(self):
        return self.m_decay_length.value

    def init_materials(self):
        self.m_ambience = ba.HomogeneousMaterial("Air", 0.0, 0.0)
        self.m_substrate = ba.HomogeneousMaterial("Substrate",  0.00111570884, 0.0018275599)  # Si
        self.m_grating = ba.HomogeneousMaterial("Particle",  0.101456583, 0.0521341525)  # Au
        self.m_poly = ba.HomogeneousMaterial("Polycarbonat",  0.0234414786, 0.00490225013)  #

    def box_grating(self, material = None):
        if not material:
            material = self.m_grating
        #ff = ba.FormFactorBox(self.grating_length(), 0.25*self.grating_period(), self.grating_height())
        ff = ba.FormFactorLongBoxLorentz(self.grating_length(), 0.05*self.grating_period(), self.grating_height())
        #ff = ba.FormFactorLongBoxGauss(self.grating_length(), 0.25*self.grating_period(), self.grating_height())
        return ba.Particle(material, ff)

    def box_composition(self):
        composition = ba.ParticleComposition()
        composition.addParticle(self.box_grating(self.m_grating), ba.kvector_t(0, 0, 0))
        composition.addParticle(self.box_grating(self.m_poly), ba.kvector_t(0, 0, -(self.grating_height()+self.grating_bulk())))
        # box1 = ba.Particle(self.m_grating, ba.FormFactorLongBoxLorentz(self.grating_length(), 0.05*self.grating_period(), self.grating_height()))
        # composition.addParticle(box1, ba.kvector_t(0., 0., self.grating_bulk()))
        # box2 = ba.Particle(self.m_grating, ba.FormFactorLongBoxLorentz(self.grating_length(), self.grating_period(), self.grating_bulk()))
        # composition.addParticle(box2, ba.kvector_t(0., 0., 0))
        return composition

    def sinusoidal_grating(self, material = None):
        if not material:
            material = self.m_grating
        #ff = ba.FormFactorRipple1(self.grating_length(), self.grating_period(), self.grating_height())
        ff = ba.FormFactorLongRipple1Lorentz(self.grating_length(), self.grating_period(), self.grating_height())
        #ff = ba.FormFactorLongRipple1Gauss(self.grating_length(), self.grating_period(), self.grating_height())
        return ba.Particle(material, ff)

    def sinusoidal_composition(self):
        composition = ba.ParticleComposition()
        composition.addParticle(self.sinusoidal_grating(self.m_grating), ba.kvector_t(0, 0, 0))
        composition.addParticle(self.sinusoidal_grating(self.m_poly), ba.kvector_t(0, 0, -(self.grating_height()+self.grating_bulk())))
        return composition

    def get_grating(self):
        if self.m_grating_type == "box":
            return self.box_grating()
        elif self.m_grating_type == "box_composition":
            return self.box_composition()
        elif self.m_grating_type == "sinusoidal":
            return self.sinusoidal_grating()
        elif self.m_grating_type == "sinusoidal_composition":
            return self.sinusoidal_composition()
        else :
            raise Exception("Unknown grating type")


    def get_decay_function(self):
        if self.m_decay_function_type == "gauss":
            return ba.FTDecayFunction1DGauss(self.decay_length())
        else:
            raise Exception("Unknown decay function type")


    def buildSample(self):
        particle_layout = ba.ParticleLayout()
        particle_layout.addParticle(self.get_grating(), 1.0, ba.kvector_t(0.0, 0.0, 0.0), ba.RotationZ(self.rotation_angle()))

        # interference function
        interference = ba.InterferenceFunction1DLattice(self.grating_period(), 90.0*deg - self.rotation_angle())
        interference.setDecayFunction(self.get_decay_function())
        particle_layout.setInterferenceFunction(interference)

        # assemble layers
        air_layer = ba.Layer(self.m_ambience)
        air_layer.addLayout(particle_layout)
        substrate_layer = ba.Layer(self.m_substrate)

        gold_layer = ba.Layer(self.m_grating, self.grating_bulk()+self.grating_height())

        emulsion_layer = ba.Layer(self.m_poly, self.m_emulsion_layer_thickness.value)

        roughness = ba.LayerRoughness()
        roughness.setSigma(25.0*nm)
        roughness.setHurstParameter(0.5)
        roughness.setLatteralCorrLength(10.0*nm)

        # assemble multilayer
        multi_layer = ba.MultiLayer()
        multi_layer.addLayer(air_layer)
        multi_layer.addLayerWithTopRoughness(gold_layer, roughness)
        multi_layer.addLayerWithTopRoughness(emulsion_layer, roughness)
        multi_layer.addLayerWithTopRoughness(substrate_layer, roughness)
        return multi_layer


def get_sample():
    builder = GratingBuilder()
    return builder.buildSample()