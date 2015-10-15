#-*- coding: utf-8 -*-

"""Loop principal da simulacao"""
from app.params import step_size
import threading
from time import time

class LoopThread(threading.Thread):
    """Thread do loop da simulacao"""
    def __init__(self, caldeira, valvula, queimador, caldeiraLock):
        threading.Thread.__init__(self)
        self.t0 = time()
        self.caldeira = caldeira
        self.valvula = valvula
        self.queimador = queimador
        self.caldeiraLock = caldeiraLock

    def run(self):
        while True:
            ti = time()

            # tempo estourou: hora de atualizar caldeira
            if ti - self.t0 >= step_size:
                with self.caldeiraLock:
                    # step do controlador da valvula
                    self.valvula.step()
                    self.queimador.step()
                    # passa valor de feed para caldeira
                    self.caldeira._state.q_f = self.valvula.q
                    self.caldeira._state.Q = self.queimador.Q
                    # print(self.valvula.q, self.valvula.q_sp)

                    # step da caldeira
                    self.caldeira.step()
                    self.t0 = ti
