import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import bornagain as ba
from bornagain import micrometer


class Circle:
    def __init__(self, x0, y0, radius):
        self.m_x0 = x0
        self.m_y0 = y0
        self.m_radius = radius

    def get_y(self, x):
        sq = np.sqrt(self.m_radius**2 - (x-self.m_x0)**2)
        return [self.m_y0 + sq, self.m_y0 - sq]

    def intersect(self, other):
        """
        Calculate points for two circles intersection
        """
        x1 = self.m_x0
        x2 = other.m_x0
        y1 = self.m_y0
        y2 = other.m_y0
        r1 = self.m_radius
        r2 = other.m_radius

        centerdx = x1 - x2
        centerdy = y1 - y2
        R = np.sqrt(centerdx * centerdx + centerdy * centerdy)

        if not (np.abs(r1 - r2) <= R and R <= r1 + r2):
            return []  # no intersection

        R2 = R * R
        R4 = R2 * R2
        a = (r1 * r1 - r2 * r2) / (2 * R2)
        r2r2 = (r1 * r1 - r2 * r2)
        c = np.sqrt(2 * (r1 * r1 + r2 * r2) / R2 - (r2r2 * r2r2) / R4 - 1)

        fx = (x1 + x2) / 2 + a * (x2 - x1)
        gx = c * (y2 - y1) / 2
        ix1 = fx + gx
        ix2 = fx - gx

        fy = (y1 + y2) / 2 + a * (y2 - y1)
        gy = c * (x1 - x2) / 2
        iy1 = fy + gy
        iy2 = fy - gy

        return [(ix1, iy1), (ix2, iy2)]


class Rectangle:
    def __init__(self, x, y, width, height):
        self.m_x = x  # lower left corner
        self.m_y = y  # lower left corner
        self.m_width = width
        self.m_height = height


class GratingShape:
    def __init__(self, period=833.0, thickness=300.0, nslices = 100, grating_length=5.0*micrometer):
        self.m_period = period
        self.m_thickness = thickness
        self.m_nslices = nslices
        self.m_circle0 = Circle(0.0, 0.0, 225.0)
        self.m_circle1 = Circle(period/2.0, 820.0-450.0, 360.0)
        self.m_circle2 = Circle(period, 0.0, 225.0)
        self.m_grating_length = grating_length

    def get_y(self, x):
        """
        For x coordinate along grating ripples calculate y-value using one of 3 circles forming the grating
        """
        if x < self.m_period/2:
            points = self.m_circle0.intersect(self.m_circle1)
            x_intersect = max(points[0][0], points[1][0])  # second intersection point
            if x < x_intersect:
                print("a")
                return max(self.m_circle0.get_y(x))

            else:
                print("b")
                return min(self.m_circle1.get_y(x))
        else:
            points = self.m_circle1.intersect(self.m_circle2)
            x_intersect = min(points[0][0], points[1][0])  # first intersection point
            if x < x_intersect:
                print("c")
                return min(self.m_circle1.get_y(x))
            else:
                print("d")
                return max(self.m_circle2.get_y(x))


    def rectangle_set(self):

        px_intersect = self.m_circle0.intersect(self.m_circle1)[0][0]
        print(self.m_circle0.intersect(self.m_circle1))
        rectangles = []
        for i in range(0, self.m_nslices):
            dx = self.m_period/self.m_nslices
            x = i*dx
            y = self.get_y(x)
            rectangles.append(Rectangle(x, y, dx, self.m_thickness))
            print(i, x, self.get_y(x))

        return rectangles

    def get_composition(self, material):
        result = ba.ParticleComposition()
        # ff = ba.FormFactorLongBoxLorentz(self.m_grating_length, self.m_period * 0.05, 192)
        # pos = ba.kvector_t(0, 0, -100)
        # result.addParticle(ba.Particle(material, ff), pos)
        for r in self.rectangle_set():
            ff = ba.FormFactorLongBoxLorentz(self.m_grating_length, r.m_width, r.m_height)
            pos = ba.kvector_t(0, r.m_x+r.m_width/2, r.m_y)
            result.addParticle(ba.Particle(material, ff), pos)
        return result


if __name__ == '__main__':
    shape = GratingShape()
    rect = shape.rectangle_set()

    fig1 = plt.figure()
    ax1 = fig1.add_subplot(111, aspect='equal')
    ax1.set_xlim([0, shape.m_period])
    ax1.set_ylim([0, shape.m_thickness*1.1+shape.m_circle0.m_radius])
    for r in rect:
        ax1.add_patch(patches.Rectangle((r.m_x, r.m_y), r.m_width, r.m_height))

    plt.show()