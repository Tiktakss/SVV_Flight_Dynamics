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
    
    def elev_defl_mat(self):
        vect = [-par.CXde, -par.CZde, 0, -par.Cmde]
        #print(np.transpose(vect))
        return np.transpose(vect)

    def P(self, v_t0):
        P1 = [-2 * par.muc * par.c / v_t0, 0, 0, 0]
        P2 = [0, (par.CZadot - 2 * par.muc) * par.c / v_t0, 0, 0]
        P3 = [0, 0, -par.c / v_t0, 0]
        P4 = [0, par.Cmadot * par.c / v_t0, 0, -2 * par.muc * par.KY2 * par.c / v_t0]

        #print(np.asarray((P1, P2, P3, P4)))
        return np.asarray((P1, P2, P3, P4))

    
    def Q(self):
        Q1 = [-par.CXu, -par.CXy, -par.CXz0, 0]
        Q2 = [-par.CZu, -par.CZa, par.CX0, -(par.CZq * 2 * par.muc)]
        Q3 = [0, 0, 0, -1]
        Q4 = [-par.Cmu, -par.Cma, 0, -par.Cmq]

        #print(np.asarray((Q1, Q2, Q3, Q4)))
        return np.asarray((Q1, Q2, Q3, Q4))
    
    def A(self, v_t0):
        A = np.matmul(np.linalg.inv(self.P(v_t0)),self.Q)
        return A
    
    def B(self, v_t0):
        B = np.matmul(np.linalg.inv(self.P(v_t0)),self.elev_defl_mat)
        return B
    
    def C(self):
        return np.identity(4)
        
    def Ds(self):
        return np.transpose(np.zeros(4))
    
    def Da(self):
        return np.zeros((4,2))
    
if __name__ == "__main__":
    model = Analytical_Model()
    
    v_ias = model.tools.kts_to_ms(161)
    alt = model.tools.ft_to_m(13250)
    v_tas = model.tools.ias_to_tas(alt, v_ias)
    #print(alt,v_tas)
    v_dimless = model.v_dimless(v_tas, v_tas+1)
    D_c = model.D_c(0.1, v_dimless)
    #print(model.symm_mat(D_c))
    #print(model.elev_defl_mat())

#    print(model.As(100))
#    print(model.Bs(100))
#    print()
#    print(model.Aa(100))
#    print(model.Ba(100))
#    print()
#    print(model.C())
#    print(model.Ds())
#    print(model.Da())
    
    
    v_ref = 1
    s_eigen = np.linalg.eig(model.As(v_ref))
    print('eigenvalues symm')
    print(s_eigen)
    s_eigen = np.linalg.eig(model.Aa(v_ref))[0]
    print('eigenvalues asymm')
    print(s_eigen)


    