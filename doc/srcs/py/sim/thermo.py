# -*- coding: utf-8 -*-

"""Package contem as funcoes de aproximacao das propriedades
termodinamicas da agua

Mais informacoes:
  Approximate functions for the fast calculation of light-water
  properties at saturation, Wm. J. Garland e J.D. Hoskins (1988)
"""

from math import exp

def D_l(P):
    """Densidade do liquido
    Recebe: P(MPa)
    Retorna: kg/m^3"""

    if P < .075 or P > 21.5:
        raise ValueError("Valor fora do range, %.4f" % P)
    if P <= 1:
        return 1./(1.2746977e-4 * P**.4644339 + .001)
    elif P <= 3.88:
        return 1./(1.0476071e-4 * P**.5651090 + .001022)
    elif P <= 8.84:
        return 1./(3.2836717e-5 * P + 1.12174735e-3)
    elif P <= 14.463:
        return 1./(3.3551046e-4 * exp(5.8403566e-2 * P) + .00085)
    elif P <= 18.052:
        return 1./(3.1014626e-8 * P**3.284754 + .00143)
    elif P <= 20.204:
        return 1./(1.5490787e-11 * P**5.7205 + .001605)
    else:
        return 1./(4.1035988e-24 * P**15.03329 + .00189)



def D_g(P):
    """Densidade do gas
    Recebe: P(MPa)
    Retorna: kg/m^3"""
    if P <= .085 or P > 21.5:
        raise ValueError("Valor fora do range")
    elif P < 1.112:
        return 5.126076 * P**.9475862 + .012
    elif P < 3.932:
        return 4.630832 * P**1.038819 + .52
    elif P < 8.996:
        return 2.868721 * P**1.252148 + 3.8
    elif P < 14.628:
        return .5497653 * P**1.831182 + 18.111
    elif P <= 18.21:
        return 8.6791582e-3 * P**3.176484 + 50
    elif P <= 20.253:
        return 3.5587113e-6 * P**5.660939 + 88
    else:
        return 3.558734e-16 * P**13.03774 + 138


def h_l(P):
    """Entalpia da agua
    Recebe: P(MPa)
    Retorna: J/kg"""
    if P <= .075 or P > 21.7:
        raise ValueError("Valor fora do range")
    elif P < .942:
        return (912.1779 * P**.2061637 - 150) * 1000
    elif P < 4.02:
        return (638.0621 * P**.2963192 + 125) * 1000
    elif P < 9.964:
        return (373.7665 * P**.4235532 + 415) * 1000
    elif P < 16.673:
        return (75.38673 * P**.8282384 + 900) * 1000
    elif P < 20.396:
        return (.1150827 * P**2.711412 + 1440) * 1000
    else:
        return (9.1417257e-14*P**11.47287 + 1752) * 1000


def h_g(P):
    """Entalpia do gas
    Recebe: P(MPa)
    Retorna: J/kg"""
    if P <= .075 or P > 21.55:
        raise ValueError("Valor fora do range")
    elif P <= .348:
        return (-4.0381938e-6 * (3-P)**15.72364 + 2750) * 1000
    elif P <= 1.248:
        return (-.5767304 * exp(-1.66153 * (P-3.2)) + 2800) * 1000
    elif P <= 2.955:
        return (-7.835986 * (3.001 - P)**2 + 2.934312 * (3.001 - P) + \
          2803.71) * 1000
    elif P <= 6.522:
        return (-1.347244 * (P - 2.999)**2 - 2.326913 * (P - 2.999) + \
          2803.35) * 1000
    elif P < 16.497:
        return (-.9219176*(P-9)**2 - 16.38835 * (P-9) + 2742.03) * 1000
    elif P < 20.193:
        return (-3.532177 * (P - 8)**2 + 29.81305 * (P - 8) + 2565) * 1000
    else:
        return (-22.92521 * (P - 18)**2 + 44.23671 * (P - 18) + 2415.01) * 1000


def T_sat(P):
    """Temperatuda de saturacao da agua
    Recebe: P(MPa)
    Retorna: Celsius"""
    if P < .07 or P > 21.85:
        raise ValueError("Valor fora do range")
    elif P < .359:
        return 236.2315 * P ** .1784767 - 57
    elif P <= 1.676:
        return 207.9248 * P ** .2092705 - 28
    elif P <= 8.511:
        return 185.0779 * P ** .2323217 - 5
    elif P < 17.69:
        return 195.1819 * P ** .2241729 - 16
    else:
        return 227.2963 * P ** .201581 - 50

######################################################################
# Derivadas das funcoes anteriores (em funcao da Pressao)
######################################################################

