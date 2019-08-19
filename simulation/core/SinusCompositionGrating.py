import bornagain as ba
from .grating_base import GratingBase
from bornagain import nm, deg
from .grating_base import GratingBase
from .utils import load_setup


class SinusCompositionGrating(GratingBase):
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
        self.m_grating_bulk = sample_setup["grating_bulk"]
        self.init_interference(sample_setup["interf"])

    def grating_height(self):
        return self.m_grating_height

    def grating_width(self):
        return self.m_grating_width

    def grating_length(self):
        return self.m_grating_length

    def grating_period(self):
        return self.m_grating_period

    def grating(self, mat_top, mat_bottom):
        composition = ba.ParticleComposition()
        ff = ba.FormFactorLongRipple1Gauss(self.grating_length(), self.grating_width(), self.grating_height())
        top = ba.Particle(mat_top, ff)
        bottom = ba.Particle(mat_bottom, ff)
        composition.addParticle(top, ba.kvector_t(0.0, 0.0, self.m_grating_bulk))
        composition.addParticle(bottom, ba.kvector_t(0.0, 0.0, 0.0))
        return composition

    def buildSample(self, wavelength):
        mat_ambience = self.ambience_material(wavelength)
        mat_substrate = self.substrate_material(wavelength)
        mat_grating = self.grating_material(wavelength)

        layout = ba.ParticleLayout()
        layout.addParticle(self.grating(mat_grating, mat_ambience), 1.0,
                           ba.kvector_t(0.0, 0.0, -self.m_grating_bulk),
                           ba.RotationZ(self.rotation_angle()))
        layout.setInterferenceFunction(self.interference())
        layout.setTotalParticleSurfaceDensity(self.m_surface_density)

        # assemble layers
        air_layer = ba.Layer(mat_ambience)
        intermediate = ba.Layer(mat_grating, self.m_grating_bulk)
        # under = ba.Layer(mat_ambience, 10*nm)
        substrate_layer = ba.Layer(mat_substrate)

        intermediate.addLayout(layout)

        roughness = ba.LayerRoughness()
        roughness.setSigma(self.m_rough_sigma)
        roughness.setHurstParameter(self.m_rough_hurst)
        roughness.setLatteralCorrLength(self.m_rough_corr)

        # assemble multilayer
        multi_layer = ba.MultiLayer()
        multi_layer.addLayer(air_layer)
        multi_layer.addLayerWithTopRoughness(intermediate, roughness)
        # multi_layer.addLayer(under)
        multi_layer.addLayerWithTopRoughness(substrate_layer, roughness)
        return multi_layer


def get_sample():
    exp_config = load_setup("experiments.json", "exp3")
    sample_config = load_setup("gratings.json", "sinuscomp")
    return SinusCompositionGrating(exp_config, sample_config).buildSample(1.0)


if __name__ == '__main__':
    print(get_sample().treeToString())
