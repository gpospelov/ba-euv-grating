import bornagain as ba
from grating_base import GratingBase
from bornagain import nm, deg
from grating_base import GratingBase
from utils.json_utils import load_sample_setup
from utils.json_utils import load_experimental_setup


class SinusShellGrating(GratingBase):
    def __init__(self, exp_setup, sample_setup):
        super().__init__(exp_setup, sample_setup)
        self.m_grating_period = sample_setup["grating_period"]
        self.m_grating_length = sample_setup["length"]
        self.m_grating_height = sample_setup["grating_height"]
        self.m_grating_width = sample_setup["grating_width"]
        self.m_grating_bulk = sample_setup["grating_bulk"]
        self.m_rough_sigma = sample_setup["r_sigma"]
        self.m_rough_hurst = sample_setup["r_hurst"]
        self.m_rough_corr = sample_setup["r_corr"]
        self.m_surface_density = sample_setup["surface_density"]
        self.init_interference(sample_setup["interf"])

    def grating_height(self):
        return self.m_grating_height

    def grating_width(self):
        return self.m_grating_width

    def grating_length(self):
        return self.m_grating_length

    def grating_period(self):
        return self.m_grating_period

    def grating_bulk(self):
        return self.m_grating_bulk

    def grating(self, grating_material, air_material):
        composition = ba.ParticleComposition()

        sin_ff = ba.FormFactorLongRipple1Lorentz(self.grating_length(), self.grating_width(), self.grating_height())

        box_ff = ba.FormFactorLongBoxLorentz(self.grating_length(), self.grating_width(),
                                         self.grating_bulk())

        top_grating = ba.Particle(grating_material, sin_ff)
        box = ba.Particle(grating_material, box_ff)
        bottom_grating = ba.Particle(air_material, sin_ff)

        coreshell = ba.ParticleCoreShell(bottom_grating, box, ba.kvector_t(0.0, 0.0, 0.0))

        composition.addParticle(top_grating, ba.kvector_t(0.0, 0.0, self.grating_bulk()))
        composition.addParticle(coreshell, ba.kvector_t(0.0, 0.0, 0.0))

        return composition

    def buildSample(self, wavelength):
        mat_ambience = self.ambience_material(wavelength)
        mat_substrate = self.substrate_material(wavelength)
        mat_grating = self.grating_material(wavelength)

        interm_thickness = self.grating_height() + self.grating_bulk()

        layout = ba.ParticleLayout()
        layout.addParticle(self.grating(mat_grating, mat_ambience), 1.0,
                           ba.kvector_t(0.0, 0.0, -interm_thickness),
                           ba.RotationZ(self.rotation_angle()))
        layout.setInterferenceFunction(self.interference())
        layout.setTotalParticleSurfaceDensity(self.m_surface_density)

        # assemble layers
        air_layer = ba.Layer(mat_ambience)
        intermediate = ba.Layer(mat_ambience, interm_thickness)
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
        multi_layer.addLayerWithTopRoughness(substrate_layer, roughness)
        return multi_layer

def get_sample():
    exp_config = load_experimental_setup("exp2")
    sample_config = load_sample_setup("sinusshell")
    return SinusShellGrating(exp_config, sample_config).buildSample(1.0)

if __name__ == '__main__':
    get_sample()
