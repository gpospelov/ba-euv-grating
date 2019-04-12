import bornagain as ba
from grating_base import GratingBase
from bornagain import nm, deg
from material_library import MaterialLibrary
from grating_base import GratingBase


class SimpleSinusGrating(GratingBase):
    def __init__(self, exp_setup, sample_setup):
        super().__init__(exp_setup, sample_setup)
        self.m_grating_period = sample_setup["period"]
        self.m_grating_length = sample_setup["length"]
        self.m_grating_height = sample_setup["height"]
        self.m_grating_width = sample_setup["width"]
        self.m_decay_length = sample_setup["decay_length"]
        self.m_rough_sigma = sample_setup["r_sigma"]
        self.m_rough_hurst = sample_setup["r_hurst"]
        self.m_rough_corr = sample_setup["r_corr"]
        self.m_surface_density = sample_setup["surface_density"]
        self.materials = MaterialLibrary()

    def grating_height(self):
        return self.m_grating_height

    def grating_width(self):
        return self.m_grating_width

    def grating_length(self):
        return self.m_grating_length

    def grating_period(self):
        return self.m_grating_period

    def grating(self, material):
        # ff = ba.FormFactorLongRipple1Lorentz(self.grating_length(), self.grating_width(), self.grating_height())
        ff = ba.FormFactorLongRipple1Gauss(self.grating_length(), self.grating_width(), self.grating_height())
        return ba.Particle(material, ff)

    def decay_function(self, decay_type="gauss"):
        if decay_type == "gauss":
            return ba.FTDecayFunction1DGauss(self.m_decay_length)
        else:
            raise Exception("Unknown decay function type")

    def interference(self):
        interference = ba.InterferenceFunction1DLattice(
            self.m_grating_period, 90.0*deg - self.rotation_angle())
        interference.setDecayFunction(self.decay_function())
        return interference

    def buildSample(self, wavelength):
        mat_ambience = self.materials.ambience_material()
        mat_substrate = self.materials.substrate_material()
        mat_grating = self.materials.grating_material()

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
