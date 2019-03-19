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

#Phugoid
fugoiddata = matlab.getdata_at_time('Dadc1_bcAlt',matlab.fugoidstart,matlab.fugoidstart+matlab.fugoidtime)*0.3048
fugoidtime = matlab.getdata_at_time('time',matlab.fugoidstart,matlab.fugoidstart+matlab.fugoidtime)/60

#Aperiodic roll
ap_rolldata = matlab.getdata_at_time('Ahrs1_bRollRate',matlab.ap_rollstart,matlab.ap_rollstart+matlab.ap_rolltime)/180*np.pi
ap_rolltime = matlab.getdata_at_time('time',matlab.ap_rollstart,matlab.ap_rollstart+matlab.ap_rolltime)/60

#Short period
sh_perioddata = matlab.getdata_at_time('Ahrs1_bPitchRate',matlab.sh_periodstart,matlab.sh_periodstart+matlab.sh_periodtime)/180*np.pi
sh_periodtime = matlab.getdata_at_time('time',matlab.sh_periodstart,matlab.sh_periodstart+matlab.sh_periodtime)/60

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
plt.plot(fugoidtime,fugoiddata)
plt.xlabel('time [min]')
plt.ylabel('height [m]')
plt.title("Phugoid")

plt.figure(2)
plt.plot(ap_rolltime,ap_rolldata)
plt.xlabel('time [min]')
plt.ylabel('roll rate [rad/s]')
plt.title("Aperiodic roll")

plt.figure(3)
plt.plot(sh_periodtime,sh_perioddata)
plt.xlabel('time [min]')
plt.ylabel('pitch rate [rad/s]')
plt.title("Short period")

plt.figure(4)
plt.subplot(211)
plt.plot(dutchRtime,dutchRdata)
plt.xlabel('time [min]')
plt.ylabel('roll rate [rad/s]')
plt.title("Dutch roll (undamped)")
plt.subplot(212)
plt.plot(dutchRtime,dutchRdata2)
plt.ylabel('yaw rate [rad/s]')
plt.xlabel('time [min]')

plt.figure(5)
plt.subplot(211)
plt.plot(dutchR_damptime,dutchR_dampdata)
plt.ylabel('roll rate [rad/s]')
plt.xlabel('time [min]')
plt.title("Dutch roll (damped)")
plt.subplot(212)
plt.plot(dutchR_damptime,dutchR_dampdata2)
plt.ylabel('yaw rate [rad/s]')
plt.xlabel('time [min]')

plt.figure(6)
plt.subplot(211)
plt.plot(spiraltime,spiraldata)
plt.ylabel('roll [rad]')
plt.xlabel('time [min]')
plt.title("Spiral")
plt.subplot(212)
plt.plot(spiraltime,spiraldata2)
plt.ylabel('yaw rate [deg/s]')
plt.xlabel('time [min]')

plt.show()






