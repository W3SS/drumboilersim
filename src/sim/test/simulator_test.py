#-*- coding: utf-8 -*-


from app import caldeira as cldr
from test.tools.helpers import mock_step_astrom

class TestSimulator():

    def test_init_params(self):
        caldeira = cldr.Simulator()
        print("parametros iniciais:")
        print(caldeira._state)


    def test_response(self):
        """Reproduzindo situação de simulações de Astrom & Bell"""
        caldeira = cldr.Simulator()
        mock_step_astrom(caldeira)
