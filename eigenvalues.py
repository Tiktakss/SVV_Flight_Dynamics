import numpy as np
import Cit_par as p

class EigenV:
    def __init__(self):
        a=1
    
    def poly(self):
        A = 4 * p.muc**2 * p.KY2 * (p.CZadot - 2 * p.muc)
        B = p.Cmadot * 2 * p.muc * (p.CZq + 2 * p.muc) - p.Cmq * 2 * p.muc * (p.CZadot - 2 * p.muc) \
        - 2 * p.muc * p.KY2 * (p.CXu * (p.CZadot- 2* p.muc)- 2 * p.muc * p.CZa)
        C = p.Cma * 2 * p.muc * (p.CZq + 2 * p.muc) - p.Cmadot * (2*p.muc * p.CX0 + p.CXu * (p.CZq + 2 * p.muc)) \
        + p.Cmq * (p.CXu * (p.CZadot - 2*p.muc) - 2*p.muc * p.CZa) + 2*p.muc * p.KY2 *(p.CXa * p.CZu - p.CZa * p.CXu)
        D = p.Cmu * (p.CXa * (p.CZq + 2*p.muc) - p.CZ0 * (p.CZadot - 2*p.muc)) - p.Cma * (2*p.muc * p.CX0 + p.CXu * (p.CZq + 2*p.muc)) \
        + p.Cmadot * (p.CX0 * p.CXu - p.CZ0 * p.CZu) + p.Cmq * (p.CXu * p.CZa - p.CZu * p.CXa)
        E = -p.Cmu * (p.CX0 * p.CXa + p.CZ0 * p.CZa) + p.Cma * (p.CX0 * p.CXu + p.CZ0 * p.CZu)
        return [A,B,C,D,E]
        #return [E,D,C,B,A]

    def half_time(self, xi, v):
        return np.log(0.5)*p.c/(xi * v)
    
    def D_c(self, dt, v_dimless):
        return p.c / (v_dimless * dt)
    
    def A_lect(self, v_0):
        d_c = self.D_c(1,v_0)
        A1 = [p.CXu - 2*p.muc * d_c,    p.CXa,                                  p.CZ0,      0]
        A2 = [p.CZu,                    p.CZa + (p.CZadot - 2*p.muc) * d_c,     -p.CX0,     p.CZq + 2*p.muc]
        A3 = [0,                        0,                                      -d_c,       1]
        A4 = [p.Cmu,                    p.Cma + p.Cmadot * d_c,                 0,          p.Cmq - 2*p.muc * p.KY2 * d_c]
        return np.asarray((A1,A2,A3,A4))
    
if __name__ == "__main__":
    eigen = EigenV()
    e=eigen.poly()
    roots = np.roots(e)*100/p.c
    #print(e)
    print(roots)
    print(eigen.half_time(np.real(roots),100))
    print()
    
    e2 = eigen.A_lect(1)
    roots2 = np.linalg.eig(e2)[0]
    print(e2)
    print(roots2)