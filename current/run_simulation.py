"""
Cosine ripple on a 2D lattice. Beam is parallel to the grating.
"""

import bornagain as ba
from matplotlib import pyplot as plt
from simulation_builder import SimulationBuilder
from matplotlib import rcParams
rcParams['image.cmap'] = 'jet'
import matplotlib.gridspec as gridspec
from report_manager import ReportManager
from utils.json_utils import load_experimental_setup
from utils.json_utils import load_sample_setup
import numpy as np
from bornagain import nm, deg


def plot_simulations(sim_results, exp_data):

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

    plt.ylim(mean*0.005, mean*50)


def run_pack(exp_config, sample_config, report):

    # report.m_title = "Grating height scan"
    # for i in range(0, 40):
    #     value = 180 + i*2.0
    #     print("run_pack()", i, value)
    #     builder.m_sample_builder.m_grating_height = value
    #     run_single(builder, report)

    # optimal: 826
    # report.m_title = "Period scan"
    # for i in range(0, 3):
    #     value = 780 + i*2
    #     print("run_pack()", i, value)
    #     builder.m_sample_builder.m_grating_period = value
    #     run_single(builder, report)

    ## Optimal: 0.2 deg (exp1), -0.8 exp2
    # report.m_title = "Rotation scan"
    # for value in np.linspace(-0.8, 0.5, 14):
    #     print("run_pack()", value)
    #     builder.m_sample_builder.m_rotation_angle = value
    #     run_single(builder, report)

    # report.m_title = "Beta_b"
    # for value in np.linspace(78.89-10.0, 78.89+10.0, 10):
    #     print("run_pack()", value)
    #     builder.m_detector_builder.m_beta_b = value
    #     run_single(builder, report)

    # report.m_title = "Det DX"
    # for value in np.linspace(-1.0, 1.0, 11):
    #     print("run_pack()", value)
    #     builder.m_detector_builder.m_det_dx = value
    #     run_single(builder, report)

    # report.m_title = "Para Omega"
    # for value in np.linspace(0.1, 100.0, 10):
    #     print("run_pack()", value)
    #     sample_config["interf"]["omega"] = value
    #     run_single(exp_config, sample_config, report)

    # report.m_title = "Exp2 parabox domainsize"
    # for value in np.linspace(0.1, 100000.0, 10):
    #     print("run_pack()", value)
    #     sample_config["interf"]["domain_size"] = value
    #     run_single(exp_config, sample_config, report)

    report.m_title = "Exp2 parasinus height"
    for value in np.linspace(150, 300.0, 10):
        print("run_pack()", value)
        sample_config["height"] = value
        run_single(exp_config, sample_config, report)


def run_single(exp_config, sample_config, report=None):
    builder = SimulationBuilder(exp_config, sample_config)

    sim_result = builder.run_simulation()
    exp_data = builder.experimentalData()
    plot_simulations(sim_result, exp_data)

    if report:
        report.write_report(builder.parameter_tuple())


if __name__ == '__main__':
    report = ReportManager()

    exp_config = load_experimental_setup("exp2")
    sample_config = load_sample_setup("sinuscomp")

    run_single(exp_config, sample_config, report)
    # run_pack(exp_config, sample_config, report)

    report.generate_pdf()
    plt.show()
