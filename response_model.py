# -*- coding: utf-8 -*-
"""
Created on Wed Mar 13 10:56:04 2019

@author: Jeije
"""

from control.matlab import * 
import numpy as np
import Cit_par as par
from aero_tools import Aero_Tools
from real_analytical_model import Analytical_Model
from numerical_model import Numerical_Model

class Response:
    def __init__(self):
        self.p0 = 101325            #Pa
    


"""
put testing/debugging code in the if-statement below
it will only run if you run this python file (aero_tools.py)
"""
if __name__ == "__main__":
    resp = Response()
    model = Numerical_Model()
    
    
    v_ias = model.tools.kts_to_ms(161)
    alt = model.tools.ft_to_m(13250)
    v_tas = model.tools.ias_to_tas(alt, v_ias)
    v_dimless = model.v_dimless(v_tas, v_tas+1)
    
    D_c = model.D_c(0.1, v_dimless)
    D_b = model.D_b(0.1, v_dimless)
    
    sym = model.EOM_sym(D_c)
    asym = model.EOM_asym(D_b)
    
    print()
    print()
    


#    print(model.As(100))
#    print(model.Bs(100))
#    print()
#    print(model.Aa(100))
#    print(model.Ba(100))
#    print()
#    print(model.C())
#    print(model.Ds())
#    print(model.Da())
    
    
#    v_ref = 1
#    s_eigen = np.linalg.eig(model.As(v_ref))[0] / par.c
#    print(model.amod.eigenv_short())
#    print(model.amod.eigenv_phugoid())
#    print('eigenvalues symm')
#    print(s_eigen)
#    s_eigen = np.linalg.eig(model.Aa(v_ref))[0] / par.b
#    print('eigenvalues asymm')
#    print(s_eigen)