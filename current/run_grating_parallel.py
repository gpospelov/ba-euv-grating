"""
Cosine ripple on a 2D lattice. Beam is parallel to the grating.
To generate pdf from the 'output' produced by the script use
markdown-pdf -s custom.css -r landscape *.md
"""

import bornagain as ba
from matplotlib import pyplot as plt
from simulation_builder import ParallelBuilder
from detector_builder import DetectorBuilder
from matplotlib import rcParams
rcParams['image.cmap'] = 'jet'
import matplotlib.gridspec as gridspec
from histogram_utils import *
from report_manager import ReportManager


def plot_simulations(result, detector_masks=None):

    fig = plt.figure(figsize=(16, 8))

    gs1 = gridspec.GridSpec(1, 2)
    gs1.update(left=0.05, right=1.0, bottom=0.525, top=0.95, wspace=0.05)

    plt.subplot(gs1[0])
    ba.plot_histogram(result, zmin=1, zmax=1e+10)

    plt.subplot(gs1[1])
    exp_data = DetectorBuilder().get_histogram()
    if detector_masks:
        apply_mask_to_histogram(exp_data, detector_masks)
    ba.plot_histogram(exp_data)

    gs2 = gridspec.GridSpec(1, 1)
    gs2.update(left=0.05, right=0.95, bottom=0.05, top=0.475, wspace=0.05)
    plt.subplot(gs2[0])
    exp_proj = exp_data.projectionX()
    plt.semilogy(exp_proj.getBinCenters(), exp_proj.getBinValues()+1, label=r'$\phi=0.0^{\circ}$')

    if detector_masks:
        apply_mask_to_histogram(result, detector_masks)
    sim_proj = result.projectionX()
    plt.semilogy(sim_proj.getBinCenters(), sim_proj.getBinValues()+1, label=r'$\phi=0.0^{\circ}$')
    plt.ylim(5e+6, 1e+9)


def run_pack(builder):
    # for i in range(0, 40):
    #     value = 30 + i*3
    #     print("run_pack()", i, value)
    #     builder.m_sample_builder.setParameterValue("grating_width", value)
    #     run_single(builder)

    # for i in range(0, 40):
    #     value = 180 + i*3.0
    #     print("run_pack()", i, value)
    #     builder.m_sample_builder.setParameterValue("grating_height", value)
    #     run_single(builder)

    for i in range(0, 10):
        value = 400 + i*10
        print("run_pack()", i, value)
        builder.m_sample_builder.setParameterValue("grating_bulk", value)
        run_single(builder)


def run_single(builder, report=None):
    result = builder.run()
    plot_simulations(result, detector_masks=builder.m_detector_masks)
    if report:
        report.write_report(builder.parameter_tuple())


if __name__ == '__main__':
    report = ReportManager()

    builder = ParallelBuilder()
    run_single(builder, report)
    # run_pack(builder)

    report.generate_pdf()
    plt.show()
