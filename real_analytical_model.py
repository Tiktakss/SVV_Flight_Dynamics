import numpy as np
import Cit_par as par
from numerical_model import Numerical_Model

class Analytical_Model:
    def __init__(self):
        a=1
    """
    Sammary 4 FD 2.3.1 Short period motion
    """
    def eigenv_short(self):
        X = 2 * par.muc * par.KY2 * (2* par.muc - par.CZadot)
        Y = -2 * par.muc * par.KY2 * par.CZa - (2 * par.muc + par.CZq) * par.Cmadot - \
        (2 * par.muc - par.CZadot) * par.Cmq
        Z = par.CZa * par.Cmq - (2 * par.muc + par.CZq) * par.Cma
        
        L_Re = -Y/(2*X)
        L_Im = np.sqrt(4*X*Z - Y**2) / (2*X)
        L1 = [L_Re, L_Im]
        L2 = [L_Re, -L_Im]
        return L1, L2
    
    def eigenv_phugoid(self):
        X = 2 * par.muc * (par.CZa * par.Cmq - 2 * par.muc * par.Cma)
        Y = 2* par.muc * (par.CXu * par.Cma - par.Cmu * par.CXa) + par.Cmq * (par.CZu * par.CXa - par.CXu * par.CZa)
        Z = par.CZ0 * (par.Cmu * par.CZa - par.CZu * par.Cma)
        
        L_Re = -Y/(2*X)
        L_Im = np.sqrt(4*X*Z - Y**2) / (2*X)
        L1 = [L_Re, L_Im]
        L2 = [L_Re, -L_Im]
        return L1, L2
    
    def dutchr(self):
        L_Re = (par.Cnr + 2 * par.KZ2 * par.CYb) / (8*par.mub * par.KZ2)
        L_Im = np.sqrt(64 * par.KZ2 * (4*par.mub * par.Cnb + par.CYb * par.Cnr) - 4 * \
                       (par.Cnr + 2*par.KZ2 * par.CYb)**2) / (16*par.mub * par.KZ2)
        L1 = [L_Re, L_Im]
        L2 = [L_Re, -L_Im]
        return L1, L2
    
    def aperroll(self):
        return par.Clp / (4*par.mub * par.KX2)
    
    def spiral(self):
        X = 2 * par.CL * (par.Clb * par.Cnr - par.Cnb * par.Clr)
        Y = par.Clp * (par.CYb * par.Cnr + 4 *par.mub * par.Cnb) - par.Cnp *(par.CYb * par.Clr + 4*par.mub * par.Clb)
        return X/Y
    
    def half_time(self, xi, v):
        return np.log(0.5)*par.c/(xi * v)

    def half_time2(self, xi, v):
        return np.log(0.5)*par.b/(xi * v)
    
    def period_s(self, eta, v):
        return (2*np.pi*par.c)/(eta*v)
    
    def period_a(self, eta, v):
        return (2*np.pi*par.b)/(eta*v)
    
if __name__ == "__main__":
    amod = Analytical_Model()
    num = Numerical_Model()
    
    v = 100
    vc = v/par.c
    vb = v/par.b
    vc =1
    vb =2
    
    print('\t', 'SYMMETRIC')
    As_mat=num.As(v)
    As_eig=np.linalg.eig(As_mat)[0] * par.c/v
    #print(As_mat)
    print(As_eig)
    print(amod.half_time(np.real(As_eig),v))
    
    print('\t', 'ASYMMETRIC')
    Aa_mat=num.Aa(v)
    Aa_eig=np.linalg.eig(Aa_mat)[0] * 0.5*par.b/v
    print(Aa_mat)
    print(Aa_eig)
    print(amod.half_time2(np.real(Aa_eig),v))
    print()
    
    print('\t', 'short period:')
    print(amod.eigenv_short())
    print(amod.half_time(amod.eigenv_short()[0][0],v)*vc)
    
    
    print('\t', 'phugoid:')
    print(amod.eigenv_phugoid())
    print(amod.half_time(amod.eigenv_phugoid()[0][0],v)*vc)
    
    
    
    print('\t', 'dutch roll:')
    print(amod.dutchr())
    print(amod.half_time2(amod.dutchr()[0][0],v)*vb)
    
    
    
    print('\t', 'aperiodic roll:')
    print(amod.aperroll())
    print(amod.half_time2(amod.aperroll(),v)*vb)
    
    
    
    print('\t', 'spiral:')
    print(amod.spiral())
    print(amod.half_time2(amod.spiral(),v)*vb)
    
    
    