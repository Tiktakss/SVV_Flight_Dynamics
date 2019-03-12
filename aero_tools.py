import numpy as np
from math import *

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
        self.lbs = 0.453592         #kg
    
    def T_alt(self, h):
        return self.T0 + h * self.lapse
    
    def p_alt(self, h):
        return self.p0 * (self.T_alt(h) / self.T0)**(-self.g0 / (self.R * self.lapse))
    
    def a_alt(self, h):
        return np.sqrt(self.gamma * self.R * self.T_alt(h))
    
    def rho_alt(self, h):
        return self.p_alt(h) / (self.R * self.T_alt(h))

    def ft_to_m(self, ft):
        return self.foot * ft
    
    def kts_to_ms(self, kts):
        return kts * self.nm / 3600
    
    def ias_to_tas(self, h, v_ias):
        return v_ias * np.sqrt(self.rho0 / self.rho_alt(h))
    
    def calc_mach(self, h, v_cal): #h[m] and v_cal[m/s] speed the pilot reads 
        p = self.p0*(1+ (self.lapse*h)/self.T0)**(self.g0/(self.lapse*self.R))
        M = sqrt( (2/(self.gamma -1))*((1 + self.p0/0*(1+ (self.gamma -1)/(2*self.gamma)*self.rho0/self.p0*v_cal*v_cal)**(self.gamma/(self.gamma -1))-1)**((self.gamma - 1)/self.gamma)-1))
    


"""
put testing/debugging code in the if-statement below
it will only run if you run this python file (aero_tools.py)
"""
if __name__ == "__main__":
    tools = Aero_Tools()
    
    h = 1000
    print(h)
    print(tools.p_alt(h), 'Pa')
    print(tools.rho_alt(h), 'kg/m^3')