"""
Main script to run grating fitting.
"""
import bornagain as ba
from matplotlib import pyplot as plt
from simulation_builder import SimulationBuilder
from utils.json_utils import load_experimental_setup
from utils.json_utils import load_sample_setup

builder = None

def get_simulation(params):
    builder.m_sample_builder.m_rotation_angle = params["sample_rotation"]
    builder.m_detector_builder.m_beta_b = params["beta_b"]
    builder.m_detector_builder.m_det_dx = params["det_dx"]
    # builder.m_sample_builder.m_grating_period = params["grating_period"]
    return builder.build_simulation()


def run_fitting():
    global builder

    print(builder.experimentalData())
    fit_objective = ba.FitObjective()
    fit_objective.addSimulationAndData(get_simulation, builder.experimentalData().array())

    fit_objective.initPrint(1)
    fit_objective.initPlot(1)

    params = ba.Parameters()
    params.add("sample_rotation", 0.0, min=-1.0, max=1.0, step=0.1)
    params.add("det_dx", 0.0, min=-0.1, max=0.1, step=0.01)
    params.add("beta_b", 78.89, min=78.89-10.0, max=78.89+10.0, step=1.0)
    params.add("grating_period", 833, min=833-50.0, max=833+50.0, step=1.0)

    minimizer = ba.Minimizer()
    minimizer.setMinimizer("Genetic", "", "MaxIterations=3;RandomSeed=1")
    result = minimizer.minimize(fit_objective.evaluate, params)
    fit_objective.finalize(result)
    print("Fitting completed.")


if __name__ == '__main__':
    exp_config = load_experimental_setup("exp2")
    sample_config = load_sample_setup("box")
    builder = SimulationBuilder(exp_config, sample_config)
    run_fitting()
    plt.show()



