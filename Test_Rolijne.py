import numpy as np
import matplotlib.pyplot as plt
#from Cl_Cd_Plot import C_l
import Cit_par as par
from math import pi

#import classes
from aero_tools import Aero_Tools
aero = Aero_Tools()
from excel_tools import import_excel
excel = import_excel('./Post_Flight_Datasheet_03_05_V3.xlsx')
from matlab_tools import Matlab_Tools

#Inputs
blockfuel = 4050.0 #lbs #obtained from written data sheet
empty_weight = 9165.0 #lbs #obtained from Mass & Balance report
Arm_seat12 = 131.0 #inch #obtained from appendix E
Arm_seat910 = 170.0 #inch #obtained from appendix E
Arm_seat34 = 214.0 #inch #obtained from appendix E
Arm_seat56 = 251.0 #inch #obtained from appendix E
Arm_seat78 = 288.0 #inch #obtained from appendix E
Arm_cgshift = 145.0 #inch estimated between 1 and 9
Arm_fuel = 285.56 #inch #obtained from Mass & Balance report
Arm_BEM = 292.18 #inch #obtained from Mass & Balance report
Time = np.array([18.,21.,25.,27.,29.,31.,34.,36.,38.,39.,40.,41.,46.,47.])

#obtain data for mass balance
data = import_excel.Cl_Cd_data(excel)
data_trim_curve = import_excel.trimcurve_data(excel)
data_cg_shift_data = import_excel.cg_shift_data(excel)
weight_people = sum(import_excel.weights(excel))/0.453592 #lbs
total_weight = weight_people + blockfuel + empty_weight

#Calculate moments for people and BEM
moment_p1 = import_excel.weights(excel)[0] * Arm_seat12  # lbs*inch
moment_p2 = import_excel.weights(excel)[1] * Arm_seat12  # lbs*inch
moment_p10 = import_excel.weights(excel)[2] * Arm_seat910  # lbs*inch
moment_p3 = import_excel.weights(excel)[3] * Arm_seat34  # lbs*inch
moment_p4 = import_excel.weights(excel)[4] * Arm_seat34  # lbs*inch
moment_p5 = import_excel.weights(excel)[5] * Arm_seat56  # lbs*inch
moment_p6 = import_excel.weights(excel)[6] * Arm_seat56  # lbs*inch
moment_p7 = import_excel.weights(excel)[7] * Arm_seat78  # lbs*inch
moment_p8 = import_excel.weights(excel)[8] * Arm_seat78  # lbs*inch
moment_CGshift = import_excel.weights(excel)[8] * Arm_cgshift #lbs*inch
moment_BEM = empty_weight * Arm_BEM  # lbs*inch

#Empty arrays
AOA = np.zeros(len(data_trim_curve)+len(data_cg_shift_data)-1)
de = np.zeros(len(data_trim_curve)+len(data_cg_shift_data)-1)
Fe = np.zeros(len(data_trim_curve)+len(data_cg_shift_data)-1)
V = np.zeros(len(data_trim_curve)+len(data_cg_shift_data)-1)
Center_gravity = np.zeros(len(data)+len(data_trim_curve)+len(data_cg_shift_data)-1)

#Make Life curve
#Inputs
A = par.b*par.b / par.S
#Create emoty lists for plots
C_l = [] #lift coefficient
C_d = [] #drag coefficient
alpha = [] #angle of attack

#Create plots
data_lift_curve = import_excel.Cl_Cd_data(excel)
for i in range(len(data)):
    row_lift = data_lift_curve[i]
    weight = total_weight - row_lift[8] #lbs
    weight_kg = aero.lbs * weight
    weight_n = weight_kg * aero.g0
    
    height = row_lift[3]
    height_m = aero.ft_to_m(height)
    density = aero.rho_alt(height_m)
    
    speed = row_lift[4]
    speed_ms = aero.kts_to_ms(speed)
    
    lift = (2*weight_n)/(density*par.S*speed_ms**2)
    C_l.append(lift)
    
    drag = par.CD0 +(lift**2)/(pi*A*par.e)
    C_d.append(drag)
    
    angle = row_lift[5]
    alpha.append(angle)
    

