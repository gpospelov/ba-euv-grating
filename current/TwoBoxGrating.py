import ctypes
import bornagain as ba
from GratingBase import GratingBase
from bornagain import nm, deg


class TwoBoxGrating(GratingBase):
    def __init__(self):
        GratingBase.__init__(self)

        self.m_grating_height = ctypes.c_double(192*nm)
        self.registerParameter("grating_height", ctypes.addressof(self.m_grating_height))

        self.m_grating_with = ctypes.c_double(41.5*nm)
        self.m_grating_bulk = ctypes.c_double(100.0*nm)

    def grating_height(self):
        return self.m_grating_height.value

    def grating_width(self):
        return self.m_grating_with.value

    def grating_bulk(self):
        return self.m_grating_bulk.value

    def grating(self):
        ff = ba.FormFactorLongBoxLorentz(self.grating_length(), self.grating_width(), self.grating_height())
        topPart =  ba.Particle(self.grating_material(), ff)

        ff = ba.FormFactorLongBoxLorentz(self.grating_length(), self.grating_period(), self.grating_bulk())
        bottomPart =  ba.Particle(self.grating_material(), ff)

        composition = ba.ParticleComposition()
        composition.addParticle(topPart, ba.kvector_t(0, 0, self.grating_bulk()))
        composition.addParticle(topPart, ba.kvector_t(0, 0, 0))
        return composition


    def buildSample(self):
        layout = ba.ParticleLayout()
        layout.addParticle(self.grating(), 1.0, ba.kvector_t(0.0, 0.0, 0.0), ba.RotationZ(self.rotation_angle()))
        layout.setInterferenceFunction(self.interference())

        # assemble layers
        air_layer = ba.Layer(self.ambience_material())
        air_layer.addLayout(layout)
        substrate_layer = ba.Layer(self.substrate_material())

        roughness = ba.LayerRoughness()
        roughness.setSigma(25.0*nm)
        roughness.setHurstParameter(0.5)
        roughness.setLatteralCorrLength(10.0*nm)

        # assemble multilayer
        multi_layer = ba.MultiLayer()
        multi_layer.addLayer(air_layer)
        multi_layer.addLayerWithTopRoughness(substrate_layer, roughness)
        return multi_layer


if __name__ == '__main__':
    grating = TwoBoxGrating()
    print(grating.parametersToString())
