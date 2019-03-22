import numpy as np
from math import *
from matlab_tools import Matlab_Tools
mat = Matlab_Tools('./FTISxprt-20190305_124649.mat')


class Aero_Tools:
    def __init__(self):
        self.p0 = 101325            #Pa
        self.g0 = 9.80665           #m/s^2
        self.T0 = 288.15            #K
        self.rho0 = 1.225           #kg/m^3
        self.lapse = -6.5 * 10**(-3)  #K/m
        self.foot = 0.3048          #m
        self.nm = 1852              #m
        self.R = 287                #? gas constant
        self.gamma = 1.4            #gas ratio
        self.lbs = 0.453592         #kg
        self.mu = 16.9e-6              #Pa s Dynamics viscosity
    
    def T_alt(self, h):
        return self.T0 + h * self.lapse
    
    def p_alt(self, h):
        return self.p0 * (self.T_alt(h) / self.T0)**(-self.g0 / (self.R * self.lapse))
    
    def a_alt(self, h):
        return np.sqrt(self.gamma * self.R * self.T_alt(h))
    
    def rho_alt(self, h):
        return self.p_alt(h) / (self.R * self.T_alt(h))

    def ft_to_m(self, ft):
        return self.foot * ft
    
    def kts_to_ms(self, kts):
        return kts * self.nm / 3600
    
    def ias_to_tas(self, h, v_ias):
        return v_ias * np.sqrt(self.rho0 / self.rho_alt(h))
    
    def calc_pressure(self, h): #static pressure
        return self.p0*(1 + (self.lapse*h)/self.T0)**(-self.g0/(self.lapse*self.R))
    
    def calc_mach(self, h, v_cal): #h[m] and v_cal[m/s] speed the pilot reads 
        p = self.p0*(1 + (self.lapse*h)/self.T0)**(-self.g0/(self.lapse*self.R))
        M = sqrt((2.0/(self.gamma -1.0))*((1.0 \
                 + (self.p0/p)*((1.0+ ((self.gamma \
                   -1.0)/(2.0*self.gamma))*(self.rho0/self.p0)*v_cal*v_cal)**(self.gamma/(self.gamma \
                    -1.0))-1.0))**((self.gamma \
            - 1.0)/self.gamma)-1.0))
        return M
    
    def calc_temp(self, Tm , M ): #static temperature
        return Tm/(1 + M*M*(self.gamma-1))
    
    def calc_re(self, rho, speed, length):
        return (rho * speed * length)/(self.mu)
    
    def calc_aircraft_mass(self, t_manouvre): #time in Seconds
        block_fuel = 4050.0 #lbs
        empty_weight = 9165.0 #lbs
        weight_people = (92 + 89 + 76.5 + 74 + 77 + 65 + 69 + 72.5 + 106)/self.lbs #lbs
        fuel_used_left = mat.getdata_at_time('lh_engine_FU', t_manouvre, t_manouvre+1)
        fuel_used_right = mat.getdata_at_time('rh_engine_FU', t_manouvre, t_manouvre+1)
        fuel_used = fuel_used_right + fuel_used_left
        fuel_used_avg = sum(fuel_used)/len(fuel_used)
        mass = block_fuel + empty_weight + weight_people - fuel_used_avg
        
        return mass*self.lbs #kg
    
    def calc_pressure_altitude(self, t_manouvre): #Time in seconds
        height = mat.getdata_at_time('Dadc1_alt',t_manouvre, t_manouvre + 1)
        height_avg = sum(height)/len(height)
        return height_avg*self.foot
    
    def calc_speed(self, t_manouvre): #Time in Seconds
        speed = mat.getdata_at_time('Dadc1_tas',t_manouvre, t_manouvre + 1)
        speed_avg = sum(speed)/len(speed)
        return speed_avg* self.nm / 3600 #True airspeed m/s
    
    def calc_angle_of_attack(self, t_manouvre):#time in seconds
        angle = mat.getdata_at_time('vane_AOA',t_manouvre, t_manouvre + 1)
        angle_avg = sum(angle)/len(angle)
        return np.radians(angle_avg)#rad
    
    def calc_pitch_angle(self, t_manouvre):#time ins seconds
        pitch = mat.getdata_at_time('Ahrs1_Pitch',t_manouvre, t_manouvre + 1)
        pitch_avg = sum(pitch)/len(pitch)
        return np.radians(pitch_avg) #rad
       

"""
put testing/debugging code in the if-statement below
it will only run if you run this python file (aero_tools.py)
"""
if __name__ == "__main__":
    tools = Aero_Tools()
    
    h = 1000
    print(h)
    print(tools.p_alt(h), 'Pa')
    print(tools.rho_alt(h), 'kg/m^3')
