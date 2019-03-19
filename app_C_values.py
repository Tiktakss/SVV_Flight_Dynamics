import Test_Rolijne as test

Chp0    = 0      	  # pressure altitude in the stationary flight condition [m]
CV0     = 100           # true airspeed in the stationary flight condition [m/sec]
Calpha0 = 0.04          # angle of attack in the stationary flight condition [rad]
Cth0    = 0.0        # pitch angle in the stationary flight condition [rad]

# Aircraft mass
Cm      = 6700            # mass [kg]

# aerodynamic properties
Ce      = 0.8            # Oswald factor [ ]
CCD0    = 0.04            # Zero lift drag coefficient [ ]
CCLa    = 5.084            # Slope of CL-alpha curve [ ]

# Longitudinal stability
CCma    = test.Cm_alpha            # longitudinal stabilty [ ]
CCmde   = test.Cm_delta            # elevator effectiveness [ ]

