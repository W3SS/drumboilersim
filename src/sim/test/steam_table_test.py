#-*- coding: utf-8 -*-

import app.tools.thermo as steam
from test.tools.helpers import (relative_eq_)

from matplotlib import pyplot, rc, mathtext


Ps = [8, 8.4, 8.5, 8.7, 2.11169, 1.7048, 2.12896, 2.63063, 2, 2.2, 1.5, 1.57232, 1.6, 1.7048, 2]
T_sats = [294.96, 298.38, 299.22, 300.87, 215.13, 204.43, 215.55, 226.66, 212.36, 217.23, 198.28, 200.52, 201.36, 204.43, 212.36]
h_ls = [1.3171e+06, 1.3361e+06, 1.3407e+06, 1.35e+06, 921260, 872470, 923180, 974660, 908590, 930950, 844660, 854780, 858560, 872470, 908590]
D_ls = [722.439, 715.563, 713.827, 710.429, 846.525, 859.476, 846.024, 831.739, 849.907, 843.882, 866.7, 864.08, 863.11, 859.47, 849.91]
h_gs = [2.7599e+06, 2.754e+06, 2.7524e+06, 2.7493e+06, 2.7983e+06, 2.7935e+06, 2.7985e+06, 2.8015e+06, 2.7972e+06, 2.7991e+06, 2.7899e+06, 2.7913e+06, 2.7917e+06, 2.7935e+06, 2.7972e+06]
D_gs = [42.517, 44.996, 45.624, 46.891, 10.596, 8.598, 10.681, 13.164, 10.047, 11.032, 7.596, 7.9497, 8.085, 8.598, 10.047]



class TestSteamTable():
    """Testa se os valores aproximados estão de acordo com as
    steam tables de referencia"""
    def values_test(self):
        """Testa cada valor"""

        rel_err = .0026
        for i in range(len(Ps)):
            relative_eq_(T_sats[i], steam.T_sat(Ps[i]), rel_err)
            relative_eq_(h_ls[i], steam.h_l(Ps[i]), rel_err)
            relative_eq_(D_ls[i], steam.D_l(Ps[i]), rel_err)
            relative_eq_(h_gs[i], steam.h_g(Ps[i]), rel_err)
            relative_eq_(D_gs[i], steam.D_g(Ps[i]), rel_err)

    def values_plot_test(self):
        rc('text', usetex=True)
        mathtext.fontset = "Computer Modern"

        Psf = [x/100. for x in range(120, 900)]

        steam_tables = [T_sats, h_ls, D_ls, h_gs, D_gs]

        funcs = [[steam.T_sat(x) for x in Psf],
                 [steam.h_l(x) for x in Psf],
                 [steam.D_l(x) for x in Psf],
                 [steam.h_g(x) for x in Psf],
                 [steam.D_g(x) for x in Psf]]

        ylabels = [r"$T_{sat} (^oC)$",
                   r'$h_w (J/kg)$',
                   r"$\rho_w (kg/m^3)$",
                   r"$h_s (J/kg)$",
                   r"$\rho_s (kg/m^3)$"]


        pyplot.clf()
        pyplot.figure(1)

        plot_grid_sz = 320

        for i in range(len(steam_tables)):
            pyplot.subplot(plot_grid_sz + i + 1)
            pyplot.xlabel(r'Press\~{a}o (MPa)')
            pyplot.ylabel(ylabels[i])
            pyplot.plot(Psf, funcs[i])
            pyplot.scatter(Ps, steam_tables[i], c='g', marker='+', s=80)

        pyplot.tight_layout()

        pyplot.savefig("plots/steam_table_test.png")
