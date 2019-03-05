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
from utils.json_utils import load_setup


def plot_simulations(sim_results, exp_data):

    fig = plt.figure(figsize=(16, 12))

    gs1 = gridspec.GridSpec(1, 2)
    gs1.update(left=0.05, right=1.0, bottom=0.525, top=0.95, wspace=0.05)

    units = ba.AxesUnits.DEGREES

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
    plt.ylim(5e+6, 1e+9)


def run_pack(builder, report):

    report.m_title = "Grating height scan"
    for i in range(0, 4):
        value = 180 + i*3.0
        print("run_pack()", i, value)
        builder.m_sample_builder.m_grating_height = value
        run_single(builder, report)


def run_single(builder, report=None):
    sim_result = builder.run_simulation()
    exp_data = builder.experimentalData()
    plot_simulations(sim_result, exp_data)

    if report:
        report.write_report(builder.parameter_tuple())


if __name__ == '__main__':
    report = ReportManager()

    cfg = load_setup("exp1")
    builder = SimulationBuilder(cfg)

    run_single(builder, report)
    # run_pack(builder, report)

    report.generate_pdf()
    plt.show()
