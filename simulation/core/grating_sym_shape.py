import bornagain as ba
from .grating_shape import Circle, Rectangle
import numpy as np


class GratingSymShape:
    def __init__(self, setup):
        self.m_period = setup["grating_period"]
        self.m_nslices = setup["nslices"]
        self.m_grating_length = setup["length"]
        self.m_r0 = setup["r0"]
        self.m_r0_height = setup["r0_height"]
        self.m_circle0 = Circle(0.0, self.m_r0_height-self.m_r0, self.m_r0)

    def get_y(self, x):
        """
        For x coordinate along grating ripples calculate y-value using one of 3 circles forming the grating
        """
        result = self.m_circle0.get_y(abs(x))
        if result:
            return max(result)
        else:
            return None


    def rectangle_set(self):
        dx = self.m_period / self.m_nslices
        rectangles = []
        for i in range(0, self.m_nslices):
            x = -self.m_period/2 + (i+0.5)*dx
            y = self.get_y(x)
            if y and y > 0.0:
                # print(i, x, y)
                rectangles.append(Rectangle(x-dx/2., 0.0, dx, y))

        return rectangles

    def get_composition(self, material):
        result = ba.ParticleComposition()
        for r in self.rectangle_set():
            ff = ba.FormFactorLongBoxLorentz(self.m_grating_length, r.m_width, r.m_height)
            pos = ba.kvector_t(0, r.m_x+r.m_width/2, r.m_y)
            result.addParticle(ba.Particle(material, ff), pos)
        return result
