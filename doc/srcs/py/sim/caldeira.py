#-*- coding: utf-8 -*-

"""Package principal da caldeira"""

from app.params import (V_dc, V_r, V_d, m_t, m_r, m_d, C_p, q_s0,
                        P_0, A_dc, k, g, T_d, beta, step_size, A_d,
                        V_sd_0, h_f, l_o)

import app.tools.metric_prefixes as prefs
import app.tools.thermo as steam
from math import (log1p, sqrt)
import numpy as np
import scipy.optimize
import scipy.linalg
import scipy.misc


class State(object):
    """Estado da caldeira. Guarda todas as variaveis de estado"""
    def __init__(self):
        self.m_d = m_d

        self.prev_dVwt = 0
        self.prev_dP = 0
        self.prev_dalfa_r = 0
        self.prev_dV_sd = 0

        # self.h_f = steam.h_l(steam.P_sat(T_f))

        self.q_s = self.q_f = q_s0
        self.P = P_0


        self.get_values_from_steam_table(self.P)

        self.h_f = h_f

        self.Q = (self.q_s * self.h_s - self.q_f * self.h_f)
        self.V_t = V_r + V_dc + V_d

        self.alfa_r = scipy.optimize.brentq(self._solve_alfa_r0, 1e-10, 1)
        self.alfa_v_avg = self.calc_alfa_v_avg(self.alfa_r)

        self.q_ct = (((self.h_w - self.h_f) / self.h_c) * self.q_f)

        self.V_sd_0 = V_sd_0
        self.V_sd = (self.V_sd_0 - ((T_d * (self.h_w - self.h_f))
                                    / (self.ro_s*self.h_c))* self.q_f)

        self.l_o = l_o

        self.V_wd = l_o * A_d - self.V_sd

        self.V_wt = self.V_wd + V_dc + (1 - self.alfa_v_avg) * V_r


        self.l_wo = self.V_wd / A_d
        self.l_so = self.V_sd / A_d

        self.calc_aux_state_vars()

        self.q_dc = self.Q/(self.alfa_r * self.h_c)


        self.q_r = self.q_dc


        self.calc_output_vars()


    def calc_alfa_v_avg(self, alfa_r):
        """Calcula alfa_v_avg"""

        return ((self.ro_w / (self.ro_w - self.ro_s))
                * (1 - (self.ro_s / ((self.ro_w - self.ro_s) * alfa_r))
                   * log1p(((self.ro_w - self.ro_s)/self.ro_s) * alfa_r)))


    def _solve_alfa_r0(self, alfa_r):
        """Helper para encontrar alfa_r0"""
        alfa_v_avg = self.calc_alfa_v_avg(alfa_r)
        return (alfa_r * self.h_c
                * sqrt((2 * self.ro_w * A_dc * (self.ro_w - self.ro_s)
                        * g * alfa_v_avg * V_r) / k) - self.Q)

    def get_values_from_steam_table(self, P):
        """Atualiza valores com aproximacao da tabela de vapor"""
        self.h_w = steam.h_l(P)
        self.h_s = steam.h_g(P)
        self.ro_w = steam.D_l(P)
        self.ro_s = steam.D_g(P)
        self.t_s = steam.T_sat(P)

        self.dh_w_dP = steam.dh_l_dP(P)
        self.dh_s_dP = steam.dh_g_dP(P)
        self.dro_w_dP = steam.dD_l_dP(P)
        self.dro_s_dP = steam.dD_g_dP(P)
        self.dt_s_dP = steam.dT_sat_dP(P)

        self.h_c = self.h_s - self.h_w

    def calc_aux_state_vars(self):
        """Atualiza state com as variaveis auxiliares de estado"""

        self.get_values_from_steam_table(self.P)

        self.V_st = self.V_t - self.V_wt

        self.alfa_v_avg = self.calc_alfa_v_avg(self.alfa_r)

        aux = self.alfa_r * (self.ro_w - self.ro_s) / self.ro_s

        self.dalfa_v_avg_dP = ((1./ ((self.ro_w - self.ro_s)**2))
                               * (self.ro_w * self.dro_s_dP - self.ro_s * self.dro_w_dP)
                               * (1 + (self.ro_w/self.ro_s) * (1 / (1 + aux))
                                  - ((self.ro_s + self.ro_w)/(aux*self.ro_s))*log1p(aux)))

        self.dalfa_v_avg_dalfa_r = ((self.ro_w / (aux * self.ro_s))
                                    * (log1p(aux)/aux - 1 / (1+aux)))
        self.V_wd = self.V_wt- V_dc - (1 - self.alfa_v_avg) * V_r



        self.q_dc = sqrt((2 * self.ro_w * A_dc * (self.ro_w - self.ro_s)
                          * g * self.alfa_v_avg * V_r) / k)

    def calc_output_vars(self):
        """Calcula as variaveis de saída"""
        self.L = ((((self.V_wd + self.V_sd) / A_d) - self.l_o)
                  / self.l_o)

        self.L_w = ((((self.V_wd) / A_d) - self.l_wo) / self.l_wo)

        self.L_s = ((((self.V_sd) / A_d) - self.l_so) / self.l_so)

    def update_state(self, dVwt, dP, dalfa_r, dV_sd):
        """Faz o update do estado"""

        delt_Vwt = ((dVwt + self.prev_dVwt)/2)*step_size
        delt_P = ((dP + self.prev_dP)/2)*step_size
        delt_alfa_r = ((dalfa_r + self.prev_dalfa_r)/2)*step_size
        delt_Vsd = ((dV_sd + self.prev_dV_sd)/2)*step_size

        # Usa derivadas para calcular o novo X
        self.V_wt = self.V_wt + delt_Vwt
        self.P = self.P + delt_P
        self.alfa_r = self.alfa_r + delt_alfa_r
        self.V_sd = self.V_sd + delt_Vsd

        self.prev_dP = dP
        self.prev_dVwt = dVwt
        self.prev_dalfa_r = dalfa_r
        self.prev_dV_sd = dV_sd


        self.calc_aux_state_vars()
        self.calc_output_vars()

        # Atualiza outras variaveis dependentes de X
        self.q_ct = (((self.h_w - self.h_f) / self.h_c) * self.q_f
                     + (1/self.h_c)*(self.ro_s * self.V_st * self.dh_s_dP
                                     + self.ro_w * self.V_wt * self.dh_w_dP
                                     - self.V_t + m_t * C_p * self.dt_s_dP) * dP)

        self.q_r = (self.q_dc - V_r
                    * (self.alfa_v_avg * self.dro_s_dP
                       + (1 - self.alfa_v_avg) * self.dro_w_dP
                       + (self.ro_w - self.ro_s) * self.dalfa_v_avg_dP) * dP
                    + (self.ro_w - self.ro_s) * V_r
                    * self.dalfa_v_avg_dalfa_r * dalfa_r)

    def __repr__(self):
        """representacao na hora de imprimir"""
        ret = "X = [V_wt=%f; P=%f; alfa_r=%f; V_sd=%f]\n" % (
            self.V_wt, self.P, self.alfa_r, self.V_sd)
        ret = ret + "U = [qf=%f; q_s=%f; Q=%f]\n" % (self.q_f, self.q_s, self.Q)
        ret = ret + "Outras: [alfa_v_avg=%f; q_dc=%f]" % (self.alfa_v_avg, self.q_dc)
        return ret



