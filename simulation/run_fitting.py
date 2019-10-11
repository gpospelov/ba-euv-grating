"""
Main script to run grating fitting.
"""
import bornagain as ba
from matplotlib import pyplot as plt
from core.simulation_builder import SimulationBuilder
from core.utils import load_setup
import numpy as np


EXPERIMENT_NAME = "exp3"
SAMPLE_NAME = "sinus"


def get_simulation(params):
    exp_config = load_setup("experiments.json", EXPERIMENT_NAME)
    sample_config = load_setup("gratings.json", SAMPLE_NAME)

    exp_config["sample_rotation"] = params["sample_rotation"]
    sample_config["grating_period"] = params["grating_period"]
    sample_config["grating_width"] = params["grating_period"]
    sample_config["grating_height"] = params["grating_height"]

    builder = SimulationBuilder(exp_config, sample_config)
    return builder.build_simulation()


def run_fitting():

    exp_config = load_setup("experiments.json", EXPERIMENT_NAME)
    sample_config = load_setup("gratings.json", SAMPLE_NAME)

    builder = SimulationBuilder(exp_config, sample_config)

    fit_objective = ba.FitObjective()
    fit_objective.addSimulationAndData(get_simulation, builder.experimentalData().array())

    fit_objective.initPrint(1)

    plot_observer = ba.PlotterGISAS(units=ba.AxesUnits.DEGREES)
    fit_objective.initPlot(1, plot_observer.plot)

    params = ba.Parameters()
    params.add("sample_rotation", 0.131, min=0.131-0.05, max=0.131+0.05, step=0.01)
    params.add("grating_height", 225, min=225-75.0, max=225+75.0, step=2.0)
    params.add("grating_period", 834.2, min=834.2-5.0, max=834.2+5.0, step=0.1)

    minimizer = ba.Minimizer()
    minimizer.setMinimizer("Genetic", "", "MaxIterations=100;RandomSeed=2;PopSize=30")
    result = minimizer.minimize(fit_objective.evaluate, params)
    fit_objective.finalize(result)

    best_params_so_far = result.parameters()
    minimizer.setMinimizer("Minuit2", "Migrad")
    result = minimizer.minimize(fit_objective.evaluate, best_params_so_far)

    fit_objective.finalize(result)
    print("Fitting completed.")


if __name__ == '__main__':
    run_fitting()
    plt.show()



