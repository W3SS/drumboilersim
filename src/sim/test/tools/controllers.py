#-*- coding: utf-8 -*-

K_p = 800
K_i = .081
K_d = 15

from app.params import *

class PController:
    def __init__(self):
        self.K_p = K_p
        
    def get_q_f(self, L, q_f, q_s):
        return (q_s - L * self.K_p)

class PIController:
    def __init__(self):
        self.K_p = K_p
        self.K_i = K_i

        self.integral = 0

    def get_q_f(self, L, q_f, q_s):
        self.integral -= L
        return q_s + self.integral * self.K_i  - L * self.K_p


class PIDController:
    def __init__(self):
        self.K_p = K_p
        self.K_i = K_i
        self.K_d = K_d
        self.integral = 0
        self.last_q = q_s0

    def get_q_f(self, L, q_f, q_s):
        self.integral -= L
        delt = (q_f - self.last_q)
        ret = q_s + self.integral * self.K_i  - L * self.K_p + self.K_d * delt
        self.last_q = q_f
        return ret
