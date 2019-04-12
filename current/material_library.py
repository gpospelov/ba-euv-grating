from bornagain import ba
from bornagain import nm
import periodictable as pt
from periodictable.xsf import xray_energy, xray_sld_from_atoms, xray_sld
from periodictable.xsf import index_of_refraction, mirror_reflectivity


class MaterialLibrary:
    def __init__(self, use_sld=True):
        self.m_use_sld = use_sld
        pass

    def ambience_material(self):
        # return ba.HomogeneousMaterial("air", 0.0, 0.0)
        if self.m_use_sld:
            return ba.MaterialBySLD("air", 0.0, 0.0)
        else:
            return ba.HomogeneousMaterial("air", 0.0, 0.0)

    def substrate_material(self):
        # return ba.HomogeneousMaterial("substrate",  0.00111570884, 0.0018275599)  # Si
        return self.get_si()

    def grating_material(self):
        # return ba.HomogeneousMaterial("grating",  0.101456583, 0.0521341525)  # Au
        return self.get_au()

    def get_si(self):
        if self.m_use_sld:
            return ba.MaterialBySLD("si", 3.8419756509395133e-07, 6.282115314984396e-07)
            # return ba.MaterialBySLD("si", 2.0071e-05, 4.5816e-07)
        else:
            return ba.HomogeneousMaterial("si", 0.001117707391540712, -0.0018275927179164807)

    def get_au(self):
        if self.m_use_sld:
            return ba.MaterialBySLD("au", 3.4838805704272005e-05, 1.7905760965614288e-05)
            # return ba.MaterialBySLD("au", 0.0001249, 1.2871e-05)
        else:
            return ba.HomogeneousMaterial("au", 0.001117707391540712, -0.0018275927179164807)


if __name__ == '__main__':
    # factory = MaterialFactory()

    wavelength = 10

    print("--- Si ---")
    print(pt.Si.density)
    si = pt.formula("Si")
    rho, mu = pt.xray_sld(si, density=pt.Si.density, wavelength=wavelength)
    print("si rho_mu:",rho*1e-6, mu*1e-6)
    # ri = pt.xsf.index_of_refraction({pt.Si: 1}, density=pt.Si.density, wavelength=wavelength)
    # print("si refractive coeff:",ri, 1.0-ri.real, ri.imag)

    print("--- Au ---")
    print(pt.Au.density)
    au = pt.formula("Au")
    rho, mu = pt.xray_sld(au, density=pt.Au.density, wavelength=wavelength)
    print("au rho_mu:",rho*1e-6, mu*1e-6)
    # ri = pt.xsf.index_of_refraction({pt.Au: 1}, density=pt.Au.density, wavelength=wavelength)
    # print("au refractive coeff:", ri, 1.0-ri.real, ri.imag)
