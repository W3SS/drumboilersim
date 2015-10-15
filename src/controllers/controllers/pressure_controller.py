#-*- coding: utf-8 -*-

import threading
import time

from tools.interface import Interface
from controllers.config import (REQ_ADDR, PUSH_ADDR)
from tools.generic_controllers import (PIController)
from tools.logger import Logger

PRESSURE_STEP = 10

logger = Logger('controlador pressao')

class PressureController(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        logger.log_msg('Conectando')
        self.interface = Interface(REQ_ADDR, PUSH_ADDR)
        logger.log_msg('Conectado')
        self.controller = PIController(6e7, 3e6, 8.5, -1e12, 1e12, PRESSURE_STEP)
        self.Q0 = float(self.interface.request('Q'))

    def step(self):
        P = float(self.interface.request('P'))
        self.controller.step(P)
        logger.log_msg(P, self.controller.p_port, self.controller.i_port, self.controller.d_port)
        self.interface.send_cmd('Q = ' + str(self.Q0 + self.controller.out))

    def run(self):
        logger.log_msg('Iniciando controlador')
        while True:
            self.step()

            time.sleep(PRESSURE_STEP)

