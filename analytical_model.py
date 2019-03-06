import numpy as np
import Cit_par as par

class Analytical_Model:
    def __init__(self):
        self.v_t0 = 2           #stationary normal velocity
        
        
    def v_dimless(self, v_t):
        return (v_t - self.v_t0) / self.v_t0
    
    def D_c(self, dt):
        return par.c / (self.v_dimless(1) * dt)
    
    def symm_mat(self, dt):
        symm1 = [par.CXu - 2 * par.muc * self.D_c(dt), par.CXa, par.CZ0, par.CXq]
        symm2 = [par.CZu, par.CZa + (par.CZadot - 2 * par.muc)*self.D_c(dt), -par.CX0, par.CZq + 2 * par.muc]
        symm3 = [0, 0, -self.D_c(dt), 1]
        symm4 = [par.Cmu, par.Cma + par.Cmadot * self.D_c(dt), 0, par.Cmq - 2 * par.muc * par.KY2 * self.D_c(dt)]
        return np.asarray((symm1, symm2, symm3, symm4))
    
    
    
if __name__ == "__main__":
    model = Analytical_Model()
    print(model.symm_mat(0.1))
    