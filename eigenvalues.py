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

if __name__ == "__main__":
    eigen = EigenV()
    e=eigen.poly()
    roots = np.polynomial.polynomial.polyroots(e)
    print(e)
    print(roots)