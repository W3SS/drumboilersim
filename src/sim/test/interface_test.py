#-*- coding: utf-8 -*-


"""Testa interface """

import zmq

from app.params import (PULL_ADDR, REP_ADDR)

class TestInterface:
    def test_req(self):
        ctx = zmq.Context()
        socket = ctx.socket(zmq.REQ)
        socket.connect(REP_ADDR)
        socket.send(b'report')
        print(socket.recv)

    def test_push(self):
        ctx = zmq.Context()
        socket = ctx.socket(zmq.PUSH)
        socket.connect(PULL_ADDR)
        socket.send(b'qf + 10')
