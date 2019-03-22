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
import numpy as np
from math import *
from matlab_tools import Matlab_Tools
mat = Matlab_Tools('./FTISxprt-20190305_124649.mat')

class App_C:
    def __init__(self):
        a=1
        
    def calc_aircraft_mass(self, t_manouvre): #time in Seconds
        block_fuel = 4050.0 #lbs
        empty_weight = 9165.0 #lbs
        weight_people = (92 + 89 + 76.5 + 74 + 77 + 65 + 69 + 72.5 + 106)/ 0.453592 #lbs
        fuel_used_left = mat.getdata_at_time('lh_engine_FU', t_manouvre, t_manouvre+1)
        fuel_used_right = mat.getdata_at_time('rh_engine_FU', t_manouvre, t_manouvre+1)
        fuel_used = fuel_used_right + fuel_used_left
        fuel_used_avg = sum(fuel_used)/len(fuel_used)
        mass = block_fuel + empty_weight + weight_people - fuel_used_avg
        
        return mass* 0.453592 #kg
    
    def calc_pressure_altitude(self, t_manouvre): #Time in seconds
        height = mat.getdata_at_time('Dadc1_alt',t_manouvre, t_manouvre + 1)
        height_avg = sum(height)/len(height)
        return height_avg*0.3048
    
    def calc_speed(self, t_manouvre): #Time in Seconds
        speed = mat.getdata_at_time('Dadc1_tas',t_manouvre, t_manouvre + 1)
        speed_avg = sum(speed)/len(speed)
        return speed_avg*  1852 / 3600 #True airspeed m/s
    
    def calc_angle_of_attack(self, t_manouvre):#time in seconds
        angle = mat.getdata_at_time('vane_AOA',t_manouvre, t_manouvre + 1)
        angle_avg = sum(angle)/len(angle)
        return np.radians(angle_avg)#rad
    
    def calc_pitch_angle(self, t_manouvre):#time ins seconds
        pitch = mat.getdata_at_time('Ahrs1_Pitch',t_manouvre, t_manouvre + 1)
        pitch_avg = sum(pitch)/len(pitch)
        return np.radians(pitch_avg) #rad

    
    def values(self):
        #tl = App_C()
        
        t = 900
        
        
        
        Chp0    = self.calc_pressure_altitude(t)  
        #print(Chp0,'alt')    	  # pressure altitude in the stationary flight condition [m]
        CV0     = self.calc_speed(t)                  # true airspeed in the stationary flight condition [m/sec]
        Calpha0 = self.calc_angle_of_attack(t)          # angle of attack in the stationary flight condition [rad]
        Cth0    =self.calc_pitch_angle(t)        # pitch angle in the stationary flight condition [rad]
        
        # Aircraft mass
        Cm      =self.calc_aircraft_mass(t)    #Use def calc_aircraft_mass from aero tool
        
        # aerodynamic properties
        Ce      = 0.7991242852322632            # Oswald factor [ ]
        CCD0    = 0.023220020475067445            # Zero lift drag coefficient [ ]
        CCLa    = 4.435334042960342            # Slope of CL-alpha curve [ ]
        
        # Longitudinal stability
        CCma    = -0.7750212638973237            # longitudinal stabilty [ ]
        CCmde   = -1.6792127384442015       # elevator effectiveness [ ]
    
        return Chp0,CV0,Calpha0,Cth0,Cm,Ce,CCD0,CCLa,CCma,CCmde
    
if __name__ == "__main__":
    print('was ist los')