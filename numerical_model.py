import numpy as np
import Cit_par as p
from aero_tools import Aero_Tools
from real_analytical_model import Analytical_Model

from matlab_tools import Matlab_Tools
matlab = Matlab_Tools('FTISxprt-20190305_124649.mat')

#from control.matlab import * 

class Numerical_Model:
    def __init__(self):
        self.tools = Aero_Tools()
        self.amod = Analytical_Model()
        self.delta_t = 0.1
        
        
    def v_dimless(self, v_t, v_t0):
        return (v_t - v_t0) / v_t0
    
    def D_c(self, dt, v_dimless):
        return p.c / (v_dimless * dt)
    
    def D_b(self, dt, v_dimless):
        return p.b / (v_dimless * dt)
    
    def EOM_sym(self, D_c):
        symm1 = [p.CXu - 2 * p.muc * D_c, p.CXa, p.CZ0, p.CXq]
        symm2 = [p.CZu, p.CZa + (p.CZadot - 2 * p.muc)*D_c, -p.CX0, p.CZq + 2 * p.muc]
        symm3 = [0, 0, - D_c, 1]
        symm4 = [p.Cmu, p.Cma + p.Cmadot * D_c, 0, p.Cmq - 2 * p.muc * p.KY2 * D_c]
        return np.matrix((symm1, symm2, symm3, symm4))
    
    def EOM_asym(self, D_b):
        asymm1 = [p.CYb + (p.CYbdot - 2*p.mub)*D_b, p.CL, p.CYp, p.CYr - 4*p.mub]
        asymm2 = [0, -0.5*D_b, 1, 0]
        asymm3 = [p.Clb, 0, p.Clp - 4*p.mub * p.KX2 * D_b, p.Clr + 4*p.mub * p.KXZ * D_b]
        asymm4 = [p.Cnb + p.Cnbdot, 0, p.Cnp + 4*p.mub * p.KXZ * D_b, p.Cnr - 4*p.mub * p.KZ2 * D_b]
        return np.matrix((asymm1, asymm2, asymm3, asymm4))
    
    def elev_defl_mat(self):
        vect = [-p.CXde, -p.CZde, 0, -p.Cmde]
        #print(np.transpose(vect))
        return np.transpose(vect)

    def Ps(self, v_t0):
        P1 = [-2 * p.muc * p.c / v_t0,      0,                                      0,              0]
        P2 = [0,                            (p.CZadot - 2 * p.muc) * p.c / v_t0,    0,              0]
        P3 = [0,                            0,                                      -p.c / v_t0,    0]
        P4 = [0,                            p.Cmadot * p.c / v_t0,                  0,              -2 * p.muc * p.KY2 * p.c / v_t0]
        #print(np.matrix((P1, P2, P3, P4)))
        return np.matrix((P1, P2, P3, P4))

    def Qs(self, v_t0):
        Q1 = [-p.CXu,  -p.CXa,     -p.CZ0,     0]
        Q2 = [-p.CZu,  -p.CZa,     p.CX0,      -(p.CZq + 2 * p.muc)]
        Q3 = [0,       0,          0,          -1]
        Q4 = [-p.Cmu,  -p.Cma,     0,          -p.Cmq]
        #print(np.matrix((Q1, Q2, Q3, Q4)))
        return np.matrix((Q1, Q2, Q3, Q4))


    def Pa(self, v_t0):
        P1 = [(p.CYbdot -2 * p.mub)*p.b/v_t0, 0, 0, 0]
        P2 = [0, -0.5*p.b/v_t0, 0, 0]
        P3 = [0, 0, -4 * p.mub * p.KX2 * p.b/v_t0, 4 * p.mub * p.KXZ * p.b/v_t0]
        P4 = [p.Cnbdot * p.b/v_t0, 0, 4 * p.mub * p.KXZ * p.b/v_t0, -4 * p.mub * p.KZ2 * p.b/v_t0]
        return np.matrix((P1, P2, P3, P4))
    
    def Qa(self):
        Q1 = [-p.CYb, -p.CL, -p.CYp, -(p.CYr - 4*p.mub)]
        Q2 = [0, 0, -1, 0]
        Q3 = [-p.Clb, 0, -p.Clp, -p.Clr]
        Q4 = [-p.Cnb, 0, -p.Cnp, -p.Cnr]
        return np.matrix((Q1, Q2, Q3, Q4))
    
    def Ra(self):
        R1 = [-p.CYda, -p.CYdr, ]
        R2 = [0, 0]
        R3 = [-p.Clda, -p.Cldr]
        R4 = [-p.Cnda, -p.Cndr]
        return np.matrix((R1, R2, R3, R4))
    
    def As(self, v_t0):
        P_inv = np.linalg.inv(self.Ps(v_t0))
        Q_mat = self.Qs(v_t0)
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
        return np.matrix(np.identity(4))

    def Ds(self):
        return np.matrix(np.transpose(np.zeros(4)))

    def Da(self):
        return np.matrix(np.zeros((4,2)))
    
    def t_run(self,T):
        return np.arange(0,T,self.delta_t)
    
    def interpolate(self,T,manouvre):
        if manouvre == 'fugoid':
            start=matlab.fugoidstart
            time=matlab.fugoidtime
        elif manouvre=='ap_roll':
            start=matlab.ap_rollstart
            time=matlab.ap_rolltime
        elif manouvre=='sh_period':
            start=matlab.sh_periodstart
            time=matlab.sh_periodtime
        elif manouvre=='dutchR':
            start=matlab.dutchRstart
            time=matlab.dutchRtime
        elif manouvre=='dutchR_damp':
            start=matlab.dutchR_dampstart
            time=matlab.dutchR_damptime
        elif manouvre=='spiral':
            start=matlab.spiralstart
            time=matlab.spiraltime
        else:
            print ('invalid manouvre')
            start=0
        Xs = matlab.Xs(manouvre)
        de = matlab.getdata_at_time('delta_e',start,start+time)
        vt0 = matlab.getdata_at_time('Dadc1_tas',start,start+0.2)[0]
        u_hat=np.matrix(Xs[0][0])
        AoA=Xs[1][0]
        Theta=Xs[2][0]
        q=Xs[3][0]
        for t in range(1,len(self.t_run(time))):
            U_s = de[t]
            print ('8======D')
            DX_s = np.dot(self.As(vt0),Xs) + np.transpose(self.Bs(vt0)*U_s)
            Xs = Xs + DX_s*self.delta_t
            np.vstack((u_hat,Xs[0][0]))
            np.vstack((AoA,Xs[1][0]))
            np.vstack((Theta,Xs[2][0]))
            np.vstack((q,Xs[3][0]))
        print ('8======D~~~~')
        return u_hat, AoA, Theta, q



        
        
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

    v_ref = 100

    As_mat=model.As(v_ref)
