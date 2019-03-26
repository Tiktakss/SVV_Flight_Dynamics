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
#from matlab_tools import Matlab_Tools

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
C_l2 = []
C_d = [] #drag coefficient
alpha = [] #angle of attack
h_p = [] #altitude pressure
Mach = [] #Mach number
diff_temp = [] #difference between ISA and calcuated temp
ffl = [] #fuel flow right
ffr = [] #fuel flow left
Reynolds = []

#Create C_l plot
data_lift_curve = import_excel.Cl_Cd_data(excel)

for i in range(len(data)):
    row_lift = data_lift_curve[i]
    weight = total_weight - row_lift[8] #lbs
    weight_kg = aero.lbs * weight #kg
    weight_n = weight_kg * aero.g0 #N
    
    height = row_lift[3] #ft
    height_m = aero.ft_to_m(height) #m
    h_p.append(height_m)
    density = aero.rho_alt(height_m)

    
    speed = row_lift[4] #kts
    speed_m = aero.kts_to_ms(speed) #ms IAS
    speed_ms = aero.ias_to_tas(height_m, speed_m) # ms TAS
    
    lift = (2*weight_n)/(density*par.S*speed_ms**2) #N
    C_l.append(lift)
    C_l2.append(lift*lift)
    
    angle = row_lift[5]
    alpha.append(angle)
    fuel_left = row_lift[6]*aero.lbs/3600
    fuel_right = row_lift[7]*aero.lbs/3600
    ffl.append(fuel_left)
    ffr.append(fuel_right)
    
    M = aero.calc_mach(height_m, speed_ms)
    Mach.append(M)
    
    Re = aero.calc_re(density, speed_ms, par.b)
    Reynolds.append(Re)
    
    temp = aero.calc_temp(row_lift[9]+273.15, M)
    temp_ISA = aero.T_alt(height_m)
    diff = temp - temp_ISA
    diff_temp.append(diff)
    
#print(h_p)
#print(Mach)
#print(diff_temp)
#print(ffl)
#print(ffr)

T_right = [3641.04, 2717.52, 2266.88, 2123.31, 2223.13, 1907.57] #obtained from thrust file 
T_left = [3991.19, 3136.22, 2510.9, 2414.81, 2526.69, 2178.88]

#Create Drag plot
for i in range(len(data)):
    row_lift = data_lift_curve[i]
    weight = total_weight - row_lift[8] #lbs
    weight_kg = aero.lbs * weight #kg
    weight_n = weight_kg * aero.g0 #N
    
    height = row_lift[3] #ft
    height_m = aero.ft_to_m(height) #m
    density = aero.rho_alt(height_m)

    
    speed = row_lift[4] #kts
    speed_m = aero.kts_to_ms(speed) #ms IAS
    speed_ms = aero.ias_to_tas(height_m,speed_m) #ms TAS
    
    thrust = T_right[i] + T_left[i]
    drag = (2*thrust)/(density*par.S*speed_ms**2)
    C_d.append(drag)


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
    moment_p8 = moment_CGshift
    Center_gravity[i+len(data)+len(data_trim_curve)-1] = (moment_fuel+moment_BEM+moment_p1+moment_p2+moment_p10+moment_p3\
                         +moment_p4+moment_p5+moment_p6+moment_p7+moment_p8)/total_weight*2.54 #cm
    AOA[i+len(data_trim_curve)-1] = row[5]
    de[i+len(data_trim_curve)-1] = row[6]
    Fe[i+len(data_trim_curve)-1] = row[8]
    V[i+len(data_trim_curve)-1] = row[4]
    
    weight = total_weight #lbs
    weight_kg = aero.lbs * weight #kg
    weight_n = weight_kg * aero.g0 #N
    
    height = row_lift[3] #ft
    height_m = aero.ft_to_m(height) #m
    density = aero.rho_alt(height_m) 
    
    speed = row_lift[4] #kts
    speed_ms = aero.kts_to_ms(speed) #ms
    
    C_n = (2*weight_n)/(density*par.S*speed_ms**2) #N
    
