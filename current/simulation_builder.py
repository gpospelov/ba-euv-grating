from bornagain import deg, nm
from BeamData import beam_data
import bornagain as ba
from utils.parameter_utils import RunParameters
from bornagain import deg, micrometer, nm
from SimpleBoxGrating import SimpleBoxGrating
from SimpleSinusGrating import SimpleSinusGrating
from BoxCompositionGrating import BoxCompositionGrating
from SphericalGrating import SphericalGrating
from detector_builder import DetectorBuilder
from SinusCompositionGrating import SinusCompositionGrating
import time

builders = {
    "SimpleBoxGrating": SimpleBoxGrating,
    "SimpleSinusGrating": SimpleSinusGrating,
    "SphericalGrating": SphericalGrating,
    "SinusCompositionGrating": SinusCompositionGrating
}

class DivergenceData:
    FLAG, TYPE, NPOINTS, SIGMA = range(4)


class SimulationBuilder:
    def __init__(self, exp_config, sample_config):

        self.m_alpha_inc = exp_config["alpha_inc"]
        self.m_phi_inc = 0
        self.m_beam_intensity = exp_config["intensity"]
        self.m_wavelength = exp_config["wavelength"]*nm
        self.m_detector_resolution_sigma = 0.02
        self.m_constant_background = exp_config["background"]

        self.m_beam_data_str = ""

        self.m_monte_carlo = False
        self.m_beam_divergence_alpha = (False, "gauss", 5, 0.05)
        self.m_beam_divergence_phi = (False, "gauss", 5, 0.05)
        self.m_time_spend = 0

        self.m_detector_builder = DetectorBuilder(exp_config)
        self.m_simulation = None

        self.m_sample_builder = builders[sample_config["builder"]](exp_config, sample_config)

        self.init_simulation()

    def alpha_inc(self):
        return self.m_alpha_inc*deg

    def phi_inc(self):
        return self.m_phi_inc

    def wavelength(self):
        return self.m_wavelength

    def get_run_parameters(self):
        result = RunParameters()
        result.add_parameters(self)
        self.m_detector_builder.add_parameters(result)
        self.m_sample_builder.add_parameters(result)
        return result

    def parameter_tuple(self):
        """
        Return RunParameters representing all registered parameter of 'self' and
        other children.
        """
        return self.get_run_parameters().parameter_tuple()

    def get_distribution(self, type, par1, par2):
        if type == "gauss":
            return  ba.DistributionGaussian(par1, par2)
        else:
            raise Exception("Unknown distribution type")

    def build_simulation(self):
        simulation = ba.GISASSimulation()
        simulation.setTerminalProgressMonitor()

        simulation.setDetector(self.m_detector_builder.create_detector())
        simulation.setBeamParameters(self.wavelength(), self.alpha_inc(), self.phi_inc())
        simulation.setBeamIntensity(self.m_beam_intensity)

        simulation.setDetectorResolutionFunction(ba.ResolutionFunction2DGaussian(self.m_detector_resolution_sigma*deg, self.m_detector_resolution_sigma*deg))
        simulation.setBackground(ba.ConstantBackground(self.m_constant_background))

        self.m_detector_builder.apply_masks(simulation)
        simulation.getOptions().setIncludeSpecular(True)

        if self.m_monte_carlo:
            simulation.getOptions().setMonteCarloIntegration(True, 50)

        d = self.m_beam_divergence_alpha
        if d[DivergenceData.FLAG]:
            distr = self.get_distribution(d[DivergenceData.TYPE], self.alpha_inc(), d[DivergenceData.SIGMA]*deg)
            simulation.addParameterDistribution("*/Beam/InclinationAngle", distr, d[DivergenceData.NPOINTS])

        d = self.m_beam_divergence_phi
        if d[DivergenceData.FLAG]:
            d = self.m_beam_divergence_phi
            distr = self.get_distribution(d[DivergenceData.TYPE], self.phi_inc(), d[DivergenceData.SIGMA]*deg)
            simulation.addParameterDistribution("*/Beam/AzimuthalAngle", distr, d[DivergenceData.NPOINTS])

        return simulation

    def init_simulation(self):
        self.m_simulation = self.build_simulation()

    def run_simulation(self):
        start = time.time()
        self.m_beam_data_str += "({:5.2f},{:5.2f})".format(self.wavelength(), 1.0)

        self.m_simulation = self.build_simulation()
        self.m_simulation.setSample(self.m_sample_builder.buildSample(self.wavelength()))

        print(self.get_run_parameters().parameter_string())

        self.m_simulation.runSimulation()

        self.m_time_spend = time.time() - start

        return self.m_simulation.result()

    def experimentalData(self):
        """
        Returns experimental data in same units as simulated data.
        """
        data = self.m_detector_builder.get_histogram().array()
        return ba.ConvertData(self.m_simulation, data)

