"""
Main script to run grating fitting.
"""
import bornagain as ba
from matplotlib import pyplot as plt
from simulation_builder import SimulationBuilder
from utils.json_utils import load_experimental_setup
from utils.json_utils import load_sample_setup
import numpy as np


EXPERIMENT_NAME = "exp2"
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

    # sample_config["period"] = params["grating_period"]
    # exp_config["sample_rotation"] = params["sample_rotation"]
    # exp_config["det_dx"] = params["det_dx"]
    # exp_config["beta_b"] = params["beta_b"]

    sample_config["grating_period"] = params["grating_period"]
    # sample_config["grating_width"] = params["grating_period"]
    sample_config["grating_height"] = params["grating_height"]

    # sample_config["r0"] = params["r0"]
    # sample_config["r1"] = params["r1"]
    # sample_config["bulk"] = params["bulk"]

    builder = SimulationBuilder(exp_config, sample_config)

    # builder.m_sample_builder.m_rotation_angle = params["sample_rotation"]
    # # builder.m_detector_builder.m_beta_b = params["beta_b"]
    # # builder.m_detector_builder.m_det_dx = params["det_dx"]
    # builder.m_sample_builder.m_grating_period = params["grating_period"]
    return builder.build_simulation()


def run_fitting():

    exp_config = load_experimental_setup("exp2")
    sample_config = load_sample_setup("sinus")
    builder = SimulationBuilder(exp_config, sample_config)

    fit_objective = MyObjective()
    fit_objective.addSimulationAndData(get_simulation, builder.experimentalData().array())

    fit_objective.initPrint(1)
    fit_objective.initPlot(1)

    params = ba.Parameters()
    # params.add("sample_rotation", -0.731, min=-0.731-0.2, max=-0.731+0.2, step=0.01)
    # params.add("det_dx", 0.00225, min=0.00225-0.005, max=0.00225+0.005, step=0.0005)
    # params.add("beta_b", 72.12, min=72.12-5.0, max=72.12+5.0, step=0.5)
    params.add("grating_height", 201, min=201-60.0, max=201+100.0, step=1.0)

    params.add("grating_period", 834.2, min=834.2-3.0, max=834.2+3.0, step=0.1)
    # params.add("r0", 225, min=225-12.0, max=225+12.0, step=0.2)
    # params.add("r1", 360, min=360-12.0, max=360+12.0, step=0.2)
    # params.add("bulk", 450, min=450-75.0, max=450+50.0, step=10.0)

    minimizer = ba.Minimizer()
    # minimizer.setMinimizer("Genetic", "", "MaxIterations=200;RandomSeed=2;PopSize=20")
    # result = minimizer.minimize(fit_objective.evaluate_residuals, params)
    # fit_objective.finalize(result)
    #
    # best_params_so_far = result.parameters()
    best_params_so_far = params
    minimizer.setMinimizer("Minuit2", "Migrad")
    result = minimizer.minimize(fit_objective.evaluate, best_params_so_far)

    fit_objective.finalize(result)
    print("Fitting completed.")


if __name__ == '__main__':
    run_fitting()
    plt.show()



