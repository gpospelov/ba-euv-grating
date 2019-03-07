"""
Spherical grating. A collection of thing box slices mimicking
three-spheres-shape-like profile grating.
"""
import bornagain as ba
from grating_base import GratingBase
from bornagain import nm, deg
from utils.grating_shape import GratingShape
from utils.json_utils import load_sample_setup


class SphericalGrating(GratingBase):
    def __init__(self, setup):
        super().__init__()
        self.m_grating_height = 225*nm
        self.m_grating_bulk = 100.0*nm
        self.m_nslices = 50.0

    def grating_height(self):
        return self.m_grating_height

    def grating_bulk(self):
        return self.m_grating_bulk

    def grating(self):
        grshape = GratingShape(period=self.grating_period(),
                                     grating_length=self.grating_length(),
                                     thickness=self.grating_bulk(),
                                     nslices=int(self.m_nslices))
        return grshape.get_composition(self.grating_material())

    def buildSample(self, wavelength):
        layout = ba.ParticleLayout()
        layout.addParticle(self.grating(), 1.0,
                           ba.kvector_t(0.0, 0.0, 100.0),
                           ba.RotationZ(self.rotation_angle()))
        layout.setTotalParticleSurfaceDensity(0.05)
        layout.setInterferenceFunction(self.interference())

        # assemble layers
        air_layer = ba.Layer(self.ambience_material())
        air_layer.addLayout(layout)
        substrate_layer = ba.Layer(self.substrate_material())

        roughness = ba.LayerRoughness()
        roughness.setSigma(5.0*nm)
        roughness.setHurstParameter(0.5)
        roughness.setLatteralCorrLength(10.0*nm)

        # assemble multilayer
        multi_layer = ba.MultiLayer()
        multi_layer.addLayer(air_layer)
        multi_layer.addLayerWithTopRoughness(substrate_layer, roughness)

        return multi_layer


def get_sample():
    sample_config = load_sample_setup("spherical")
    return SphericalGrating(sample_config).buildSample(1.0)