from aero_tools import Aero_Tools
import Cit_par as par

class Coefficients:
    def __init__(self):
        self.tools = Aero_Tools()
        self.S = par.S
        
    def rho_v2_s(self, h, v):
        rho = self.tools.rho_alt(h)
        v_tas = self.tools.ias_to_tas(h, v)
        return 0.5 * rho * v_tas**2 *self.S
    
    
    
if __name__ == "__main__":
    coef = Coefficients()
    
    #print(coef.rho_v2_s(3000,140))