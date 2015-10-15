#-*- coding: utf-8 -*-


"""Testando comunicação com servidor"""

from interface import Interface

class TestInterface:
    """Testes de comunicação"""

    def test_req(self):
        interface = Interface()
        print(interface.request('qf'))
