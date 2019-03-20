# main running program
# SVV - Flight Dynamics
# AE3212-II
# 2019

# Giel Kerkhofs
# Teun Vleming
# Jeije vd Wijngaart
# Wouter Spek
# Rolijne Pietersma
# Nick Pauly

#######################

#import classes
import matplotlib.pyplot as plt
import numpy as np

from aero_tools import Aero_Tools
aero = Aero_Tools()
from excel_tools import import_excel
excel = import_excel('./Post_Flight_Datasheet_03_05_V3.xlsx')
from matlab_tools import Matlab_Tools
matlab = Matlab_Tools('FTISxprt-20190305_124649.mat')
from numerical_model import Numerical_Model
nummodel = Numerical_Model()


#Phugoid
fugoiddata = matlab.getdata_at_time('Ahrs1_Pitch',matlab.fugoidstart,matlab.fugoidstart+matlab.fugoidtime)
#fugoiddata = fugoiddata - fugoiddata[0] #correct for stable flight
fugoidtime = matlab.getdata_at_time('time',matlab.fugoidstart,matlab.fugoidstart+matlab.fugoidtime)/60
fugoid = nummodel.symmetric_interpolate('fugoid')[2]/np.pi*180#/np.pi*180 #pitch 'theta'
#fugoid = nummodel.symmetric_control('fugoid')[2]/np.pi*180#/np.pi*180 #pitch 'theta'


#Aperiodic roll
ap_rolldata = matlab.getdata_at_time('Ahrs1_Roll',matlab.ap_rollstart,matlab.ap_rollstart+matlab.ap_rolltime)#'Ahrs1_bRollRate'
ap_rolltime = matlab.getdata_at_time('time',matlab.ap_rollstart,matlab.ap_rollstart+matlab.ap_rolltime)/60
#ap_roll = nummodel.not_symmetric_interpolate('ap_roll')[1] # roll angle 'phi'

#Short period
sh_perioddata = matlab.getdata_at_time('Ahrs1_bPitchRate',matlab.sh_periodstart,matlab.sh_periodstart+matlab.sh_periodtime)
sh_periodtime = matlab.getdata_at_time('time',matlab.sh_periodstart,matlab.sh_periodstart+matlab.sh_periodtime)/60
#sh_period = nummodel.symmetric_interpolate('sh_period')[3]/np.pi*180#/np.pi*180 #pitch 'q'

#Dutch roll undamped
dutchRdata = matlab.getdata_at_time('Ahrs1_bRollRate',matlab.dutchRstart,matlab.dutchRstart+matlab.dutchRtime)/180*np.pi
dutchRdata2 = matlab.getdata_at_time('Ahrs1_bYawRate',matlab.dutchRstart,matlab.dutchRstart+matlab.dutchRtime)/180*np.pi
dutchRtime = matlab.getdata_at_time('time',matlab.dutchRstart,matlab.dutchRstart+matlab.dutchRtime)/60

#Dutch roll damped
dutchR_dampdata = matlab.getdata_at_time('Ahrs1_bRollRate',matlab.dutchR_dampstart,matlab.dutchR_dampstart+matlab.dutchR_damptime)/180*np.pi
dutchR_dampdata2 = matlab.getdata_at_time('Ahrs1_bYawRate',matlab.dutchR_dampstart,matlab.dutchR_dampstart+matlab.dutchR_damptime)/180*np.pi
dutchR_damptime = matlab.getdata_at_time('time',matlab.dutchR_dampstart,matlab.dutchR_dampstart+matlab.dutchR_damptime)/60

#Spiral
spiraldata = matlab.getdata_at_time('Ahrs1_Roll',matlab.spiralstart,matlab.spiralstart+matlab.spiraltime)/180*np.pi
spiraldata2 = matlab.getdata_at_time('Ahrs1_bYawRate',matlab.spiralstart,matlab.spiralstart+matlab.spiraltime)
spiraltime = matlab.getdata_at_time('time',matlab.spiralstart,matlab.spiralstart+matlab.spiraltime)/60

#Plotting
plt.figure(1)
plt.plot(fugoidtime,fugoiddata,label='data')
plt.plot(fugoidtime,fugoid,label='numerical model')
plt.xlabel('time [min]')
plt.ylabel('pitch [deg]')
plt.title("Phugoid")
plt.legend()

plt.figure(2)
plt.plot(ap_rolltime,ap_rolldata,label='data')
plt.plot(ap_rolltime,ap_roll,label='numerical model')
plt.xlabel('time [min]')
plt.ylabel('roll [deg]')
plt.title("Aperiodic roll")
plt.legend()

plt.figure(3)
plt.plot(sh_periodtime,sh_perioddata,label='data')
plt.plot(sh_periodtime,sh_period,label='numerical model')
plt.xlabel('time [min]')
plt.ylabel('pitch rate [deg/s]')
plt.title("Short period")
plt.legend()

plt.figure(4)
plt.subplot(211)
plt.plot(dutchRtime,dutchRdata,label='data')
#plt.plot(dutchRtime,dutchR,label='numerical model')
plt.ylabel('roll rate [rad/s]')
plt.title("Dutch roll (undamped)")
plt.legend()
plt.subplot(212)
plt.plot(dutchRtime,dutchRdata2,label='data')
#plt.plot(dutchRtime,dutchR2,label='numerical model')
plt.ylabel('yaw rate [rad/s]')
plt.xlabel('time [min]')
plt.legend()

plt.figure(5)
plt.subplot(211)
plt.plot(dutchR_damptime,dutchR_dampdata,label='data')
#plt.plot(dutchR_damptime,dutchR_damp,label='numerical')
plt.ylabel('roll rate [rad/s]')
plt.xlabel('time [min]')
plt.title("Dutch roll (damped)")
plt.legend()
plt.subplot(212)
plt.plot(dutchR_damptime,dutchR_dampdata2,label='data')
#plt.plot(dutchR_damptime,dutchR_damp2,label='numerical')
plt.ylabel('yaw rate [rad/s]')
plt.xlabel('time [min]')
plt.legend()

plt.figure(6)
plt.subplot(211)
plt.plot(spiraltime,spiraldata,label='data')
#plt.plot(spiraltime,spiral,label='numerical')
plt.ylabel('roll [rad]')
plt.xlabel('time [min]')
plt.title("Spiral")
plt.legend()
plt.subplot(212)
plt.plot(spiraltime,spiraldata2,label='data')
#plt.plot(spiraltime,spiral2,label='numerical')
plt.ylabel('yaw rate [deg/s]')
plt.xlabel('time [min]')
plt.legend()

plt.show()






