import ctypes
import bornagain as ba
from GratingBase import GratingBase
from bornagain import nm, deg
import utils


class SphericalGrating(GratingBase):
    def __init__(self):
        GratingBase.__init__(self)

        self.m_grating_height = ctypes.c_double(225*nm)
        self.registerParameter("grating_height", ctypes.addressof(self.m_grating_height))

        self.m_grating_bulk = ctypes.c_double(100.0*nm)
        self.registerParameter("grating_bulk", ctypes.addressof(self.m_grating_bulk))

        self.m_nslices = ctypes.c_double(50.0)
        self.registerParameter("nslices", ctypes.addressof(self.m_nslices))

    def grating_height(self):
        return self.m_grating_height.value

    def grating_width(self):
        return self.m_grating_with.value

    def grating_bulk(self):
        return self.m_grating_bulk.value

    def grating(self):
        grshape = utils.GratingShape(period = self.grating_period(), grating_length=self.grating_length(), thickness=self.grating_bulk(), nslices=int(self.m_nslices.value))
        return grshape.get_composition(self.grating_material())

    def buildSample(self):
        layout = ba.ParticleLayout()
        layout.addParticle(self.grating(), 1.0, ba.kvector_t(0.0, 0.0, 100.0), ba.RotationZ(self.rotation_angle()))
        layout.setTotalParticleSurfaceDensity(0.05)
        layout.setInterferenceFunction(self.interference())

        # assemble layers
        air_layer = ba.Layer(self.ambience_material())
        air_layer.addLayout(layout)
        substrate_layer = ba.Layer(self.substrate_material())

        gold_layer = ba.Layer(self.grating_material(), self.grating_bulk()+self.grating_height())

        emulsion_layer = ba.Layer(self.ambience_material(), 200.0*nm)

        roughness = ba.LayerRoughness()
        roughness.setSigma(25.0*nm)
        roughness.setHurstParameter(0.5)
        roughness.setLatteralCorrLength(10.0*nm)

        # assemble multilayer
        multi_layer = ba.MultiLayer()
        multi_layer.addLayer(air_layer)
        # multi_layer.addLayerWithTopRoughness(gold_layer, roughness)
        # multi_layer.addLayerWithTopRoughness(emulsion_layer, roughness)
        multi_layer.addLayerWithTopRoughness(substrate_layer, roughness)

        return multi_layer
