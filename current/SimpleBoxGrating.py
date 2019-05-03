import bornagain as ba
from bornagain import nm, deg
from material_library import MaterialLibrary
from utils.json_utils import load_sample_setup
from grating_base import GratingBase


class SimpleBoxGrating(GratingBase):
    def __init__(self, exp_setup, sample_setup):
        super().__init__(exp_setup, sample_setup)
        self.m_grating_period = sample_setup["period"]
        self.m_grating_length = sample_setup["length"]
        self.m_grating_height = sample_setup["height"]
        self.m_grating_width = sample_setup["width"]
        self.m_rough_sigma = sample_setup["r_sigma"]
        self.m_rough_hurst = sample_setup["r_hurst"]
        self.m_rough_corr = sample_setup["r_corr"]
        self.m_surface_density = sample_setup["surface_density"]
        self.init_interference(sample_setup["interf"])

    def init_interference(self, interf_setup):
        self.m_interftype = interf_setup["type"]
        if interf_setup["type"] == "1dlattice":
            self.interference_function = ba.InterferenceFunction1DLattice(self.m_grating_period, 90.0*deg - self.rotation_angle())
            self.m_decay_type = interf_setup["decay_type"]
            self.m_decay_length = interf_setup["decay_length"]
            self.interference_function.setDecayFunction(self.decay_function(self.m_decay_type, self.m_decay_length))
        elif interf_setup["type"] == "1dpara":
            self.m_distr_type = interf_setup["distr_type"]
            self.m_damping_length = interf_setup["damping_length"]
            self.m_domain_size = interf_setup["domain_size"]
            self.m_omega = interf_setup["omega"]
            self.interference_function = ba.InterferenceFunctionRadialParaCrystal(self.m_grating_period, self.m_damping_length)
            self.interference_function.setProbabilityDistribution(self.probability_distribution(self.m_distr_type, self.m_omega))
            if self.m_domain_size != 0.0:
                self.interference_function.setDomainSize(self.m_domain_size)
        else:
            raise Exception("Unknown interference function")

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

    def interference(self):
        # interference = ba.InterferenceFunction1DLattice(
        #     self.m_grating_period, 90.0*deg - self.rotation_angle())
        # interference.setDecayFunction(self.decay_function())

        # interference = ba.InterferenceFunctionRadialParaCrystal(
        #     self.m_grating_period, 1000 * nm)
        # pdf = ba.FTDistribution1DGauss(1 * nm)
        # interference.setProbabilityDistribution(pdf)
        # return interference
        #
        return self.interference_function

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
    sample_config = load_sample_setup("box")
    return SimpleBoxGrating(sample_config).buildSample(1.0)