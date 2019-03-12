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
        Y = -2 * par.muc * par.KY2 * par.CZa - (2 * par.muc + par.CZq) * par.Cmadot - (2 * par.muc - par.CZadot) * par.Cmq
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
    
    
if __name__ == "__main__":
    mod = Analytical_Model()
    print(mod.eigenv_short())
    print(mod.eigenv_phugoid())
    