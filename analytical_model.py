import numpy as np
import Cit_par as par
from aero_tools import Aero_Tools

class Analytical_Model:
    def __init__(self):
        self.tools = Aero_Tools()
        
    def v_dimless(self, v_t, v_t0):
        return (v_t - v_t0) / v_t0
    
    def D_c(self, dt, v_dimless):
        return par.c / (v_dimless * dt)
    
    def symm_mat(self, D_c):
        symm1 = [par.CXu - 2 * par.muc * D_c, par.CXa, par.CZ0, par.CXq]
        symm2 = [par.CZu, par.CZa + (par.CZadot - 2 * par.muc)*D_c, -par.CX0, par.CZq + 2 * par.muc]
        symm3 = [0, 0, - D_c, 1]
        symm4 = [par.Cmu, par.Cma + par.Cmadot * D_c, 0, par.Cmq - 2 * par.muc * par.KY2 * D_c]
        return np.asarray((symm1, symm2, symm3, symm4))
    
    
    
if __name__ == "__main__":
    model = Analytical_Model()
    
    v_ias = model.tools.kts_to_ms(161)
    alt = model.tools.ft_to_m(13250)
    v_tas = model.tools.ias_to_tas(alt, v_ias)
    print(alt,v_tas)
    v_dimless = model.v_dimless(v_tas, v_tas+1)
    D_c = model.D_c(0.1, v_dimless)
    print(model.symm_mat(D_c))