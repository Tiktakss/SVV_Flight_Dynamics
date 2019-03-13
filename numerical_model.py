import numpy as np
import Cit_par as par
from aero_tools import Aero_Tools
from real_analytical_model import Analytical_Model

class Numerical_Model:
    def __init__(self):
        self.tools = Aero_Tools()
        self.amod = Analytical_Model()
        
    def v_dimless(self, v_t, v_t0):
        return (v_t - v_t0) / v_t0
    
    def D_c(self, dt, v_dimless):
        return par.c / (v_dimless * dt)
    
    def D_b(self, dt, v_dimless):
        return par.b / (v_dimless * dt)
    
    def EOM_sym(self, D_c):
        symm1 = [par.CXu - 2 * par.muc * D_c, par.CXa, par.CZ0, par.CXq]
        symm2 = [par.CZu, par.CZa + (par.CZadot - 2 * par.muc)*D_c, -par.CX0, par.CZq + 2 * par.muc]
        symm3 = [0, 0, - D_c, 1]
        symm4 = [par.Cmu, par.Cma + par.Cmadot * D_c, 0, par.Cmq - 2 * par.muc * par.KY2 * D_c]
        return np.asarray((symm1, symm2, symm3, symm4))
    
    def EOM_asym(self, D_b):
        asymm1 = [par.CYb + (par.CYbdot - 2*par.mub)*D_b, par.CL, par.CYp, par.CYr - 4*par.mub]
        asymm2 = [0, -0.5*D_b, 1, 0]
        asymm3 = [par.Clb, 0, par.Clp - 4*par.mub * par.KX2 * D_b, par.Clr + 4*par.mub * par.KXZ * D_b]
        asymm4 = [par.Cnb + par.Cnbdot, 0, par.Cnp + 4*par.mub * par.KXZ * D_b, par.Cnr - 4*par.mub * par.KZ2 * D_b]
        return np.asarray((asymm1, asymm2, asymm3, asymm4))
    
    def elev_defl_mat(self):
        vect = [-par.CXde, -par.CZde, 0, -par.Cmde]
        #print(np.transpose(vect))
        return np.transpose(vect)

    def Ps(self, v_t0):
        P1 = [-2 * par.muc * par.c / v_t0, 0, 0, 0]
        P2 = [0, (par.CZadot - 2 * par.muc) * par.c / v_t0, 0, 0]
        P3 = [0, 0, -par.c / v_t0, 0]
        P4 = [0, par.Cmadot * par.c / v_t0, 0, -2 * par.muc * par.KY2 * par.c / v_t0]
        #print(np.asarray((P1, P2, P3, P4)))
        return np.asarray((P1, P2, P3, P4))

    def Qs(self):
        Q1 = [-par.CXu, -par.CXa, -par.CZ0, 0]
        Q2 = [-par.CZu, -par.CZa, par.CX0, -(par.CZq + 2 * par.muc)]
        Q3 = [0, 0, 0, -1]
        Q4 = [-par.Cmu, -par.Cma, 0, -par.Cmq]
        #print(np.asarray((Q1, Q2, Q3, Q4)))
        return np.asarray((Q1, Q2, Q3, Q4))


    def Pa(self, v_t0):
        P1 = [(par.CYbdot -2 * par.mub)*par.b/v_t0, 0, 0, 0]
        P2 = [0, -0.5*par.b/v_t0, 0, 0]
        P3 = [0, 0, -4 * par.mub * par.KX2 * par.b/v_t0, 4 * par.mub * par.KXZ * par.b/v_t0]
        P4 = [par.Cnbdot * par.b/v_t0, 0, 4 * par.mub * par.KXZ * par.b/v_t0, -4 * par.mub * par.KZ2 * par.b/v_t0]
        return np.asarray((P1, P2, P3, P4))
    
    def Qa(self):
        Q1 = [-par.CYb, -par.CL, -par.CYp, -(par.CYr - 4*par.mub)]
        Q2 = [0, 0, -1, 0]
        Q3 = [-par.Clb, 0, -par.Clp, -par.Clr]
        Q4 = [-par.Cnb, 0, -par.Cnp, -par.Cnr]
        return np.asarray((Q1, Q2, Q3, Q4))
    
    def Ra(self):
        R1 = [-par.CYda, -par.CYdr, ]
        R2 = [0, 0]
        R3 = [-par.Clda, -par.Cldr]
        R4 = [-par.Cnda, -par.Cndr]
        return np.asarray((R1, R2, R3, R4))
    
    def As(self, v_t0):
        P_inv = np.linalg.inv(self.Ps(v_t0))
        Q_mat = self.Qs()
        A = np.matmul(P_inv,Q_mat)
        return A
    
    def Bs(self, v_t0):
        P_inv = np.linalg.inv(self.Ps(v_t0))
        delta_mat = self.elev_defl_mat()
        B = np.matmul(P_inv,delta_mat)
        return B
    
    def Aa(self, v_t0):
        P_inv = np.linalg.inv(self.Pa(v_t0))
        Q_mat = self.Qa()
        A = np.matmul(P_inv,Q_mat)
        return A
    
    def Ba(self, v_t0):
        P_inv = np.linalg.inv(self.Pa(v_t0))
        R_mat = self.Ra()
        B = np.matmul(P_inv,R_mat)
        return B

    def C(self):
        return np.identity(4)

    def Ds(self):
        return np.transpose(np.zeros(4))

    def Da(self):
        return np.zeros((4,2))

        
        
if __name__ == "__main__":
    model = Numerical_Model()
    
    v_ias = model.tools.kts_to_ms(1)
    alt = model.tools.ft_to_m(0)
    v_tas = model.tools.ias_to_tas(alt, v_ias)
    v_dimless = model.v_dimless(v_tas, v_tas+1)
    #print(v_dimless)
    D_c = model.D_c(1, v_dimless)
    D_b = model.D_b(1, v_dimless)
    
    sym = model.EOM_sym(D_c)
    asym = model.EOM_asym(D_b)
    
    eig_s = np.linalg.eig(sym)[0]
    eig_a = np.linalg.eig(asym)
    
    
    print(sym)
    print(eig_s)
    print()
    #print(asym)
    #print(eig_a)



    print(model.As(1))
#    print(model.Bs(100))
#    print()
    print(model.Aa(1))
#    print(model.Ba(100))
#    print()
#    print(model.C())
#    print(model.Ds())
#    print(model.Da())
    
    
    v_ref = 1
    s_eigen = np.linalg.eig(model.As(v_ref))[0] / par.c
#    print(model.amod.eigenv_short())
#    print(model.amod.eigenv_phugoid())
#    print('eigenvalues symm')
    print(s_eigen)
    s_eigen = np.linalg.eig(model.Aa(v_ref))[0] / par.b
    print('eigenvalues asymm')
    print(s_eigen)


    

