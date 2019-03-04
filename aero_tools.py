import numpy as np

class Aero_Tools:
    def __init__(self):
        self.p0 = 101325            #Pa
        self.g0 = 9.80665           #m/s^2
        self.T0 = 288.15            #K
        self.rho0 = 1.225           #kg/m^3
        self.lapse = -6.5 * 10**-3  #K/m
        self.foot = 0.3048          #m
        self.nm = 1852              #m
        self.R = 287                #? gas constant
        self.gamma = 1.4            #gas ratio
    
    def T_alt(self, h):
        return self.T0 + h * self.lapse
    
    def p_alt(self, h):
        return self.p0 * (self.T_alt(h) / self.T0)**(-self.g0 / (self.R * self.lapse))
    
    def a_alt(self, h):
        return np.sqrt(self.gamma * self.R * self.T_alt(h))


"""
put testing/debugging code in the if-statement below
it will only run if you run this python file (aero_tools.py)
"""
if __name__ == "__main__":
    tools = Aero_Tools()
    
    h = 1000
    print(tools.p_alt(h), 'Pa')
    print(tools.a_alt(h), 'm/s')