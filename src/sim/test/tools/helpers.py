#-*- coding: utf-8 -*-


"""Helper module for testing"""
from nose.tools import (ok_)

import numpy as np
import matplotlib.pyplot as pyplot

from matplotlib import (rc, mathtext)

from app.params import step_size

def float_eq_(val_a, val_b, threshold=1e-12):
    """Testes if two numbers are equal, according to an absolute
    threshold (necessary for float comparison)"""
    ok_(abs(val_a - val_b) < threshold, "%f != %f" % (val_a, val_b))

def relative_eq_(real_value, approx_value, threshold=1e-12):
    """Tests if two float numbers are real, according to a relative
    threshold"""
    relative_error = abs((real_value - approx_value) / real_value)
    ok_(relative_error < threshold, "%f != %f -> err %f > %f" % (
        real_value,
        approx_value,
        relative_error,
        threshold))


def mock_step_astrom(caldeira, plot_id=""):
    """Refaz o step de Astrom"""


    if plot_id is not "":
        plot_id = "_" + plot_id

    S = caldeira._state

    t_steady = 50
    t_end  = 200

    T = np.arange(0, t_end, step_size)
    P = []
    V_wt = []
    alfa_r = []
    V_sd = []
    q_dc = []
    q_r = []
    q_ct = []

    L = []
    Lw = []
    Ls = []
    alfa_v_avg = []


    increased = False
    for i in T:
        if i >= t_steady and not increased:
            S.q_s = S.q_s + 10
            # S.Q = S.Q + 10e6
            increased = True
        caldeira.step()
        P.append(S.P)
        V_wt.append(S.V_wt)
        alfa_r.append(S.alfa_r)
        V_sd.append(S.V_sd)
        q_dc.append(S.q_dc)
        q_r.append(S.q_r)
        q_ct.append(S.q_ct)

        L.append(S.L)
        Lw.append(S.L_w)
        Ls.append(S.L_s)
        alfa_v_avg.append(S.alfa_v_avg)

        # print(caldeira.dX)


    rc('text', usetex=True)
    mathtext.fontset = "Computer Modern"

    pyplot.clf()
    pyplot.figure(1)


    pyplot.subplot(321)
    pyplot.plot(T, P)
    pyplot.xlabel(r'Tempo ($s$)')
    pyplot.ylabel(r'$p$ ($MPa$)')

    pyplot.subplot(322)
    pyplot.plot(T, V_wt)
    pyplot.xlabel(r'Tempo ($s$)')
    pyplot.ylabel(r'$V_{wt}$ ($m^3$)')

    pyplot.subplot(323)
    pyplot.plot(T, alfa_r)
    pyplot.xlabel(r'Tempo ($s$)')
    pyplot.ylabel(r'$\alpha_r$')

    pyplot.subplot(324)
    pyplot.plot(T, V_sd)
    pyplot.xlabel(r'Tempo ($s$)')
    pyplot.ylabel(r'$V_{sd}$ ($m^3$)')

    pyplot.subplot(325)
    line_q_dc, = pyplot.plot(T, q_dc, 'b', label='$q_{dc}$')
    line_q_r, = pyplot.plot(T, q_r, '--', label='$q_r$')
    pyplot.legend(handles=[line_q_dc, line_q_r])
    pyplot.xlabel(r'Tempo ($s$)')
    pyplot.ylabel(r'($kg/s$)')


    pyplot.subplot(326)
    pyplot.plot(T, q_ct)
    pyplot.xlabel(r'Tempo ($s$)')
    pyplot.ylabel(r'$q_{ct}$ ($kg/s$)')

    pyplot.tight_layout()
    pyplot.savefig("plots/response_test"+ plot_id + ".png")

    pyplot.clf()

    pyplot.subplot(321)
    pyplot.plot(T, L)
    pyplot.xlabel(r'Tempo ($s$)')
    pyplot.ylabel(r'$L$')

    pyplot.subplot(322)
    pyplot.plot(T, P)
    pyplot.xlabel(r'Tempo ($s$)')
    pyplot.ylabel(r'$p$ ($MPa$)')

    pyplot.subplot(323)
    pyplot.plot(T, Lw)
    pyplot.xlabel(r'Tempo ($s$)')
    pyplot.ylabel(r'$L_w$')

    pyplot.subplot(324)
    pyplot.plot(T, alfa_v_avg)
    pyplot.xlabel(r'Tempo ($s$)')
    pyplot.ylabel(r'$\bar{\alpha_v}$')

    pyplot.subplot(325)
    pyplot.plot(T, Ls)
    pyplot.xlabel(r'Tempo ($s$)')
    pyplot.ylabel(r'$L_s$')

    pyplot.subplot(326)
    pyplot.plot(T,alfa_r)
    pyplot.xlabel(r'Tempo ($s$)')
    pyplot.ylabel(r'$\alpha_r$')

    pyplot.tight_layout()
    pyplot.savefig("plots/response_test_2"+ plot_id + ".png")

    pyplot.clf()
    pyplot.subplot(111)
    pyplot.plot(T, L)
    pyplot.xlabel(r'Tempo ($s$)')
    pyplot.ylabel(r'$L$')

    pyplot.tight_layout()
    pyplot.savefig("plots/level_response_test"+ plot_id + ".png")



def estimate_init(caldeira):
    """Injeta variáveis globais modificadas no módulo da caldeira, com
    base nas estimativas a partir dos valores iniciais"""
    pass
