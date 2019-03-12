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
excel = import_excel('./Post_Flight_Datasheet_Flight_test.xlsx')
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
ap_rollstart = 60*52+56
ap_rolltime = 20

ap_rolldata = matlab.getdata_at_time('Ahrs1_bRollRate',ap_rollstart,ap_rollstart+ap_rolltime)/180*np.pi
ap_rolltime = matlab.getdata_at_time('time',ap_rollstart,ap_rollstart+ap_rolltime)/60

plt.figure(2)
plt.plot(ap_rolltime,ap_rolldata)
plt.xlabel('time [min]')
plt.ylabel('rollrate [deg/s]')

### sh_period
sh_periodstart = 60*54
sh_periodtime = 4

sh_perioddata = matlab.getdata_at_time('Ahrs1_bPitchRate',sh_periodstart,sh_periodstart+sh_periodtime)
sh_periodtime = matlab.getdata_at_time('time',sh_periodstart,sh_periodstart+sh_periodtime)/60

plt.figure(3)
plt.plot(sh_periodtime,sh_perioddata)
plt.xlabel('time [min]')
plt.ylabel('rollrate [deg/s]')





