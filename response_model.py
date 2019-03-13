# -*- coding: utf-8 -*-
"""
Created on Wed Mar 13 10:56:04 2019

@author: Jeije
"""
import control
from control.matlab import * 
import numpy as np
import Cit_par as par
from aero_tools import Aero_Tools
from real_analytical_model import Analytical_Model
from numerical_model import Numerical_Model
import matplotlib.pyplot as plt

class Response:
    def __init__(self):
        self.p0 = 101325            #Pa
    


"""
put testing/debugging code in the if-statement below
it will only run if you run this python file (response_model.py)
"""
if __name__ == "__main__":
    resp = Response()
    model = Numerical_Model()
    
    
    v_ias = model.tools.kts_to_ms(161)
    alt = model.tools.ft_to_m(13250)
    v_tas = model.tools.ias_to_tas(alt, v_ias)
    v_dimless = model.v_dimless(v_tas, v_tas+1)
    
    A=np.matrix(model.As(v_tas))
    B=np.matrix(model.Bs(v_tas))
    C=np.matrix(model.C())
    D=np.matrix(model.Ds())
    A=np.transpose(A)
    B=np.transpose(B)
    C=np.transpose(C)
    D=np.transpose(D)
    
    
    
    print (A.shape,B.shape,C.shape,D.shape)
    sys=control.StateSpace(A,B,C,D)
    x0=0
    
    print (sys)
    
    T,yout, xout=control.step_response(sys,return_x=True,transpose=True)
    ax = plt.figure()
    ax.plot(T,yout)
