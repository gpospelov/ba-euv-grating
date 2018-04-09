import ctypes
import bornagain as ba
from GratingBase import GratingBase
from bornagain import nm, deg


class SimpleBoxGrating(GratingBase):
    def __init__(self):
        GratingBase.__init__(self)

        self.m_grating_height = ctypes.c_double(201*nm)
        self.registerParameter("grating_height", ctypes.addressof(self.m_grating_height))

        self.m_grating_with = ctypes.c_double(29*nm)
        self.registerParameter("grating_width", ctypes.addressof(self.m_grating_with))

    def grating_height(self):
        return self.m_grating_height.value

    def grating_width(self):
        return self.m_grating_with.value

    def grating(self):
        ff = ba.FormFactorLongBoxLorentz(self.grating_length(), self.grating_width(), self.grating_height())
        return ba.Particle(self.grating_material(), ff)

    def buildSample(self):
        layout = ba.ParticleLayout()
        layout.addParticle(self.grating(), 1.0, ba.kvector_t(0.0, 0.0, -self.grating_height()), ba.RotationZ(self.rotation_angle()))
        layout.setInterferenceFunction(self.interference())
        # layout.setTotalParticleSurfaceDensity(2e-6)

        # assemble layers
        air_layer = ba.Layer(self.ambience_material())
        intermediate = ba.Layer(self.ambience_material(), self.grating_height())
        under = ba.Layer(self.ambience_material(), 100*nm)
        substrate_layer = ba.Layer(self.substrate_material())

        intermediate.addLayout(layout)

        roughness = ba.LayerRoughness()
        roughness.setSigma(5.0*nm)
        roughness.setHurstParameter(0.5)
        roughness.setLatteralCorrLength(10.0*nm)

        # assemble multilayer
        multi_layer = ba.MultiLayer()
        multi_layer.addLayer(air_layer)
        multi_layer.addLayer(intermediate)
        multi_layer.addLayer(under)
        multi_layer.addLayerWithTopRoughness(substrate_layer, roughness)
        return multi_layer


if __name__ == '__main__':
    grating = SimpleBoxGrating()
    print(grating.parametersToString())
