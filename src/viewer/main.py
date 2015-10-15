#-*- coding: utf-8 -*-


"""Viewer"""

import matplotlib.pyplot as plt
from matplotlib import rc, mathtext
import time
from interface import Interface
from config import (REQ_ADDR, PUSH_ADDR)

# opcoes de plotagem, usar TeX
rc('text', usetex=True)
mathtext.fontset = "Computer Modern"


# Interface com server
interface = Interface(REQ_ADDR, PUSH_ADDR)

# eixo X
t = []

# variaveis para plotagem
var_cmds = ['qf', 'qs', 'P', 'Q', 'L', 'alfa_r']

titles = [r'$q_f$', r'$q_s$', r'$P$', r'$Q$', r'$L$', r'$\alpha_r$']

amt_vars = len(var_cmds)

var_ids = range(amt_vars)

vals = [[] for x in var_ids]

# Indice do sample
sample_id = 0

# Configuracoes dos plots
plt.ion()

fig = plt.figure()
plot_sz = 200 + int(amt_vars / 2 + amt_vars % 2)*10

axs = [fig.add_subplot(plot_sz + x + 1) for x in var_ids]

lines = []
for i in var_ids:
    ax  = axs[i]
    line, = ax.plot([], [], 'r-')
    lines.append(line)
    ax.set_title(titles[i])

while True:
    t.append(sample_id)
    for i in var_ids:
        vals[i].append(interface.request(var_cmds[i]))
        lines[i].set_data(t, vals[i])
        axs[i].relim()
        axs[i].autoscale()

    fig.tight_layout()
    fig.canvas.draw()

    time.sleep(.1)

    sample_id = sample_id + 1
