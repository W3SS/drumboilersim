#-*- coding: utf-8 -*-


"""Controladores discretos. Todos tem a seguinte forma:

            +     error   _____________  out    _______      curr_value
setpoint --->( )-------->| Controlador |------>|Sistema|---o----->
             -^          |_____________|       |_______|   |
              |____________________________________________|

"""

import time

class PIDController:
    """Controlador PID.

    INPUT:
     > constantes  do PID (K_p, K_i, K_d)
     > Setpoint (no caso sempre será fixo)
     > Intervalos do integrador (min_int, max_int)
    """
    def __init__(self, k_p, k_i, k_d, setpoint, min_integral,
                 max_integral, stepsize, eps=1e-7):
        self.eps = eps
        self.stepsize = stepsize

        self.integral = 0


        self.setpoint = setpoint
        self.last_error = 0 # RP

        self.k_p = k_p
        self.k_i = k_i
        self.k_d = k_d

        self.min_integral = min_integral
        self.max_integral = max_integral

        self.out = 0

        self.error = 0
        self.p_port = 0
        self.i_port = 0
        self.d_port = 0




    def crossed_zero(self):
        """Metodo para descobrir se o erro cruzou zero."""
        return (
            (abs(self.error) < self.eps or abs(self.last_error) < self.eps)
            or (self.error > self.eps and self.last_error < self.eps)
            or (self.error < self.eps and self.last_error > self.eps))

    def step(self, curr_value):
        """Passo do controlador.
        Atualiza output de acordo com entrada"""

        self.error = self.setpoint - curr_value


        self.p_port = self.k_p * self.error
        self.i_port = self.k_i * self.integral
        self.d_port = self.k_d * (self.error - self.last_error) / self.stepsize


        self.out = self.p_port + self.i_port + self.d_port

        self.last_error = self.error

        self.integral = self.integral + self.error * self.stepsize

        # mantendo dentro dos limites
        self.integral = min(self.integral, self.max_integral)
        self.integral = max(self.integral, self.min_integral)



class PController(PIDController):
    """Controlador proporcional. Mesmo coisa de zerar constantes K_i e
    K_d do PID.

    INPUT:
     > constantes  K_p
     > Setpoint (no caso sempre será fixo)
    """
    def __init__(self, k_p, setpoint, stepsize):
        super().__init__(k_p, 0, 0, setpoint, 0, 0, stepsize)


class PIController(PIDController):
    """Controlador PI. Mesmo coisa de zerar constante K_d do PID.

    INPUT:
     > constantes  K_p e K_i
     > Setpoint (no caso sempre será fixo)
     > Intervalos do integrador (min_int, max_int)
    """
    def __init__(self, k_p, k_i, setpoint, min_int, max_int, stepsize):
        super().__init__(k_p, k_i, 0, setpoint, min_int, max_int, stepsize)


class PDController(PIDController):
    """Controlador PD. Mesmo coisa de zerar constante K_i do PID.

    INPUT:
     > constantes  K_p e K_d
     > Setpoint (no caso sempre será fixo)
    """
    def __init__(self, k_p, k_d, setpoint, stepsize):
        super().__init__(k_p, 0, 0, setpoint, 0, 0, stepsize)
