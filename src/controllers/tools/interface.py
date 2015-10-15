#-*- coding: utf-8 -*-


"""Modulo de comunicação com o servidor"""

import zmq

class Interface:
    """Classe usada para comunicar-se com o servidor"""
    def __init__(self, req_addr='tcp://127.0.0.1:5555',
                 push_addr='tcp://127.0.0.1:5556'):
        self.context = zmq.Context()

        self.req_socket = self.context.socket(zmq.REQ)
        self.push_socket = self.context.socket(zmq.PUSH)

        self.req_socket.connect(req_addr)
        self.push_socket.connect(push_addr)

    def send_cmd(self, cmd):
        """Envia comando para simulador"""
        self.push_socket.send_string(cmd)

    def request(self, req_cmd):
        """Realiza uma requisição ao simulador"""
        self.req_socket.send_string(req_cmd)
        return self.req_socket.recv_string()
