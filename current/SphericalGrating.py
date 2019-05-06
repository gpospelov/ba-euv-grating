"""
Spherical grating. A collection of thing box slices mimicking
three-spheres-shape-like profile grating.
"""
import bornagain as ba
from bornagain import nm, deg
from grating_shape import GratingShape
from utils.json_utils import load_sample_setup
from grating_base import GratingBase


class SphericalGrating(GratingBase):
    def __init__(self, exp_setup, sample_setup):
        super().__init__(exp_setup, sample_setup)
        self.m_grating_period = sample_setup["grating_period"]
        self.m_grating_length = sample_setup["length"]
        self.m_rough_sigma = sample_setup["r_sigma"]
        self.m_rough_hurst = sample_setup["r_hurst"]
        self.m_rough_corr = sample_setup["r_corr"]
        self.m_surface_density = sample_setup["surface_density"]
        self.m_grating_shape = GratingShape(sample_setup)
        self.init_interference(sample_setup["interf"])

    def grating_length(self):
        return self.m_grating_length

    def grating_period(self):
        return self.m_grating_period

    def grating(self, material):
        return self.m_grating_shape.get_composition(material)

    def buildSample(self, wavelength):
        mat_ambience = self.ambience_material(wavelength)
        mat_substrate = self.substrate_material(wavelength)
        mat_grating = self.grating_material(wavelength)

        layout = ba.ParticleLayout()
        layout.addParticle(self.grating(mat_grating), 1.0,
                           ba.kvector_t(0.0, 0.0, 0.0),
                           ba.RotationZ(self.rotation_angle()))
        layout.setTotalParticleSurfaceDensity(self.m_surface_density)
        layout.setInterferenceFunction(self.interference())

        # assemble layers
        air_layer = ba.Layer(mat_ambience)
        air_layer.addLayout(layout)
        substrate_layer = ba.Layer(mat_substrate)

        roughness = ba.LayerRoughness()
        roughness.setSigma(self.m_rough_sigma)
        roughness.setHurstParameter(self.m_rough_hurst)
        roughness.setLatteralCorrLength(self.m_rough_corr)

        # assemble multilayer
        multi_layer = ba.MultiLayer()
        multi_layer.addLayer(air_layer)
        multi_layer.addLayerWithTopRoughness(substrate_layer, roughness)

        return multi_layer


def get_sample():
    sample_config = load_sample_setup("spherical")
    return SphericalGrating(sample_config).buildSample(1.0)