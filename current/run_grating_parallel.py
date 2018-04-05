"""
Cosine ripple on a 2D lattice. Beam is parallel to the grating.
To generate pdf from the 'output' produced by the script use
markdown-pdf -s custom.css -r landscape *.md
"""

import bornagain as ba
from matplotlib import pyplot as plt
from SimulationBuilder import ParallelBuilder
from DetectorBuilder import DetectorBuilder
from matplotlib import rcParams
rcParams['image.cmap'] = 'jet'
import matplotlib.gridspec as gridspec
from histogram_utils import *


def plot_simulations(result, filename = None, detector_masks=None):

    fig = plt.figure(figsize=(16, 8))

    print(result.getMinimum(), result.getMaximum())

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

    if filename:
        plt.savefig(filename)


def run_pack(builder):
    # for i in range(0, 30):
    #     height = 170+i*2
    #     print("run_pack()", i, height)
    #     builder.m_sample_builder.setParameterValue("grating_height", height)
    #     run_single(builder)
    for i in range(0, 20):
        period = 820.0 + i
        print("run_pack()", i, period)
        builder.m_sample_builder.setParameterValue("grating_period", period)
        run_single(builder)


def run_single(builder):
    result = builder.run()
    builder.write_report()

    plot_simulations(result, detector_masks=builder.m_detector_masks, filename=builder.output_png_full())


if __name__ == '__main__':
    builder = ParallelBuilder("../reports/output/rectangular_setup")
    run_single(builder)
    # run_pack(builder)
    plt.show()
