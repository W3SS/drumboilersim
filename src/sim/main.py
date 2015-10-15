#-*- coding: utf-8 -*-


"""Ponto de entrada da simulação. Dispara a thread e vigia o input"""


from app.sim_thread import LoopThread
from app.caldeira import Simulator
from app.interface import Interface
from app.queimador import Queimador

#from app.params import MAX_SAMPLING_FREQ
from app.valvula import Valvula
import threading
from time import time

from app.params import (REP_ADDR, PULL_ADDR)

# Instanciando simulador, lock e thread
caldeira = Simulator()
valvula = Valvula()
caldeiraLock = threading.Lock()

state = caldeira._state

queimador = Queimador(state.Q)

loop_thread = LoopThread(caldeira, valvula, queimador, caldeiraLock)
loop_thread.setDaemon(True) # vai fechar quando main fechar
loop_thread.start()

t0 = time()

def reply_event(command):
    print("Comando: ", command)
    with caldeiraLock:
        if command == "qs":
            return str(state.q_s)
        elif command == "qf":
            return str(state.q_f)
        elif command == "Q":
            return str(state.Q)
        elif command == "L":
            return str(state.L)
        elif command == "P":
            return str(state.P)
        elif command == 'alfa_r':
            return str(state.alfa_r)

def parse_array(arr, old):
    """Helper usado para parsear o input"""
    ret = old

    arr[1] = float(arr[1])

    if arr[0] == '+':
        ret = old + arr[1]
    elif arr[0] == '-':
        ret = old - arr[1]
    elif arr[0] == '*':
        ret = old * arr[1]
    elif arr[0] == '/':
        ret = old / arr[1]
    elif arr[0] == '=':
        ret = arr[1]
    return ret

def pull_event(command):
    print("Comando: ", command)
    cmd_s = command.split()
    with caldeiraLock:
        if cmd_s[0] == "qs":
            state.q_s = parse_array(cmd_s[1:], state.q_s)
        elif cmd_s[0] == "qf":
            valvula.q_sp = parse_array(cmd_s[1:], valvula.q_sp)
        elif cmd_s[0] == "Q":
            queimador.setpoint = parse_array(cmd_s[1:], queimador.setpoint)

input_interface = Interface(reply_event, pull_event, REP_ADDR, PULL_ADDR)

while True:
    # ignora comandos se ultrapassar frequencia de sampling
    # while time() - t0 <= 1./MAX_SAMPLING_FREQ:
    #     pass
    # t0 = time()

    input_interface.act()
