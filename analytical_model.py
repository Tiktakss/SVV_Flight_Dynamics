import numpy as np
from Cit_par import Variables

class Analytical_Model:
    def __init__(self):
        self.v_t0 = 1           #stationary normal velocity
        self.var = Variables()
        
    def v_dimless(self, v_t):
        return (v_t - self.v_t0) / self.v_t0
    
    
    
    
if __name__ == "__main__":
    model = Analytical_Model()
    
    print(model.var.CXu)