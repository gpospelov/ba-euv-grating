"""
Cosine ripple on a 2D lattice. Beam is parallel to the grating.
"""

import bornagain as ba
from matplotlib import pyplot as plt
from core.simulation_builder import SimulationBuilder
from matplotlib import rcParams
rcParams['image.cmap'] = 'jet'
import matplotlib.gridspec as gridspec
from core.report_manager import ReportManager
import numpy as np
from bornagain import nm, deg
from core.utils import load_setup


def plot_simulations(sim_results, exp_data, exp_config):

    fig = plt.figure(figsize=(16, 12))

    gs1 = gridspec.GridSpec(1, 2)
    gs1.update(left=0.05, right=1.0, bottom=0.525, top=0.95, wspace=0.05)

    units = ba.AxesUnits.MM

    plt.subplot(gs1[0])
    ba.plot_colormap(sim_results, zmin=1, zmax=1e+9, units=units, zlabel="")

    plt.subplot(gs1[1])
    ba.plot_colormap(exp_data, zmin=1, zmax=1e+9, units=units, zlabel="")

    gs2 = gridspec.GridSpec(1, 1)
    gs2.update(left=0.05, right=0.95, bottom=0.05, top=0.455, wspace=0.05)
    plt.subplot(gs2[0])
    exp_proj = exp_data.histogram2d(units).projectionX()
    plt.semilogy(exp_proj.getBinCenters(), exp_proj.getBinValues()+1, label=r'$\phi=0.0^{\circ}$')

    sim_proj = sim_results.histogram2d(units).projectionX()
    plt.semilogy(sim_proj.getBinCenters(), sim_proj.getBinValues()+1, label=r'$\phi=0.0^{\circ}$')

    amps = np.concatenate((exp_proj.getBinValues(), sim_proj.getBinValues()))
    mean = np.mean(amps)

    # plt.ylim(mean*0.005, mean*50)
    # plt.ylim(1e+03, 1e+07)
    plt.ylim(exp_config["hmin"], exp_config["hmax"])



def run_single(exp_config, sample_config, report=None):
    builder = SimulationBuilder(exp_config, sample_config)

    sim_result = builder.run_simulation()
    exp_data = builder.experimentalData()
    plot_simulations(sim_result, exp_data, exp_config)

    if report:
        report.write_report(builder.parameter_tuple())


if __name__ == '__main__':
    report = ReportManager()

    exp_config = load_setup("experiments.json", "exp3")
    sample_config = load_setup("gratings.json", "sinus")

    # run_report(report)

    run_single(exp_config, sample_config, report)

    report.generate_pdf()
    plt.show()