def dD_l_dP(P):
    """Derivada em relacao a pressao da densidade do liquido
    Recebe: P (MPa)"""

    if P < .075 or P > 21.5:
        raise ValueError("Valor fora do range, %.4f" % P)
    if P <= 1:
        return -3643.48/((P**.464434 + 7.845)**2 * P**.535566)
    elif P <= 3.88:
        return -5394.28 / ((P**.565109 + 9.75557)**2 * P**.434891)
    elif P <= 8.84:
        return - 30453.7 / (P + 34.1614)**2
    elif P <= 14.463:
        return - (174.074 * exp(.0584036 * P)) / \
          (2.53345 + exp(.0584036*P))**2
    elif P <= 18.052:
        return - (1.0591e8 * P ** 2.28475) / \
          (P**3.28475 + 46107.3)**2
    elif P <= 20.204:
        return - (3.69284e11 * P ** 4.7205) / \
          (P**5.7205 + 1.0361e8)**2
    else:
        return - (3.66344e24 * P**14.0333) / \
          (P**15.0333 + 4.60571e20)**2

def dD_g_dP(P):
    """Derivada em relacao a pressao da densidade do gas
    Recebe: P(MPa)"""
    if P <= .085 or P > 21.5:
        raise ValueError("Valor fora do range")
    elif P < 1.112:
        return (5.126076 *.9475862)/(P**(1-.9475862))
    elif P < 3.932:
        return 4.630832 * 1.038819 * P**0.038819
    elif P < 8.996:
        return 2.868721 * 1.252148 * P**0.252148
    elif P < 14.628:
        return .5497653 * 1.831182 * P**0.831182
    elif P <= 18.21:
        return 8.6791582e-3 * 3.176484 * P**2.176484
    elif P <= 20.253:
        return 3.5587113e-6 * 5.660939 * P**4.660939
    else:
        return 3.558734e-16 * 13.03774 * P**12.03774


def dh_l_dP(P):
    """Derivada em relacao a pressao da entalpia da agua
    Recebe: P(MPa)"""
    if P <= .075 or P > 21.7:
        raise ValueError("Valor fora do range")
    elif P < .942:
        return ((912.1779 * .2061637)/(P**(1-.2061637))) * 1000
    elif P < 4.02:
        return ((638.0621 * .2963192)/(P**(1-.2963192))) * 1000
    elif P < 9.964:
        return ((373.7665 * .4235532)/(P**(1-.4235532))) * 1000
    elif P < 16.673:
        return ((75.38673 * .8282384) / (P**(1-.8282384))) * 1000
    elif P < 20.396:
        return (.1150827 * 2.711412 * P*1.711412) * 1000
    else:
        return (9.1417257e-14*11.47287*P**10.47287) * 1000


def dh_g_dP(P):
    """Derivada em relacao a pressao da entalpia do gas
    Recebe: P(MPa)"""
    if P <= .075 or P > 21.55:
        raise ValueError("Valor fora do range")
    elif P <= .348:
        return (-4.0381938e-6 * 15.72364 * (3-P)**14.72364) * 1000
    elif P <= 1.248:
        return (.5767304 * 338.537 * exp(-1.66153 * P)) * 1000
    elif P <= 2.955:
        return (44.0973 - 15.672 * P) * 1000
    elif P <= 6.522:
        return (5.75386 - 2.69449 * P) * 1000
    elif P < 16.497:
        return (.206167 - 1.84384 * P) * 1000
    elif P < 20.193:
        return (86.3279 - 7.06435 * P) * 1000
    else:
        return (869.544 - 45.8504 * P) * 1000

def dT_sat_dP(P):
    """Derivada em relacao a pressao da temperatuda de saturacao da
        agua
    Recebe: P(MPa)"""
    if P < .07 or P > 21.85:
        raise ValueError("Valor fora do range")
    elif P < .359:
        return (236.2315 * .1784767) / (P **(1 - .1784767))
    elif P <= 1.676:
        return (207.9248 * .2092705) / (P **(1 - .2092705))
    elif P <= 8.511:
        return (185.0779 * .2323217) / (P ** (1 - .2323217))
    elif P < 17.69:
        return (195.1819 * .2241729) / (P ** (1 - .2241729))
    else:
        return (227.2963 * .201581) / (P **(1 - .201581))

def P_sat(T):
    """Pressao de saturacao para uma dada temperatura
    Recebe: T(K)
    Retorna: P(MPa)"""

    if T < 89.965 or T > 373.253:
        raise ValueError("Valor fora do range")
    elif T < 139.781:
        return ((T + 57) / 236.2315)**5.602972
    elif T < 203.662:
        return ((T + 28) / 207.9248)**4.778504
    elif T < 299.407:
        return ((T + 5) / 185.0779)**4.304376
    elif T < 355.636:
        return ((T + 16) / 195.1819)**4.460843
    else:
        return ((T + 50) / 227.2963)**4.960785
