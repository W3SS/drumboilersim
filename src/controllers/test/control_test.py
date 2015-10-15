#-*- coding: utf-8 -*-


from  test.tools.controllers import *

from app.caldeira import *
from app.valvula import *
from test.tools.plant_simulator import *

from matplotlib import pyplot, rc, mathtext

class TestController:
    def __init__(self):
        self.caldeira = Simulator()
        self.valvula = Valvula()
        self.plant = Plant()
        self.controller = PIDController()

    def test_controller(self):
        """Testa usando a planta de testes, que nada mais é do que um
        gerador de degrau"""

        T = [x*.1 for x in range(20000)]
        labels = [
            r"\huge{$L$ ($\%$)}",
            r"\huge{$q_s$ ($kg/s$)}",
            r"\huge{$q_f$ ($kg/s$)}",
            r"\huge{$P$ ($MPa$)}"]
        Vs = [[],[],[],[]]


        for i in T:
            self.plant.step()
            self.valvula.step()

            self.caldeira._state.q_f = self.valvula.q
            self.caldeira._state.q_s = self.plant.q


            self.caldeira.step()
            self.caldeira._state.P = P_0

            if i % 100:
                self.valvula.q_sp = self.controller.get_q_f(self.caldeira._state.L,
                    self.caldeira._state.q_f, self.caldeira._state.q_s)

            Vs[0].append(self.caldeira._state.L * 100)
            Vs[1].append(self.caldeira._state.q_s)
            Vs[2].append(self.caldeira._state.q_f)
            Vs[3].append(self.caldeira._state.P)

        rc('text', usetex=True)
        mathtext.fontset = "Computer Modern"

        pyplot.clf()
        pyplot.figure(1)

        plot_grid_sz = 220
        for i in range(4):
            pyplot.subplot(plot_grid_sz + i + 1)
            pyplot.xlabel("\huge{Tempo ($s$)}")
            pyplot.ylabel(labels[i])
            pyplot.plot(T, Vs[i])

        pyplot.tight_layout()

        pyplot.savefig('plots/k_controller_test.png')
