#-*- coding: utf-8 -*-


"""Simulador de planta simples. Gera valores de vazão de vapor para a
caldeira. Observação: a planta deve iniciar no regime permanente
configurado para o simulador"""

from app.params import *

class Plant:
    """Planta simples. Só gera um sinal de degrau no vapor"""
    def __init__(self):
        self.cnt = 0
        self.q = q_s0

    def step(self):
        self.cnt = self.cnt+1
        if self.cnt < 200:
            self.q = q_s0
        else:
            self.q = q_s0 + 10
