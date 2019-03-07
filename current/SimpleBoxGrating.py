import bornagain as ba
from bornagain import nm, deg
from material_library import MaterialLibrary


class SimpleBoxGrating:
    def __init__(self, setup):
        super().__init__()
        self.m_grating_period = setup["period"]
        self.m_grating_length = setup["length"]
        self.m_grating_height = setup["height"]
        self.m_grating_width = setup["width"]
        self.m_rotation_angle = setup["rotation"]
        self.m_decay_length = setup["decay_length"]
        self.materials = MaterialLibrary()

    def add_parameters(self, run_parameters):
        run_parameters.add_parameters(self)

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

    def buildSample(self, wavelength):
        mat_ambience = self.materials.ambience_material(wavelength)
        mat_substrate = self.materials.substrate_material(wavelength)
        mat_grating = self.materials.grating_material(wavelength)

        layout = ba.ParticleLayout()
        layout.addParticle(self.grating(mat_grating), 1.0,
                           ba.kvector_t(0.0, 0.0, -self.grating_height()),
                           ba.RotationZ(self.m_rotation_angle))
        layout.setInterferenceFunction(self.interference())
        layout.setTotalParticleSurfaceDensity(2)

        # assemble layers
        air_layer = ba.Layer(mat_ambience)
        intermediate = ba.Layer(mat_ambience, self.grating_height())
        under = ba.Layer(mat_ambience, 100*nm)
        substrate_layer = ba.Layer(mat_substrate)

        intermediate.addLayout(layout)

        roughness = ba.LayerRoughness()
        roughness.setSigma(5.0*nm)
        roughness.setHurstParameter(0.5)
        roughness.setLatteralCorrLength(10.0*nm)

        # assemble multilayer
        multi_layer = ba.MultiLayer()
        multi_layer.addLayer(air_layer)
        multi_layer.addLayer(intermediate)
        multi_layer.addLayer(under)
        multi_layer.addLayerWithTopRoughness(substrate_layer, roughness)
        return multi_layer
