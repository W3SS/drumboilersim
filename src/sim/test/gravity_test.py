#-*- coding: utf-8 -*-

from app import caldeira as cldr
from test.tools.helpers import mock_step_astrom

class TestGravity():
    def test_gravity(self):
        """Testando erros na gravidade"""
        g_ori = cldr.g

        cldr.g = g_ori * .8
        mock_step_astrom(cldr.Simulator(), "g_80")

        cldr.g = g_ori * .9
        mock_step_astrom(cldr.Simulator(), "g_90")

        cldr.g = g_ori * 1.1
        mock_step_astrom(cldr.Simulator(), "g_110")

        cldr.g = g_ori * 1.2
        mock_step_astrom(cldr.Simulator(), "g_120")
