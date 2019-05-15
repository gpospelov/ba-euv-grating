"""
Main script to run grating fitting.
"""
import bornagain as ba
from matplotlib import pyplot as plt
from simulation_builder import SimulationBuilder
from utils.json_utils import load_experimental_setup
from utils.json_utils import load_sample_setup
import numpy as np


EXPERIMENT_NAME = "exp3"
SAMPLE_NAME = "sinus"

class MyObjective(ba.FitObjective):
    """
    FitObjective extension for custom fitting metric.
    """
    def __init__(self):
        super(MyObjective, self).__init__()

    def evaluate_residuals(self, params):
        """
        Provides custom calculation of vector of residuals
        """
        # calling parent's evaluate functions to run simulations
        super(MyObjective, self).evaluate(params)

        # accessing simulated and experimental data as flat numpy arrays
        # applying sqrt to every element

        sim = np.log10(np.asarray(self.simulation_array()))
        exp = np.log10(np.asarray(self.experimental_array()))
        sim[np.isneginf(sim)] = 0
        exp[np.isneginf(exp)] = 0

        res = sim-exp
        print(np.min(res), np.max(res))

        # res = np.zeros_like(sim)
        # for s, e in zip(sim, exp):
        #
        #

        # sim = np.ma.log(sim)
        # exp = np.ma.log(exp)
        # print(len(sim), sim)
        # print(len(exp), exp)
        #
        # print(np.max(sim-exp), np.min(sim-exp))
        # print(len(sim-exp), sim-exp)

        # return vector of residuals
        return res


def get_simulation(params):
    exp_config = load_experimental_setup(EXPERIMENT_NAME)
    sample_config = load_sample_setup(SAMPLE_NAME)

    exp_config["sample_rotation"] = params["sample_rotation"]
    # exp_config["det_dx"] = params["det_dx"]
    # exp_config["beta_b"] = params["beta_b"]
    # exp_config["intensity"] = exp_config["intensity"]*params["intensity_coeff"]

    sample_config["grating_period"] = params["grating_period"]
    sample_config["grating_width"] = params["grating_period"]
    sample_config["grating_height"] = params["grating_height"]
    # sample_config["grating_bulk"] = params["grating_bulk"]

    # sample_config["r0"] = params["r0"]
    # sample_config["r1"] = params["r1"]
    # sample_config["bulk"] = params["bulk"]
    # sample_config["surface_density"] = sample_config["surface_density"]*params["surface_density_coeff"]

    builder = SimulationBuilder(exp_config, sample_config)

    # builder.m_sample_builder.m_rotation_angle = params["sample_rotation"]
    # # builder.m_detector_builder.m_beta_b = params["beta_b"]
    # # builder.m_detector_builder.m_det_dx = params["det_dx"]
    # builder.m_sample_builder.m_grating_period = params["grating_period"]
    return builder.build_simulation()


def run_fitting():

    exp_config = load_experimental_setup(EXPERIMENT_NAME)
    sample_config = load_sample_setup(SAMPLE_NAME)
    builder = SimulationBuilder(exp_config, sample_config)

    fit_objective = ba.FitObjective()
    fit_objective.addSimulationAndData(get_simulation, builder.experimentalData().array())

    fit_objective.initPrint(1)
    fit_objective.initPlot(1)

    params = ba.Parameters()
    params.add("sample_rotation", 0.15, min=0.0, max=0.3, step=0.01)
    # params.add("det_dx", 0.00225, min=0.00225-0.005, max=0.00225+0.005, step=0.0005)
    # params.add("beta_b", 72.12, min=72.12-5.0, max=72.12+5.0, step=0.5)
    params.add("grating_height", 225, min=225-75.0, max=225+75.0, step=2.0)

    params.add("grating_period", 834.2, min=834.2-3.0, max=834.2+3.0, step=0.1)
    # params.add("grating_bulk", 400, min=200.0, max=500, step=10.0)
    # params.add("r0", 225, min=225-12.0, max=225+12.0, step=0.2)
    # params.add("r1", 360, min=360-12.0, max=360+12.0, step=0.2)
    # params.add("bulk", 450, min=450-75.0, max=450+50.0, step=2.0)

    # params.add("surface_density_coeff", 1.0, min=0.1, max=10.0, step=0.1)
    # params.add("intensity_coeff", 1.0, min=0.1, max=10.0, step=0.1)

    minimizer = ba.Minimizer()
    minimizer.setMinimizer("Genetic", "", "MaxIterations=150;RandomSeed=2;PopSize=30")
    result = minimizer.minimize(fit_objective.evaluate_residuals, params)
    fit_objective.finalize(result)
    #
    best_params_so_far = result.parameters()
    minimizer.setMinimizer("Minuit2", "Migrad")
    result = minimizer.minimize(fit_objective.evaluate, best_params_so_far)

    fit_objective.finalize(result)
    print("Fitting completed.")


if __name__ == '__main__':
    run_fitting()
    plt.show()



