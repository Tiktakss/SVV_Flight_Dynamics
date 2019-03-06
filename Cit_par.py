class Cit_Par:
    def __init__(self):
    
        # Citation 550 - Linear simulation
        
        # xcg = 0.25 * c
        
        # Stationary flight condition
        
        self.hp0    =       	      # pressure altitude in the stationary flight condition [m]
        self.V0     =             # true airspeed in the stationary flight condition [m/sec]
        self.alpha0 =             # angle of attack in the stationary flight condition [rad]
        self.th0    =             # pitch angle in the stationary flight condition [rad]
        
        # Aircraft mass
        self.m      =             # mass [kg]
        
        # aerodynamic properties
        self.e      =             # Oswald factor [ ]
        self.CD0    =             # Zero lift drag coefficient [ ]
        self.CLa    =             # Slope of CL-alpha curve [ ]
        
        # Longitudinal stability
        self.Cma    =             # longitudinal stabilty [ ]
        self.Cmde   =             # elevator effectiveness [ ]
        
        # Aircraft geometry
        
        self.S      = 30.00	          # wing area [m^2]
        self.Sh     = 0.2 * S         # stabiliser area [m^2]
        self.Sh_S   = Sh / S	          # [ ]
        self.lh     = 0.71 * 5.968    # tail length [m]
        self.c      = 2.0569	          # mean aerodynamic cord [m]
        self.lh_c   = lh / c	          # [ ]
        self.b      = 15.911	          # wing span [m]
        self.bh     = 5.791	          # stabilser span [m]
        self.A      = b ** 2 / S      # wing aspect ratio [ ]
        self.Ah     = bh ** 2 / Sh    # stabilser aspect ratio [ ]
        self.Vh_V   = 1	          # [ ]
        self.ih     = -2 * pi / 180   # stabiliser angle of incidence [rad]
        
        # Constant values concerning atmosphere and gravity
        
        self.rho0   = 1.2250          # air density at sea level [kg/m^3] 
        self.lambda = -0.0065         # temperature gradient in ISA [K/m]
        self.Temp0  = 288.15          # temperature at sea level in ISA [K]
        self.R      = 287.05          # specific gas constant [m^2/sec^2K]
        self.g      = 9.81            # [m/sec^2] (gravity constant)
        
        # air density [kg/m^3]  
        self.rho    = rho0 * power( ((1+(lambda * hp0 / Temp0))), (-((g / (lambda*R)) + 1)))   
        self.W      = m * g            # [N]       (aircraft weight)
        
        # Constant values concerning aircraft inertia
        
        self.muc    = m / (rho * S * c)
        self.mub    = m / (rho * S * b)
        self.KX2    = 0.019
        self.KZ2    = 0.042
        self.KXZ    = 0.002
        self.KY2    = 1.25 * 1.114
        
        # Aerodynamic constants
        
        self.Cmac   = 0                      # Moment coefficient about the aerodynamic centre [ ]
        self.CNwa   = CLa                    # Wing normal force slope [ ]
        self.CNha   = 2 * pi * Ah / (Ah + 2) # Stabiliser normal force slope [ ]
        self.depsda = 4 / (A + 2)            # Downwash gradient [ ]
        
        # Lift and drag coefficient
        
        self.CL = 2 * W / (rho * V0 ** 2 * S)              # Lift coefficient [ ]
        self.CD = CD0 + (CLa * alpha0) ** 2 / (pi * A * e) # Drag coefficient [ ]
        
        # Stabiblity derivatives  
        self.CX0    = W * sin(th0) / (0.5 * rho * V0 ** 2 * S)
        self.CXu    = -0.02792
        self.CXa    = -0.47966
        self.CXadot = +0.08330
        self.CXq    = -0.28170
        self.CXde   = -0.03728
        
        self.CZ0    = -W * cos(th0) / (0.5 * rho * V0 ** 2 * S)
        self.CZu    = -0.37616
        self.CZa    = -5.74340
        self.CZadot = -0.00350
        self.CZq    = -5.66290
        self.CZde   = -0.69612
        
        self.Cmu    = +0.06990
        self.Cmadot = +0.17800
        self.Cmq    = -8.79415
        
        self.CYb    = -0.7500
        self.CYbdot =  0     
        self.CYp    = -0.0304
        self.CYr    = +0.8495
        self.CYda   = -0.0400
        self.CYdr   = +0.2300
        
        self.Clb    = -0.10260
        self.Clp    = -0.71085
        self.Clr    = +0.23760
        self.Clda   = -0.23088
        self.Cldr   = +0.03440
        
        self.Cnb    =  +0.1348
        self.Cnbdot =   0     
        self.Cnp    =  -0.0602
        self.Cnr    =  -0.2061
        self.Cnda   =  -0.0120
        self.Cndr   =  -0.0939
