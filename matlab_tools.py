# -*- coding: utf-8 -*-
"""
Created on Wed Mar  6 09:54:48 2019

@author: Jeije
"""

import scipy.io as sio

class Matlab_Tools:
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



"""
put testing/debugging code in the if-statement below
it will only run if you run this python file (aero_tools.py)
"""
if __name__ == "__main__":
    sio.loadmat(FTISxprt-20180305_124437.mat)