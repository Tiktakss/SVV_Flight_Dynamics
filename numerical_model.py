import numpy as np
import Cit_par as par
from aero_tools import Aero_Tools
from real_analytical_model import Analytical_Model
#from control.matlab import * 

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
        return np.matrix((symm1, symm2, symm3, symm4))
    
    def EOM_asym(self, D_b):
        asymm1 = [par.CYb + (par.CYbdot - 2*par.mub)*D_b, par.CL, par.CYp, par.CYr - 4*par.mub]
        asymm2 = [0, -0.5*D_b, 1, 0]
        asymm3 = [par.Clb, 0, par.Clp - 4*par.mub * par.KX2 * D_b, par.Clr + 4*par.mub * par.KXZ * D_b]
        asymm4 = [par.Cnb + par.Cnbdot, 0, par.Cnp + 4*par.mub * par.KXZ * D_b, par.Cnr - 4*par.mub * par.KZ2 * D_b]
        return np.matrix((asymm1, asymm2, asymm3, asymm4))
    
    def elev_defl_mat(self):
        vect = [-par.CXde, -par.CZde, 0, -par.Cmde]
        #print(np.transpose(vect))
        return np.transpose(vect)

    def Ps(self, v_t0):
        P1 = [-2 * par.muc * par.c / v_t0, 0, 0, 0]
        P2 = [0, (par.CZadot - 2 * par.muc) * par.c / v_t0, 0, 0]
        P3 = [0, 0, -par.c / v_t0, 0]
        P4 = [0, par.Cmadot * par.c / v_t0, 0, -2 * par.muc * par.KY2 * par.c / v_t0]
        #print(np.matrix((P1, P2, P3, P4)))
        return np.matrix((P1, P2, P3, P4))

    def Qs(self):
        Q1 = [-par.CXu, -par.CXa, -par.CZ0, 0]
        Q2 = [-par.CZu, -par.CZa, par.CX0, -(par.CZq + 2 * par.muc)]
        Q3 = [0, 0, 0, -1]
        Q4 = [-par.Cmu, -par.Cma, 0, -par.Cmq]
        #print(np.matrix((Q1, Q2, Q3, Q4)))
        return np.matrix((Q1, Q2, Q3, Q4))


    def Pa(self, v_t0):
        P1 = [(par.CYbdot -2 * par.mub)*par.b/v_t0, 0, 0, 0]
        P2 = [0, -0.5*par.b/v_t0, 0, 0]
        P3 = [0, 0, -4 * par.mub * par.KX2 * par.b/v_t0, 4 * par.mub * par.KXZ * par.b/v_t0]
        P4 = [par.Cnbdot * par.b/v_t0, 0, 4 * par.mub * par.KXZ * par.b/v_t0, -4 * par.mub * par.KZ2 * par.b/v_t0]
        return np.matrix((P1, P2, P3, P4))
    
    def Qa(self):
        Q1 = [-par.CYb, -par.CL, -par.CYp, -(par.CYr - 4*par.mub)]
        Q2 = [0, 0, -1, 0]
        Q3 = [-par.Clb, 0, -par.Clp, -par.Clr]
        Q4 = [-par.Cnb, 0, -par.Cnp, -par.Cnr]
        return np.matrix((Q1, Q2, Q3, Q4))
    
    def Ra(self):
        R1 = [-par.CYda, -par.CYdr, ]
        R2 = [0, 0]
        R3 = [-par.Clda, -par.Cldr]
        R4 = [-par.Cnda, -par.Cndr]
        return np.matrix((R1, R2, R3, R4))
    
    def As(self, v_t0):
        P_inv = np.linalg.inv(self.Ps(v_t0))
        Q_mat = self.Qs()
        A = np.matmul(-P_inv,Q_mat)
        return A
    
    def Bs(self, v_t0):
        P_inv = np.linalg.inv(self.Ps(v_t0))
        delta_mat = self.elev_defl_mat()
        B = np.matmul(P_inv,delta_mat)
        return B
    
    def Aa(self, v_t0):
        P_inv = np.linalg.inv(self.Pa(v_t0))
        Q_mat = self.Qa()
        A = np.matmul(-P_inv,Q_mat)
        return A
    
    def Ba(self, v_t0):
        P_inv = np.linalg.inv(self.Pa(v_t0))
        R_mat = self.Ra()
        B = np.matmul(P_inv,R_mat)
        return B

    def C(self):
        return np.matrix(np.identity(4))

    def Ds(self):
        return np.matrix(np.transpose(np.zeros(4)))

    def Da(self):
        return np.matrix(np.zeros((4,2)))

    def Xs(self,manouvre):
        

        
        
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
    
    
#    print(sym)
#    print(eig_s)
    #print(np.poly(sym))
    #print(asym)
    #print(eig_a)

    v_ref = 1

    As_mat=model.As(1)
    As_mat[:,-1]*=par.c/v_ref
    Aa_mat=model.Aa(1)
    Aa_mat[:,-1]*=par.b*0.5/v_ref
    Aa_mat[:,-2]*=par.b*0.5/v_ref
    
    print(As_mat)
#    print(model.Bs(1))
    print(np.linalg.eig(As_mat)[0])
    print()
    print(Aa_mat)
    print(np.linalg.eig(Aa_mat)[0])
#    print(model.Ba(1))
#    print()
#    print(model.C())
#    print(model.Ds())
#    print(model.Da())
    
    
    
    s_eigen = np.linalg.eig(model.As(v_ref))[0] / par.c
#    print(model.amod.eigenv_short())
#    print(model.amod.eigenv_phugoid())
#    print('eigenvalues symm')
#    print(s_eigen)
#    s_eigen = np.linalg.eig(model.Aa(v_ref))[0] / par.b
#    print('eigenvalues asymm')
#    print(s_eigen)


#    q = model.Qs()
#    print(q)
#    print(np.linalg.eig(q)[0])

