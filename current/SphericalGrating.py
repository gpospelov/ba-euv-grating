"""
Spherical grating. A collection of thing box slices mimicking
three-spheres-shape-like profile grating.
"""
import bornagain as ba
from bornagain import nm, deg
from utils.grating_shape import GratingShape
from utils.json_utils import load_sample_setup
from material_library import MaterialLibrary


class SphericalGrating:
    def __init__(self, setup):
        self.m_grating_period = setup["period"]
        self.m_grating_length = setup["length"]
        self.m_grating_height = setup["height"]
        self.m_grating_width = setup["width"]
        self.m_rotation_angle = setup["rotation"]*deg
        self.m_decay_length = setup["decay_length"]
        self.m_rough_sigma = setup["r_sigma"]
        self.m_rough_hurst = setup["r_hurst"]
        self.m_rough_corr = setup["r_corr"]
        self.m_surface_density = setup["surface_density"]
        self.m_grating_bulk = setup["bulk"]*nm
        self.m_nslices = setup["nslices"]
        self.materials = MaterialLibrary()

    def add_parameters(self, run_parameters):
        run_parameters.add_parameters(self)

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

    def decay_function(self, decay_type="gauss"):
        if decay_type == "gauss":
            return ba.FTDecayFunction1DGauss(self.m_decay_length)
        else:
            raise Exception("Unknown decay function type")

    def interference(self):
        interference = ba.InterferenceFunction1DLattice(
            self.m_grating_period, 90.0*deg - self.m_rotation_angle)
        interference.setDecayFunction(self.decay_function())
        return interference

    def grating(self, material):
        grshape = GratingShape(period=self.grating_period(),
                                     grating_length=self.grating_length(),
                                     thickness=self.grating_bulk(),
                                     nslices=int(self.m_nslices))
        return grshape.get_composition(material)

    def buildSample(self, wavelength):
        mat_ambience = self.materials.ambience_material()
        mat_substrate = self.materials.substrate_material()
        mat_grating = self.materials.grating_material()

        layout = ba.ParticleLayout()
        layout.addParticle(self.grating(mat_grating), 1.0,
                           ba.kvector_t(0.0, 0.0, 100.0),
                           ba.RotationZ(self.m_rotation_angle))
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