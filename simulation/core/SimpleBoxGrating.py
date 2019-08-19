import bornagain as ba
from bornagain import nm, deg
from .grating_base import GratingBase
from .utils import load_setup


class SimpleBoxGrating(GratingBase):
    def __init__(self, exp_setup, sample_setup):
        super().__init__(exp_setup, sample_setup)
        self.m_grating_period = sample_setup["grating_period"]
        self.m_grating_length = sample_setup["length"]
        self.m_grating_height = sample_setup["grating_height"]
        self.m_grating_width = sample_setup["grating_width"]
        self.m_rough_sigma = sample_setup["r_sigma"]
        self.m_rough_hurst = sample_setup["r_hurst"]
        self.m_rough_corr = sample_setup["r_corr"]
        self.m_surface_density = sample_setup["surface_density"]
        self.init_interference(sample_setup["interf"])

    def grating_period(self):
        return self.m_grating_period

    def grating_height(self):
        return self.m_grating_height

    def grating_width(self):
        return self.m_grating_width

    def grating_length(self):
        return self.m_grating_length

    def grating(self, material):
        ff = ba.FormFactorLongBoxLorentz(self.grating_length(), self.grating_width(),
                                         self.grating_height())
        return ba.Particle(material, ff)

    def buildSample(self, wavelength):
        mat_ambience = self.ambience_material(wavelength)
        mat_substrate = self.substrate_material(wavelength)
        mat_grating = self.grating_material(wavelength)

        layout = ba.ParticleLayout()
        layout.addParticle(self.grating(mat_grating), 1.0,
                           ba.kvector_t(0.0, 0.0, -self.grating_height()),
                           ba.RotationZ(self.rotation_angle()))
        layout.setInterferenceFunction(self.interference())
        layout.setTotalParticleSurfaceDensity(self.m_surface_density)

        # assemble layers
        air_layer = ba.Layer(mat_ambience)
        intermediate = ba.Layer(mat_ambience, self.grating_height())
        under = ba.Layer(mat_ambience, 100*nm)
        substrate_layer = ba.Layer(mat_substrate)

        intermediate.addLayout(layout)

        roughness = ba.LayerRoughness()
        roughness.setSigma(self.m_rough_sigma)
        roughness.setHurstParameter(self.m_rough_hurst)
        roughness.setLatteralCorrLength(self.m_rough_corr)

        # assemble multilayer
        multi_layer = ba.MultiLayer()
        multi_layer.addLayer(air_layer)
        multi_layer.addLayer(intermediate)
        multi_layer.addLayer(under)
        multi_layer.addLayerWithTopRoughness(substrate_layer, roughness)
        return multi_layer


def get_sample():
    sample_config = load_setup("gratings.json", "box")
    return SimpleBoxGrating(sample_config).buildSample(1.0)
