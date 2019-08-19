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
from detector_builder import PIXEL_SIZE
from SinusCompositionGrating import SinusCompositionGrating
from SinusShellGrating import SinusShellGrating
import time

builders = {
    "SimpleBoxGrating": SimpleBoxGrating,
    "SimpleSinusGrating": SimpleSinusGrating,
    "SphericalGrating": SphericalGrating,
    "SinusCompositionGrating": SinusCompositionGrating,
    "SinusShellGrating": SinusShellGrating
}

class DivergenceData:
    FLAG, TYPE, NPOINTS, SIGMA = range(4)


class SimulationBuilder:
    def __init__(self, exp_config, sample_config):
        self.m_alpha_inc = exp_config["alpha_inc"]
        self.m_phi_inc = 0
        self.m_beam_intensity = exp_config["intensity"]
        self.m_wavelength = exp_config["wavelength"]*nm
        self.sim_weight = 1.0
        self.m_resolution_sigma_factor = exp_config["det_sigma_factor"]
        self.m_constant_background = exp_config["background"]
        self.m_beam_data_str = ""
        self.m_monte_carlo = False
        self.m_beam_divergence_alpha = (False, "gauss", 5, 0.05)
        self.m_beam_divergence_phi = (False, "gauss", 5, 0.05)
        self.m_time_spend = 0
        self.m_detector_builder = DetectorBuilder(exp_config)
        self.m_sample_builder = builders[sample_config["builder"]](exp_config, sample_config)
        self.m_wl_use = exp_config["wl_use"]
        self.wl_data = exp_config["wl_data"]
        self.wl_weight = exp_config["wl_weight"]
        self.wl_sel = exp_config["wl_sel"]

    def detector_resolution_sigma(self):
        return PIXEL_SIZE*self.m_resolution_sigma_factor

    def alpha_inc(self):
        return self.m_alpha_inc*deg

    def phi_inc(self):
        return self.m_phi_inc

    def wavelength(self):
        return self.m_wavelength

    def wavelength_weight(self):
        return self.sim_weight

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
            return ba.DistributionGaussian(par1, par2)
        else:
            raise Exception("Unknown distribution type")

    def build_simulation(self):
        simulation = ba.GISASSimulation()
        # simulation.setTerminalProgressMonitor()

        simulation.setDetector(self.m_detector_builder.create_detector())
        simulation.setBeamParameters(self.wavelength(), self.alpha_inc(), self.phi_inc())
        simulation.setBeamIntensity(self.m_beam_intensity)

        simulation.setDetectorResolutionFunction(ba.ResolutionFunction2DGaussian(self.detector_resolution_sigma(), self.detector_resolution_sigma()))
        simulation.setBackground(ba.ConstantBackground(self.m_constant_background))

        self.m_detector_builder.apply_masks(simulation)

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

        simulation.setSample(self.m_sample_builder.buildSample(self.wavelength()))
        return simulation

    def run_single_simulation(self):
        start = time.time()
        self.m_beam_data_str += "({:5.2f},{:5.2f})".format(self.wavelength(), self.wavelength_weight())

        simulation = self.build_simulation()
        print(self.get_run_parameters().parameter_string())

        simulation.runSimulation()

        self.m_time_spend = time.time() - start

        print("time", self.m_time_spend)

        return simulation.result()

    def run_simulation(self):
        if self.m_wl_use:
            return self.run_simulation_pack()
        else:
            return self.run_single_simulation()

    def get_wl_data(self):
        """
        Calculates pair of (wavelength, weight)
        """
        sum = 0.0
        for index in self.wl_sel:
            sum += self.wl_weight[index]
        result = []
        for index in self.wl_sel:
            result.append((self.wl_data[index], self.wl_weight[index] / sum))
        return result

    def run_simulation_pack(self):
        sim_results = []
        wld = self.get_wl_data()
        for wd in wld:
            self.m_wavelength = wd[0]
            self.sim_weight = wd[1]
            sim_results.append(self.run_single_simulation())

        output = sim_results[0]
        print("AAA", wld)
        for index in range(0, output.size()):
            sum = 0.0
            nsim=0
            for sim in sim_results:
                sum += sim[index]*wld[nsim][1]
                ++nsim
            output[index] = sum

        # for i in range(0, data.size()):
        #     data[i] = data[i]*100

        return output

    # def run_simulation(self, wavelength=13.52 * nm, weight=1.0):
    #     self.m_beam_data_str += "({:5.2f},{:5.2f})".format(wavelength, weight)
    #     simulation = self.build_simulation(wavelength)
    #     simulation.setSampleBuilder(self.m_sample_builder)
    #     simulation.runSimulation()
    #     return simulation.result().histogram2d()
    #
    # def run(self):
    #     self.init_workspace()
    #
    #     start = time.time()
    #
    #     sum_hist = None
    #
    #     self.m_beam_data_str = ""
    #     # for b in beam_data():
    #     #     wavelength = b[0]
    #     #     weight = b[1]
    #     #     result = self.run_simulation(wavelength, weight)
    #     #     if not sum_hist:
    #     #         sum_hist = result
    #     #     else:
    #     #         add_to_histogram(sum_hist, result, weight)
    #
    #     sum_hist = self.run_simulation()
    #
    #     end = time.time()
    #     self.m_time_spend = end - start
    #
    #     return sum_hist

    def experimentalData(self):
        """
        Returns experimental data in same units as simulated data.
        """
        data = self.m_detector_builder.get_histogram().array()
        simulation = self.build_simulation()
        return ba.ConvertData(simulation, data)

