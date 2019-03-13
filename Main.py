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


#plotting nice stuff
######################################################################################################################################


### fugoid
fugoidstart = 60*49
fugoidtime = 159

fugoiddata = matlab.getdata_at_time('Dadc1_bcAlt',fugoidstart,fugoidstart+fugoidtime)*0.3048
fugoidtime = matlab.getdata_at_time('time',fugoidstart,fugoidstart+fugoidtime)/60

plt.figure(1)
plt.plot(fugoidtime,fugoiddata)
plt.xlabel('time [min]')
plt.ylabel('height [m]')

### ap_roll
ap_rollstart = 60*53 + 5
ap_rolltime = 5

ap_rolldata = matlab.getdata_at_time('Ahrs1_bRollRate',ap_rollstart,ap_rollstart+ap_rolltime)/180*np.pi
ap_rolltime = matlab.getdata_at_time('time',ap_rollstart,ap_rollstart+ap_rolltime)/60

plt.figure(2)
plt.plot(ap_rolltime,ap_rolldata)
plt.xlabel('time [min]')
plt.ylabel('roll rate [rad/s]')

### sh_period
sh_periodstart = 60*54
sh_periodtime = 4

sh_perioddata = matlab.getdata_at_time('Ahrs1_bPitchRate',sh_periodstart,sh_periodstart+sh_periodtime)/180*np.pi
sh_periodtime = matlab.getdata_at_time('time',sh_periodstart,sh_periodstart+sh_periodtime)/60

plt.figure(3)
plt.plot(sh_periodtime,sh_perioddata)
plt.xlabel('time [min]')
plt.ylabel('pitch rate [rad/s]')

### dutchR
dutchRstart = 60*56+2
dutchRtime = 18

dutchRdata = matlab.getdata_at_time('Ahrs1_bRollRate',dutchRstart,dutchRstart+dutchRtime)/180*np.pi
dutchRdata2 = matlab.getdata_at_time('Ahrs1_bYawRate',dutchRstart,dutchRstart+dutchRtime)/180*np.pi
dutchRtime = matlab.getdata_at_time('time',dutchRstart,dutchRstart+dutchRtime)/60

plt.figure(4)
fig, ax = plt.subplots(2, 1, sharex=True)
ax[0].plot(dutchRtime,dutchRdata)
ax[0].set_ylabel('roll rate [rad/s]')
ax[1].plot(dutchRtime,dutchRdata2)
ax[1].set_ylabel('yaw rate [rad/s]')
ax[1].set_xlabel('time [min]')

### dutchR_damp
dutchR_dampstart = 60*57+32
dutchR_damptime = 10

dutchR_dampdata = matlab.getdata_at_time('Ahrs1_bRollRate',dutchR_dampstart,dutchR_dampstart+dutchR_damptime)/180*np.pi
dutchR_dampdata2 = matlab.getdata_at_time('Ahrs1_bYawRate',dutchR_dampstart,dutchR_dampstart+dutchR_damptime)/180*np.pi
dutchR_damptime = matlab.getdata_at_time('time',dutchR_dampstart,dutchR_dampstart+dutchR_damptime)/60

plt.figure(5)
fig, ax = plt.subplots(2, 1, sharex=True)
ax[0].plot(dutchR_damptime,dutchR_dampdata)
ax[0].set_ylabel('roll rate [rad/s]')
ax[1].plot(dutchR_damptime,dutchR_dampdata2)
ax[1].set_ylabel('yaw rate [rad/s]')
ax[1].set_xlabel('time [min]')

### spiral
spiralstart = 60*62 -10
spiraltime = 400

spiraldata = matlab.getdata_at_time('Ahrs1_Roll',spiralstart,spiralstart+spiraltime)/180*np.pi
spiraldata2 = matlab.getdata_at_time('Ahrs1_bYawRate',spiralstart,spiralstart+spiraltime)
spiraltime = matlab.getdata_at_time('time',spiralstart,spiralstart+spiraltime)/60

plt.figure(6)
fig, ax = plt.subplots(2, 1, sharex=True)
ax[0].plot(spiraltime,spiraldata)
ax[0].set_ylabel('roll [rad]')
ax[1].plot(spiraltime,spiraldata2)
ax[1].set_ylabel('yaw rate [deg/s]')
ax[1].set_xlabel('time [min]')






