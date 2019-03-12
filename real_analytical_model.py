import numpy as np
import Cit_par as par

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
    
if __name__ == "__main__":
    mod = Analytical_Model()
    v = 140
    vc = v/par.c
    vb = v/par.b
    print('\t', 'short period:')
    print(mod.eigenv_short())
    print(mod.half_time(mod.eigenv_short()[0][0],v)*vc)
    print('\t', 'phugoid:')
    print(mod.eigenv_phugoid())
    print(mod.half_time(mod.eigenv_phugoid()[0][0],v)*vc)
    print('\t', 'dutch roll:')
    print(mod.dutchr())
    print(mod.half_time2(mod.dutchr()[0][0],v)*vb)
    print('\t', 'aperiodic roll:')
    print(mod.aperroll())
    print(mod.half_time2(mod.aperroll(),v)*vb)
    print('\t', 'spiral:')
    print(mod.spiral())
    print(mod.half_time2(mod.spiral(),v)*vb)