#    As_mat[:,0]*=1/v_ref
#    As_mat[:,-1]*=p.c/v_ref
    As_eig=np.linalg.eig(As_mat)[0] #* v_ref/p.c
    
    Aa_mat=model.Aa(v_ref)
#    Aa_mat[:,-1]*=p.b*0.5/v_ref
#    Aa_mat[:,-2]*=p.b*0.5/v_ref
    Aa_eig=np.linalg.eig(Aa_mat)[0]
    
    print(As_mat)
    print(As_eig)
    print(model.amod.half_time(np.real(As_eig),v_ref))
#    print()
#    print(Aa_mat)
#    print(Aa_eig)
#    print(model.amod.half_time2(np.real(Aa_eig),v_ref))
    
    
#    print(model.Ba(1))
#    print()
#    print(model.C())
#    print(model.Ds())
#    print(model.Da())
    
    
    
    s_eigen = np.linalg.eig(model.As(v_ref))[0] / p.c
#    print(model.amod.eigenv_short())
#    print(model.amod.eigenv_phugoid())
#    print('eigenvalues symm')
#    print(s_eigen)
#    s_eigen = np.linalg.eig(model.Aa(v_ref))[0] / p.b
#    print('eigenvalues asymm')
#    print(s_eigen)


#    q = model.Qs()
#    print(q)
#    print(np.linalg.eig(q)[0])
    print (model.interpolate(7,'spiral'))
