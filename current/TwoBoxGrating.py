import bornagain as ba
from grating_base import GratingBase
from bornagain import nm, deg


class TwoBoxGrating(GratingBase):
    def __init__(self):
        super().__init__()
        self.m_grating_height = 197*nm
        self.m_grating_with = 29.0*nm
        self.m_grating_bulk = 197.0*nm

    def grating_height(self):
        return self.m_grating_height

    def grating_width(self):
        return self.m_grating_with

    def grating_bulk(self):
        return self.m_grating_bulk

    def grating(self):
        ff = ba.FormFactorLongBoxLorentz(self.grating_length(),
                                         self.grating_width(),
                                         self.grating_height())
        topPart =  ba.Particle(self.grating_material(), ff)

        ff = ba.FormFactorLongBoxLorentz(self.grating_length(),
                                         self.grating_period(),
                                         self.grating_bulk())
        bottomPart =  ba.Particle(self.grating_material(), ff)

        composition = ba.ParticleComposition()
        composition.addParticle(topPart, ba.kvector_t(0, 0, self.grating_bulk()))
        composition.addParticle(bottomPart, ba.kvector_t(0, 0, 0))
        return composition


    def buildSample(self):
        layout = ba.ParticleLayout()
        layout.addParticle(self.grating(), 1.0, ba.kvector_t(0.0, 0.0, -(self.grating_bulk() + self.grating_height())), ba.RotationZ(self.rotation_angle()))
        layout.setInterferenceFunction(self.interference())
        # layout.setTotalParticleSurfaceDensity(1e-8)

        # assemble layers
        air_layer = ba.Layer(self.ambience_material())

        intermediate = ba.Layer(self.ambience_material(), self.grating_height() + self.grating_bulk())
        intermediate.addLayout(layout)

        under = ba.Layer(self.ambience_material(), 100*nm)
        substrate_layer = ba.Layer(self.substrate_material())

        roughness = ba.LayerRoughness()
        roughness.setSigma(5.0*nm)
        roughness.setHurstParameter(0.5)
        roughness.setLatteralCorrLength(10.0*nm)

        emulsion_layer = ba.Layer(self.ambience_material(), 200.0)

        # assemble multilayer
        multi_layer = ba.MultiLayer()
        multi_layer.addLayer(air_layer)
        multi_layer.addLayer(intermediate)
        multi_layer.addLayer(under)
        # multi_layer.addLayerWithTopRoughness(emulsion_layer, roughness)
        multi_layer.addLayerWithTopRoughness(substrate_layer, roughness)
        return multi_layer
