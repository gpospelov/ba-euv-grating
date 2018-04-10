from bornagain import deg, nm
from GratingBuilder import GratingBuilder
from DetectorBuilder import DetectorBuilder
from BeamData import beam_data
import bornagain as ba
from bornagain import deg, micrometer, nm
from histogram_utils import *
from SimpleBoxGrating import SimpleBoxGrating
from TwoBoxGrating import TwoBoxGrating
from SimpleSinusGrating import SimpleSinusGrating
import time
import glob
import os


class DivergenceData:
    FLAG, TYPE, NPOINTS, SIGMA = range(4)

class ParallelBuilder():
    def __init__(self, output_dir="output"):
        self.m_output_dir = output_dir
        self.m_output_index = 0

        self.m_title = "Box-grating: scanning grating period"
        self.m_alpha_inc = 10.71
        self.m_phi_inc = 0
        self.m_beam_intensity = 5e+4
        self.m_detector_resolution_sigma = 0.02
        self.m_constant_background = 5e+4

        # self.m_sample_builder = GratingBuilder()
        # self.m_sample_builder = SimpleBoxGrating()
        # self.m_sample_builder = TwoBoxGrating()
        self.m_sample_builder = SimpleSinusGrating()

        self.m_apply_detector_masks = True
        self.m_detector_masks = None
        self.m_beam_data_str = ""

        self.m_monte_carlo = False
        self.m_beam_divergence_alpha = (False, "gauss", 5, 0.05)
        self.m_beam_divergence_phi = (False, "gauss", 5, 0.05)
        self.m_time_spend = 0

    def parameters_str(self):
        pars = self.parameters()
        result = str()
        nrows, ncols = 7, 3
        for row in range(0, nrows):
            for col in range(0, ncols):
                ipar = row + nrows*col
                if ipar < len(pars):
                    result += "{:22} {:1} {:30}".format(pars[ipar][0], ":", pars[ipar][1])
                else:
                    result += " "*56
            result += "\n"
        return result

    def parameters(self):
        return self.m_sample_builder.parameters() + self.simul_parameters()

    def simul_parameters(self):
        result=[]
        result.append(("Inclination angle", "{0}".format(self.m_alpha_inc)))
        result.append(("Azimuthal angle", "{0}".format(self.m_phi_inc)))
        result.append(("Beam intensity", "{:g}".format(self.m_beam_intensity)))
        result.append(("Beam wavelength", "{0}".format(self.m_beam_data_str)))
        result.append(("Detector resolution", "{0}".format(self.m_detector_resolution_sigma)))
        result.append(("Constant background", "{:g}".format(self.m_constant_background)))
        result.append(("Beam div alpha", "{0}".format(self.m_beam_divergence_alpha)))
        result.append(("Beam div phi", "{0}".format(self.m_beam_divergence_phi)))
        result.append(("Montecarlo", "{0}".format(self.m_monte_carlo)))
        result.append(("Time", "{:-6.2f}".format(self.m_time_spend)))
        return result

    def get_distribution(self, type, par1, par2):
        if type == "gauss":
            return  ba.DistributionGaussian(par1, par2)
        else:
            raise Exception("Unknown distribution type")

    def build_simulation(self, wavelength):
        simulation = ba.GISASSimulation()
        simulation.setTerminalProgressMonitor()

        simulation.setDetector(DetectorBuilder().create_detector())
        simulation.setBeamParameters(wavelength, self.m_alpha_inc*deg, self.m_phi_inc*deg)
        simulation.setBeamIntensity(self.m_beam_intensity)

        simulation.setDetectorResolutionFunction(ba.ResolutionFunction2DGaussian(self.m_detector_resolution_sigma*deg, self.m_detector_resolution_sigma*deg))
        simulation.setBackground(ba.ConstantBackground(self.m_constant_background))

        if self.m_apply_detector_masks:
            DetectorBuilder().apply_masks(simulation)
            self.m_detector_masks = simulation.getInstrument().getDetectorMask().createHistogram()

        if self.m_monte_carlo:
            simulation.getOptions().setMonteCarloIntegration(True, 50)

        d = self.m_beam_divergence_alpha
        if d[DivergenceData.FLAG]:
            distr = self.get_distribution(d[DivergenceData.TYPE], self.m_alpha_inc*deg, d[DivergenceData.SIGMA]*deg)
            simulation.addParameterDistribution("*/Beam/InclinationAngle", distr, d[DivergenceData.NPOINTS])

        d = self.m_beam_divergence_phi
        if d[DivergenceData.FLAG]:
            d = self.m_beam_divergence_phi
            distr = self.get_distribution(d[DivergenceData.TYPE], self.m_phi_inc*deg, d[DivergenceData.SIGMA]*deg)
            simulation.addParameterDistribution("*/Beam/AzimuthalAngle", distr, d[DivergenceData.NPOINTS])

        print(simulation.parametersToString())

        return simulation

    def run_simulation(self, wavelength=13.52*nm, weight=1.0):
        self.m_beam_data_str += "({:5.2f},{:5.2f})".format(wavelength, weight)
        simulation = self.build_simulation(wavelength)
        simulation.setSampleBuilder(self.m_sample_builder)
        simulation.runSimulation()
        return simulation.result().histogram2d()

    def run(self):
        self.init_workspace()

        start = time.time()

        sum_hist = None

        self.m_beam_data_str = ""
        # for b in beam_data():
        #     wavelength = b[0]
        #     weight = b[1]
        #     result = self.run_simulation(wavelength, weight)
        #     if not sum_hist:
        #         sum_hist = result
        #     else:
        #         add_to_histogram(sum_hist, result, weight)

        sum_hist = self.run_simulation()

        end = time.time()
        self.m_time_spend = end - start

        return sum_hist

    def make_dir(self, dirname):
        if not os.path.exists(dirname):
            os.makedirs(dirname)

    def init_workspace(self):
        """
        Analyses output directory and finds index of last file
        """
        self.make_dir(self.m_output_dir)
        mdfiles = glob.glob(os.path.join(self.m_output_dir, '*.md'))
        nums = set()
        for f in mdfiles:
            parts = f.split("-")
            if len(parts) != 2:
                raise Exception("Can't parse the name")
            num = int(parts[1].split(".")[0])
            nums.add(num)
        self.m_output_index = 1
        if len(nums):
            self.m_output_index = list(nums)[-1] + 1

    def output_md(self):
        return '{}/run-{:02d}.md'.format(self.m_output_dir, self.m_output_index)

    def output_png_full(self):
        return '{}/run-{:02d}.png'.format(self.m_output_dir, self.m_output_index)

    def output_png(self):
        return 'run-{:02d}.png'.format(self.m_output_index)

    def write_report(self):
        print(self.output_md(), self.output_png())
        with open(self.output_md(), "w") as f:
            f.write("## {0}\n\n".format(self.m_title))
            f.write("Comment: \n\n")
            f.write("<pre>\n")
            f.write(self.parameters_str())
            f.write("</pre>\n")
            f.write("\n")
            f.write("![alt text]({0})\n\n".format(self.output_png()))
            f.write("<div style=\"page-break-after: always;\"></div>\n\n")
            f.write("\n")
        print(self.parameters_str())
