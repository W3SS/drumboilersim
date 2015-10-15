#-*- coding: utf-8 -*-


"""Modulo  da interface."""

import zmq

class Interface:
    """Interface do simulador. Implementa uma interface
    'event-driven', ou seja, quando uma mensagem for recebida em um
    dos meios, a função é chamada.

    CONSTRUCTOR ARGS:
      > rep_evt: Função de resposta a requisições. Ela deve receber
        uma string e retornar outra string
      > pull_evt: Função de resposta a comandos de ação. Deve receber
        uma string."""

    def __init__(self, rep_evt, pull_evt, rep_addr="tcp://127.0.0.1:5555",
                 pull_addr="tcp://127.0.0.1:5556"):
        self.ctx = zmq.Context()

        self.rep_socket = self.ctx.socket(zmq.REP)
        self.rep_socket.bind(rep_addr)

        self.pull_socket = self.ctx.socket(zmq.PULL)
        self.pull_socket.bind(pull_addr)

        self.poller = zmq.Poller()
        self.poller.register(self.rep_socket, zmq.POLLIN|zmq.POLLOUT)
        self.poller.register(self.pull_socket, zmq.POLLIN)

        self.rep_evt = rep_evt
        self.pull_evt = pull_evt

        self.result = None

    def act(self):
        """Ve se tem mensagens na fila e, caso haja, realiza a ação
        necessária"""
        print("Esperando mensagem")

        polled = dict(self.poller.poll())


        if self.rep_socket in polled:
            if polled[self.rep_socket] == zmq.POLLIN:
                print("Recebeu requisicao")
                self.result = str(self.rep_evt(self.rep_socket.recv_string()))
                print("Resultado: ", self.result)
            else:
                print("Tentando mandar resposta")
                self.rep_socket.send_string(self.result)
        if self.pull_socket in polled:
            print("Recebeu ordem")
            self.pull_evt(self.pull_socket.recv_string())

