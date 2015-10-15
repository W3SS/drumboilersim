#-*- coding: utf-8 -*-


"""Modelo do queimador"""

from app.params import (Q_max, step_size)

class Queimador:
    def __init__(self, Q):
        self.Q = Q
        self.setpoint = Q
        self.Kp = .5

    def step(self):
        self.setpoint = max(0, min(Q_max, self.setpoint))
        self.error = self.setpoint - self.Q

        self.Q_delta = self.Kp * self.error
        self.Q = max(0, min(Q_max, self.Q + self.Q_delta * step_size))
