from math import *
import matplotlib.pyplot as plt

#import classes
from aero_tools import Aero_Tools
aero = Aero_Tools()
from excel_tools import import_excel
excel = import_excel('./Post_Flight_Datasheet_Flight_test.xlsx')
from matlab_tools import Matlab_Tools
matlab = Matlab_Tools()

#inputs
blockfuel       = 4090.0 #lbs #obtained from written data sheet
empty_weight    = 9165.0 #lbs #obtained from Mass & Balance report
gravity = 9.81 #m/s^2
surface = 30 #m^2 #obtained from reader
Cd0 = 0.04 # #obtained from reader
e = 0.8 #obtained from reader
b = 15.911 #span obtained from reader #m


#obtain data for Cl-Cd plot
data = import_excel.Cl_Cd_data(excel)

weight_people = sum(import_excel.weights(excel))/0.453592 #lbs
total_weight = weight_people + blockfuel + empty_weight
C_l = [] #lift coefficient
C_d = [] #drag coefficient
alpha = [] #angle of attack
mach = []

for i in range(len(data)):
    row = data[i]
    weight_lbs = total_weight - row[8] #weight in lbs
    weight_kg = weight_lbs * 0.453592 #weight in kg
    weight_n = weight_kg*gravity #weight inNewon
    h_ft = row[3] #height in ft
    h_m = aero.ft_to_m(h_ft) #height in m
    density = aero.rho_alt(h_m) #density kg/m^3
    speed_kts = row[4]
    speed_ms = aero.kts_to_ms(speed_kts)
    
    lift = (2*weight_n)/(density*surface*speed_ms**2)
    C_l.append(lift)
    
    A = b*b/surface #aspect ratio
    drag = Cd0 +(lift**2)/(pi*A*e)
    C_d.append(drag)
    
    aoa = row[5] #angle of attack #degrees
    alpha.append(aoa)
    
    M = aero.calc_mach(h_m, speed_ms)
    mach.append(M)
    

##Plot Cl_CD Curve    
#plt.figure()
#plt.plot(C_d[0], C_l[0], "ro")
#plt.plot(C_d[1], C_l[1], "bo")
#plt.plot(C_d[2], C_l[2], "go")
#plt.plot(C_d[3], C_l[3], "yo")
#plt.plot(C_d[4], C_l[4], "ko")
#plt.plot(C_d[5], C_l[5], "co")
#plt.plot(C_d, C_l)
#plt.title('Lift coefficient vs Drag coefficient')
#plt.xlabel('Drag coefficient [-]')
#plt.ylabel('Lift coefficient [-]')
#plt.grid(True)
#plt.show()  
#
##PLot lift curve 
#plt.figure()
#plt.plot(alpha, C_l)
#plt.title('Lift Curve')
#plt.xlabel('Angle of Attack [-]')
#plt.ylabel('Lift coefficient [-]')
#plt.grid(True)
#plt.show() 
    
print(mach)
    


    




