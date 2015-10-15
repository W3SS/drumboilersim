#-*- coding: utf-8 -*-


"""Modelo de uma  valvula. Só atrasa o sinal"""

from app.params import (q_s0, step_size, D_q_f, q_f_max)
import numpy.random

class Valvula:
    """Modelo de uma  valvula. Só atrasa o sinal"""
    def __init__(self, centro=0.0, spread=D_q_f):
        self.d_centro = centro
        self.d_spread = spread
        self.q = q_s0 # valor atual
        self.q_sp = q_s0 # setpoint
        self.Kp = .9


    def step(self):
        """Um passo da simulação"""
        self.q_sp = max(0, min(self.q_sp, q_f_max))
        q_err = self.q_sp - self.q # sinal

        q_delt = self.Kp * q_err
        if self.d_spread > 0.0:
            q_delt = q_delt + numpy.random.normal(self.d_centro,
                                                  self.d_spread)

        self.q = max(0,min(self.q + q_delt*step_size, q_f_max))