class Simulator(object):
    """Classe principal da simulacao"""

    def __init__(self):
        self._state = State()
        self.dX = np.zeros(4)

    def calc_e(self):
        """Calcula matriz do sistema linear que caracteriza a caldeira"""

        S = self._state
        e = np.zeros((4, 4))

        e[0][0] = S.ro_w - S.ro_s

        e[0][1] = S.V_wt * S.dro_w_dP + S.V_st * S.dro_s_dP

        e[1][0] = S.ro_w * S.h_w - S.ro_s * S.h_s

        e[1][1] = (S.V_wt * (S.h_w * S.dro_w_dP + S.ro_w * S.dh_w_dP)
                   + S.V_st * (S.h_s * S.dro_s_dP + S.ro_s * S.dh_s_dP)
                   - S.V_t + m_t*C_p*S.dt_s_dP)

        e[2][1] = ((S.ro_w * S.dh_w_dP - S.alfa_r * S.h_c * S.dro_w_dP) * (1 - S.alfa_v_avg) * V_r
                   + ((1 - S.alfa_r)*S.h_c * S.dro_s_dP + S.ro_s * S.dh_s_dP) * S.alfa_v_avg * V_r
                   + (S.ro_s + (S.ro_w - S.ro_s) * S.alfa_r) * S.h_c * V_r * S.dalfa_v_avg_dP
                   - V_r + m_r*C_p*S.dt_s_dP)

        e[2][2] = (((1 - S.alfa_r) * S.ro_s + S.alfa_r * S.ro_w) * S.h_c * V_r
                   * S.dalfa_v_avg_dalfa_r)

        e[3][1] = (S.V_sd * S.dro_s_dP
                   + (1./S.h_c) * (S.ro_s * S.V_sd * S.dh_s_dP
                                   + S.ro_w * S.V_wd * S.dh_w_dP
                                   - S.V_sd - S.V_wd + S.m_d * C_p * S.dt_s_dP)
                   + S.alfa_r * (1 + beta) * V_r
                   * (S.alfa_v_avg * S.dro_s_dP
                      + (1 - S.alfa_v_avg) * S.dro_w_dP
                      + (S.ro_s - S.ro_w) * S.dalfa_v_avg_dP))

        e[3][2] = S.alfa_r * (1 + beta)*(S.ro_s - S.ro_w) * V_r * S.dalfa_v_avg_dalfa_r

        e[3][3] = S.ro_s

        return e

    def step(self):
        """Cada passo da simulacao"""
        E = self.calc_e()
        S = self._state

        B = np.array([S.q_f - S.q_s,
                      S.Q + S.q_f*S.h_f - S.q_s*S.h_s,
                      S.Q - S.alfa_r * S.h_c * S.q_dc,
                      (S.ro_s/T_d) * (S.V_sd_0 - S.V_sd) + ((S.h_f - S.h_w)/S.h_c)*S.q_f])
        self.dX = scipy.linalg.solve(E, B)

        S.update_state(self.dX[0], self.dX[1], self.dX[2], self.dX[3])

