from bornagain import ba
from bornagain import nm, angstrom
import periodictable as pt
from periodictable.xsf import xray_energy, xray_sld_from_atoms, xray_sld
from periodictable.xsf import index_of_refraction, mirror_reflectivity


class MaterialLibrary:
    def __init__(self):
        pass

    def get_air(self, wavelength=None):
        return ba.MaterialBySLD("air", 0.0, 0.0)

    def get_si(self, wavelength=None):
        si = pt.formula("Si")
        dens = pt.Si.density
        rho, mu = pt.xray_sld(si, density=pt.Si.density, wavelength=wavelength/angstrom)
        rho *= 1e-6
        mu *= 1e-6
        print("MaterialLibrary > wavelength:{0} formula:{1} density:{2} rho:{3} mu:{4}".format(wavelength, si, dens, rho, mu))
        return ba.MaterialBySLD("si", rho, mu)

    def get_au(self, wavelength=None):
        au = pt.formula("Au")
        dens = pt.Au.density
        rho, mu = pt.xray_sld(au, density=dens, wavelength=wavelength/angstrom)
        rho *= 1e-6
        mu *= 1e-6
        print("MaterialLibrary > wavelength:{0} formula:{1} density:{2} rho:{3} mu:{4}".format(wavelength, au, dens, rho, mu))
        return ba.MaterialBySLD("au", rho, mu)


if __name__ == '__main__':
    wavelength = 13.52*nm
    print("--- Si ---")
    MaterialLibrary().get_si(wavelength)
    print("--- Au ---")
    MaterialLibrary().get_au(wavelength)
