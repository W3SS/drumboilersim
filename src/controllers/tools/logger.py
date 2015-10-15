#-*- coding: utf-8 -*-

"""Modulo de logs"""

class Logger:
    """Classe de log"""
    def __init__(self, log_tag):
        self.log_tag = '[' + str(log_tag) + ']'

    def log_msg(self, *msg):
        print(self.log_tag, msg)
