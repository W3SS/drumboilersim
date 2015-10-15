#-*- coding: utf-8 -*-


import threading
import time
import math

from tools.interface import Interface
from tools.generic_controllers import (PIController, PController)
from controllers.config import (REQ_ADDR, PUSH_ADDR)
from tools.logger import Logger

CONTROLLER_STEP = 3.

logger = Logger('controlador nivel')

class LevelController(threading.Thread):
    def __init__(self):
        logger.log_msg('Conectando')
        self.interface = Interface(REQ_ADDR, PUSH_ADDR)
        logger.log_msg('Conectado')
        threading.Thread.__init__(self)
        self.setpoint = 0.0

        self.LRC = PIController(60, 1.2, 0, -1300, 1300, CONTROLLER_STEP)
        self.out = 0

    def step(self):
        L = float(self.interface.request('L'))
        q_s = float(self.interface.request('qs'))

        self.LRC.step(L)

        self.out = q_s + self.LRC.out

        self.interface.send_cmd('qf = ' + str(self.out))

    def run(self):
        logger.log_msg('Iniciando controlador')
        while True:
            self.step()
            time.sleep(CONTROLLER_STEP)
