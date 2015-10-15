#-*- coding: utf-8 -*-

from app.valvula import Valvula
from app.config import step_size
from matplotlib import pyplot, rc, mathtext
class TestValvula:
    def test_step(self):
        v_sem_d = Valvula(0,0)
        v_com_d = Valvula(0,.3)
        T = [x*step_size for x in range(500)]
        Q = []
        Q_d = []
        v_sem_d.q_sp = v_com_d.q_sp = v_sem_d.q_sp + 10
        for i in T:
            v_sem_d.step()
            v_com_d.step()
            Q.append(v_sem_d.q)
            Q_d.append(v_com_d.q)

        rc('text', usetex=True)
        mathtext.fontset = "Computer Modern"


        pyplot.clf()
        pyplot.plot(T, Q)
        pyplot.xlabel(r'\huge{Tempo (s)}')
        pyplot.ylabel(r'\huge{Vaz\~{a}o (kg/s)}')
        pyplot.savefig("plots/valve_step_response.png")

        pyplot.clf()
        pyplot.plot(T, Q_d)
        pyplot.xlabel(r'\huge{Tempo (s)}')
        pyplot.ylabel(r'\huge{Vaz\~{a}o (kg/s)}')
        pyplot.savefig("plots/valve_step_response_biased.png")
