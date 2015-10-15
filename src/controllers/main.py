#-*- coding: utf-8 -*-

import time

from controllers.pressure_controller import PressureController
from controllers.level_controller import LevelController

controllers = {
     'P': PressureController(),
     'L': LevelController()}
#controllers = {'P': PressureController()}
for controller_id,controller in controllers.items():
    controller.setDaemon(True)
    controller.start()

while True:
    pass
