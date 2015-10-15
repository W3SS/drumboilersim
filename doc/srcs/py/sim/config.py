#-*- coding: utf-8 -*-

"""Parametros de uma caldeira
Fonte: K.J. Astrom, R.D. Bell - Drum-boiler dynamics (2000)"""


from app.tools.metric_prefixes import *

g = 9.8
C_p = 550


V_d = 41.0
V_r = 37.0
V_dc = 11.0
A_d = 20.0
m_t = 3e5
m_r = 1.6e5
m_d = 1e5
k = 25.0
T_d = 12.0
beta = .3

A_dc = .381657338

# parametros iniciais
q_s0 = 49.945
P_0 = 8.5 # Pa
V_sd_0 = 7.7930138
#V_sd0 = 4.9
q_ct0 = 11

# parametros de operacao da caldeira
l_o = 1.20525

# parametros retirados dos graficos
h_f = 1029763.91777

# parametros de simulacao
step_size = .1

# Disturbio das valvulas
D_q_f = .3

# Vazao massica maxima da valvula de entrada
q_f_max = 130

# Fluxo de calor maximo
Q_max = 1.5e8

# Endereco para requisicoes
REP_ADDR = "tcp://127.0.0.1:5555"

# Endereco para acoes
PULL_ADDR = "tcp://127.0.0.1:5556"
