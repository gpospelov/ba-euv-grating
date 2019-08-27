from matplotlib import pyplot as plt
from core.grating_shape import GratingShape
from core.grating_sym_shape import GratingSymShape
import matplotlib.patches as patches
from core.utils import load_setup


def plot_spherical():
    sample_config = load_setup("gratings.json", "spherical")
    shape = GratingShape(sample_config)
    rect = shape.rectangle_set()

    fig1 = plt.figure()
    ax1 = fig1.add_subplot(111, aspect='equal')
    ax1.set_xlim([0, shape.m_period])
    ax1.set_ylim([0, shape.m_thickness*1.1+shape.m_circle0.m_radius])
    for r in rect:
        ax1.add_patch(patches.Rectangle((r.m_x, r.m_y), r.m_width, r.m_height))

    plt.show()


def plot_sphericalsym():
    sample_config = load_setup("gratings.json", "sphericalsym")
    # sample_config["r0"] = 200.0
    # sample_config["r0_height"] = 300.0
    shape = GratingSymShape(sample_config)
    rect = shape.rectangle_set()

    fig1 = plt.figure()
    ax1 = fig1.add_subplot(111, aspect='equal')
    ax1.set_xlim([-shape.m_period/2, shape.m_period/2])
    ax1.set_ylim([0, 300])
    for r in rect:
        ax1.add_patch(patches.Rectangle((r.m_x, r.m_y), r.m_width, r.m_height))

    plt.show()


if __name__ == '__main__':
    # plot_spherical()
    plot_sphericalsym()