#CG shift due to fuel flow
for i in range(len(data)):
    row = data[i]
    weight_fuel = blockfuel - row[8] #lbs
    total_weight = weight_people + weight_fuel + empty_weight #lbs
    moment_fuel = weight_fuel*Arm_fuel #lbs*inch
    Center_gravity[i] = (moment_fuel+moment_BEM+moment_p1+moment_p2+moment_p10+moment_p3\
                         +moment_p4+moment_p5+moment_p6+moment_p7+moment_p8)/total_weight*2.54 #cm

#Put data from PFD into arrays
for i in range(len(data_trim_curve)):
    row = data_trim_curve[i]
    weight_fuel = blockfuel - row[11]
    total_weight = weight_people + weight_fuel + empty_weight #lbs
    moment_fuel = weight_fuel*Arm_fuel #lbs*inch
    Center_gravity[i+len(data)] = (moment_fuel+moment_BEM+moment_p1+moment_p2+moment_p10+moment_p3\
                         +moment_p4+moment_p5+moment_p6+moment_p7+moment_p8)/total_weight*2.54 #cm
    AOA[i] = row[5]
    de[i] = row[6]
    Fe[i] = row[8]
    V[i] = row[4]


#After cg shifts
for i in range(len(data_cg_shift_data)):
    row = data_cg_shift_data[i]
    weight_fuel = blockfuel - row[11]
    total_weight = weight_people + weight_fuel + empty_weight #lbs
    moment_fuel = weight_fuel*Arm_fuel #lbs*inch
    if i == 1.:
        moment_p8 = moment_CGshift
    Center_gravity[i+len(data)+len(data_trim_curve)-1] = (moment_fuel+moment_BEM+moment_p1+moment_p2+moment_p10+moment_p3\
                         +moment_p4+moment_p5+moment_p6+moment_p7+moment_p8)/total_weight*2.54 #cm
    AOA[i+len(data_trim_curve)-1] = row[5]
    de[i+len(data_trim_curve)-1] = row[6]
    Fe[i+len(data_trim_curve)-1] = row[8]
    V[i+len(data_trim_curve)-1] = row[4]

#Calculation for Cm_delta and Cm_alpha
slope = (de[3]-de[5])/(AOA[3]-AOA[5])
#Cm_delta = -C_l[5]*(Center_gravity[13]-Center_gravity[12])/((de[7]-de[6])*205.69)
#Cm_alpha = -Cm_delta*slope
#print(Cm_alpha,Cm_delta)
#print(Center_gravity[13]-Center_gravity[12])

#Plotting
plt.subplot(221)
plt.plot(Time,Center_gravity)
plt.title("Center of Gravity")
plt.ylabel("Distance from nose[cm]")
plt.xlabel("Time[min]")

plt.subplot(222)
plt.scatter(AOA,de)
plt.title("Elevator trim curve")
plt.ylabel("$\delta_e[deg]$")
plt.xlabel("$\\alpha[deg]$")

plt.subplot(223)
plt.scatter(AOA,Fe)
plt.title("Control force curve")
plt.ylabel("$F_e$[N]")
plt.xlabel("$\\alpha[deg]$")
plt.show()

#Plot C curves
plt.figure()
plt.subplot(121)
plt.plot(C_d, C_l, "ro")
plt.title('Lift coefficient vs Drag coefficient')
plt.xlabel('Drag coefficient [-]')
plt.ylabel('Lift coefficient [-]')
plt.grid(True)

plt.subplot(122)
plt.plot(alpha, C_l , "ro")
plt.title('Lift Curve')
plt.xlabel('Angle of Attack [-]')
plt.ylabel('Lift coefficient [-]')
plt.grid(True)
plt.show()