##Plotting
#plt.figure()
#plt.subplot(221)
#plt.plot(Time,Center_gravity, "bo")
#plt.title("Center of Gravity")
#plt.ylabel("Distance from nose[cm]")
#plt.xlabel("Time[min]")
#plt.grid(True)
#
#plt.subplot(222)
#plt.plot(AOA[:6],de[:6], "bo")
#plt.title("Elevator trim curve")
#plt.ylabel("$\delta_e[deg]$")
#plt.gca().invert_yaxis()
#plt.xlabel("$\\alpha[deg]$")
#plt.grid(True)
#
#plt.subplot(223)
#plt.plot(AOA[:6],Fe[:6], "bo")
#plt.title("Control force curve")
#plt.ylabel("$F_e$[N]")
#plt.xlabel("$\\alpha[deg]$")
#plt.grid(True)


#Plot C curves
#plt.figure()
#plt.subplot(221)
plt.plot(C_d, C_l, "bo", label ="Flight Data")
plt.title('Lift coefficient vs Drag coefficient')
plt.xlabel('C$_D$ [-]')
plt.ylabel('C$_L$ [-]')
plt.grid(True)
z2 = np.polyfit(C_d, C_l, 2)
p2= np.poly1d(z2)
xp2 = np.linspace(0.02, 0.06, 200)
plt.plot(xp2, p2(xp2) ,"b--", label="Trendline")
plt.legend()
#
#plt.subplot(222)
#plt.plot(alpha, C_l , "bo", label ="Flight Data")
#plt.title('Lift Curve')
#plt.xlabel('$\\alpha$ [deg]')
#plt.ylabel('C$_L$ [-]')
#plt.grid(True)
#z1 = np.polyfit(alpha, C_l, 1)
#p1 = np.poly1d(z1)
#xp1 = np.linspace(1, 12, 200)
#plt.plot(xp1,p1(xp1),"b--", label="Trendline")
#plt.legend()

#plt.subplot(223)
#plt.plot(alpha, C_d, "bo", label ="Flight Data" )
#plt.title('Drag Curve')
#plt.xlabel('$\\alpha$ [deg]')
#plt.ylabel('C$_D$ [-]')
#plt.grid(True)
#z3 = np.polyfit(alpha, C_d, 2)
#p3 = np.poly1d(z3)
#xp3 = np.linspace(1, 12, 200)
#plt.plot(xp3,p3(xp3),"b--", label="Trendline")
#plt.legend()
#
#plt.subplot(224)
#plt.plot(C_l2, C_d, "bo", label ="Flight Data" )
#plt.xlabel('C$_L^2$ [-]')
#plt.ylabel('C$_D$ [-]')
#plt.grid(True)
#z4 = np.polyfit(C_l2, C_d, 1)
#p4 = np.poly1d(z4)
#xp4 = np.linspace(0, 1.0, 200)
#plt.plot(xp4,p4(xp4),"b--", label="Trendline")
#plt.legend()
plt.show()

#Calculation for coefficients
slope = (np.radians(max(de))-np.radians(min(de)))/(np.radians(min(AOA))-np.radians(max(AOA)))
#Cm_delta = -C_l[5]*(Center_gravity[13]-Center_gravity[12])/((np.radians(de[7])-np.radians(de[6]))*205.69)
Cm_delta = -1/(np.radians(de[-1])-np.radians(de[-2]))*C_n*(Center_gravity[-2]-Center_gravity[-3])/(par.c*100)
Cm_alpha = -Cm_delta*slope
Cl_alpha = (max(C_l)-min(C_l))/(np.radians(max(alpha))-np.radians(min(alpha)))
Cd0 = p4(0)
slope_e = (p4(1.0)-p4(0))/(xp4[-1]-xp4[0])
e = 1/(pi*A*slope_e)

#print("Cl_alpha =" ,Cl_alpha)
#print("Cm_delta =" ,Cm_delta)
#print("Cm_alpha =" ,Cm_alpha)
#print("CD0 =", Cd0)
#print("e=", e)

#print(min(Reynolds))
#print(max(Reynolds))









