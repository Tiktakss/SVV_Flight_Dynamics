#Chp0    = 0      	  # pressure altitude in the stationary flight condition [m]
#CV0     = 100           # true airspeed in the stationary flight condition [m/sec]
#Calpha0 = 0.04          # angle of attack in the stationary flight condition [rad]
#Cth0    = 0.0        # pitch angle in the stationary flight condition [rad]
#
## Aircraft mass
#Cm      = 6700            #Use def calc_aircraft_mass from aero tool
#
## aerodynamic properties
#Ce      = 0.7991242852322632            # Oswald factor [ ]
#CCD0    = 0.023220020475067445            # Zero lift drag coefficient [ ]
#CCLa    = 4.435334042960342            # Slope of CL-alpha curve [ ]
#
## Longitudinal stability
#CCma    = -0.7750212638973237            # longitudinal stabilty [ ]
#CCmde   = -1.6792127384442015       # elevator effectiveness [ ]
    
from aero_tools import Aero_Tools


tl = Aero_Tools()

t = 900

Chp0    = tl.calc_pressure_altitude(t)  
#print(Chp0,'alt')    	  # pressure altitude in the stationary flight condition [m]
CV0     = tl.calc_speed(t)                  # true airspeed in the stationary flight condition [m/sec]
Calpha0 = tl.calc_angle_of_attack(t)          # angle of attack in the stationary flight condition [rad]
Cth0    = tl.calc_pitch_angle(t)        # pitch angle in the stationary flight condition [rad]

# Aircraft mass
Cm      = tl.calc_aircraft_mass(t)    #Use def calc_aircraft_mass from aero tool

# aerodynamic properties
Ce      = 0.7991242852322632            # Oswald factor [ ]
CCD0    = 0.023220020475067445            # Zero lift drag coefficient [ ]
CCLa    = 4.435334042960342            # Slope of CL-alpha curve [ ]

# Longitudinal stability
CCma    = -0.7750212638973237            # longitudinal stabilty [ ]
CCmde   = -1.6792127384442015       # elevator effectiveness [ ]