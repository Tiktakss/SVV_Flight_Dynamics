from math import pi
import matplotlib.pyplot as plt
import numpy as np
import Cit_par as par

#import classes
from aero_tools import Aero_Tools
aero = Aero_Tools()
from excel_tools import import_excel
excel = import_excel('./Post_Flight_Datasheet_03_05_V3.xlsx') #update with our file
from matlab_tools import Matlab_Tools
matlab = Matlab_Tools('./FTISxprt-20190305_124649.mat')

#inputs
blockfuel       = 4050.0 #lbs #obtained from written data sheet
empty_weight    = 9165.0 #lbs #obtained from Mass & Balance report
gravity = par.g #m/s^2
surface = par.S #m^2 #obtained from reader
Cd0 = par.CD0 # #obtained from reader
e = par.e #obtained from reader
b = par.b #span obtained from reader #m
length = 600 *0.0254
A = b*b/surface #aspect ratio


#obtain data for Cl-Cd plot
weight_people = sum(import_excel.weights(excel))/0.453592 #lbs
total_weight = weight_people + blockfuel + empty_weight

#time stamps plots
t1 = 18*60 + 50. #seconds
t2 = 21*60 + 33. #seconds
t3 = 25*60 + 30. #seconds
t4 = 27*60 + 29. #seconds
t5 = 29*60 + 3.  #seconds
t6 = 31*60 + 14. #seconds
dt = 0.5          #seconds

time = [t1, t2, t3, t4, t5, t6]

#create emoty lists for plots
C_l = [] #lift coefficient
C_d = [] #drag coefficient
alpha = [] #angle of attack
C_d_update = []

for i in range(len(time)):
    fuel_left = matlab.getdata_at_time('lh_engine_FU',time[i], time[i] + dt)
    fuel_left_avg = (sum(fuel_left))/(len(fuel_left))
    fuel_right = matlab.getdata_at_time('rh_engine_FU',time[i], time[i] + dt)
    fuel_right_avg = (sum(fuel_right))/(len(fuel_right))
    fuel_total = fuel_left_avg + fuel_right_avg

    weight_lbs = total_weight - fuel_total #weight in lbs
    weight_kg = weight_lbs * 0.453592 #weight in kg
    weight_n = weight_kg*gravity #weight inNewon
    
    height = matlab.getdata_at_time('Dadc1_alt', time[i], time[i ]+ dt)
    h_ft = (sum(height))/(len(height))
    h_m = aero.ft_to_m(h_ft) #height in m
    density = aero.rho_alt(h_m) #density kg/m^3
    
    speed = matlab.getdata_at_time('Dadc1_tas', time[i], time[i] + dt)
    speed_kts = (sum(speed))/(len(speed))
    speed_ms = aero.kts_to_ms(speed_kts)
    
    lift = (2*weight_n)/(density*surface*speed_ms**2)
    C_l.append(lift)
    
    drag = Cd0 +(lift**2)/(pi*A*e)
    C_d.append(drag)
    
    angle = matlab.getdata_at_time('vane_AOA', time[i], time[i] + dt)
    aoa = (sum(angle))/(len(angle)) #angle of attack #degrees
    alpha.append(aoa)

#Update OSwald factor
a  = (C_l[-1] - C_l[0])/(alpha[-1] - alpha[0])
a0 = 0.1097
e_better = 1/(pi*A) * 57.3 * a0 /(a0/a -1)

for i in range(len(time)): 
    drag_new = Cd0 +(C_l[i]**2)/(pi*A*e_better)
    C_d_update.append(drag_new)


#Trim Curve
t1_trim = 34*60 + 8
t2_trim = 36*60 + 50
t3_trim = 38*60 + 0
t4_trim = 39*60 + 12
t5_trim = 40*40 + 40
t6_trim = 41*60 + 56
time_trim = [t1_trim, t2_trim, t3_trim, t4_trim, t5_trim, t6_trim]

trim_curve = []
alpha_trim = []
speed_lst = []



for i in range(len(time_trim)):
    elevator = matlab.getdata_at_time('delta_e', time_trim[i], time_trim[i ]+ dt)
    elevator_avg = (sum(elevator))/(len(elevator))
    trim_curve.append(elevator_avg)
    
    angle_trim = matlab.getdata_at_time('vane_AOA', time_trim[i], time_trim[i] + dt)
    angle_avg = (sum(angle_trim))/(len(angle_trim))
    alpha_trim.append(angle_avg)
    
    speed_trim = matlab.getdata_at_time('Dadc1_tas', time_trim[i], time_trim[i ] + dt)
    speed_kts_trim = (sum(speed_trim))/(len(speed_trim))
    speed_ms_trim = aero.kts_to_ms(speed_kts_trim)
    speed_lst.append(speed_ms_trim)
    
#plot trim curve
plt.subplot(221)
plt.plot(alpha_trim, trim_curve, "ro" , label='Flight Data')
plt.title('Trim Curve')
plt.xlabel('Angle of Attack [-]')
plt.ylabel('Delta_e [-]')
plt.grid(True)

z = np.polyfit(alpha_trim, trim_curve, 1)
p = np.poly1d(z)
plt.plot(alpha_trim,p(alpha_trim),"b", label='Linear Regression')

plt.subplot(222)
plt.plot(speed_lst, trim_curve, "ro")
plt.title('Trim Curve')
plt.xlabel('Speed [m/s]')
plt.ylabel('Delta_e [-]')
plt.grid(True)
    
#Plot Cl_CD Curve
plt.subplot(223)
plt.plot(C_d, C_l, "ro", label='Orginal')
plt.plot(C_d_update, C_l, "bo", label='Updated')
plt.title('Lift coefficient vs Drag coefficient')
plt.xlabel('Drag coefficient [-]')
plt.ylabel('Lift coefficient [-]')
plt.grid(True)

z1 = np.polyfit(C_d, C_l, 1)
p1 = np.poly1d(z1)
plt.plot(C_d,p1(C_d),"r--", label='Linear Regression')

#PLot lift curve
plt.subplot(224)
plt.plot(alpha, C_l, "ro", label='FLight Data')
plt.title('Lift Curve')
plt.xlabel('Angle of Attack [-]')
plt.ylabel('Lift coefficient [-]')
plt.grid(True)

z2 = np.polyfit(alpha, C_l, 1)
p2 = np.poly1d(z2)
plt.plot(alpha,p2(alpha),"r--", label='Linear Regression')
plt.show()




    

    



    




