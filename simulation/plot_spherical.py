from matplotlib import pyplot as plt
from core.grating_shape import GratingShape
import matplotlib.patches as patches
from core.utils import load_setup


def test_plt(sample_config):
    shape = GratingShape(sample_config)
    rect = shape.rectangle_set()

    fig1 = plt.figure()
    ax1 = fig1.add_subplot(111, aspect='equal')
    ax1.set_xlim([0, shape.m_period])
    ax1.set_ylim([0, shape.m_thickness*1.1+shape.m_circle0.m_radius])
    for r in rect:
        ax1.add_patch(patches.Rectangle((r.m_x, r.m_y), r.m_width, r.m_height))

    plt.show()



if __name__ == '__main__':
    sample_config = load_setup("gratings.json", "spherical")
    # stress_test(sample_config)
    test_plt(sample_config)
