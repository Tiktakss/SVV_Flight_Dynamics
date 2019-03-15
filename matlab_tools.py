# -*- coding: utf-8 -*-
"""
Created on Wed Mar  6 09:54:48 2019

@author: Jeije
"""

import scipy.io as sio
import numpy as np
import matplotlib.pyplot as plt

class Matlab_Tools:
    def __init__(self,filename):
        self.lol = 0 #not used
        self.filename = filename#'FTISxprt-20190305_124649.mat'
        self.fugoidstart = 60*49
        self.fugoidtime = 159
        self.ap_rollstart = 60*53 + 5
        self.ap_rolltime = 5
        self.sh_periodstart = 60*54
        self.sh_periodtime = 4
        self.dutchRstart = 60*56+2
        self.dutchRtime = 18
        self.dutchR_dampstart = 60*57+32
        self.dutchR_damptime = 10
        self.spiralstart = 60*62 -10
        self.spiraltime = 400

        self.parameters=['vane_AOA','elevator_dte','column_fe','lh_engine_FMF','rh_engine_FMF','lh_engine_itt','rh_engine_itt','lh_engine_OP','rh_engine_OP','lh_engine_fan_N1','lh_engine_turbine_N2','rh_engine_fan_N1','rh_engine_turbine_N2','lh_engine_FU','rh_engine_FU','delta_a','delta_e','delta_r','Gps_date','Gps_utcSec','Ahrs1_Roll','Ahrs1_Pitch','Fms1_trueHeading','Gps_lat','Gps_long','Ahrs1_bRollRate','Ahrs1_bPitchRate','Ahrs1_bYawRate','Ahrs1_bLongAcc','Ahrs1_bLatAcc','Ahrs1_bNormAcc','Ahrs1_aHdgAcc','Ahrs1_xHdgAcc','Ahrs1_VertAcc','Dadc1_sat','Dadc1_tat','Dadc1_alt','Dadc1_bcAlt','Dadc1_bcAltMb','Dadc1_mach','Dadc1_cas','Dadc1_tas','Dadc1_altRate','measurement_running','measurement_n_rdy','display_graph_state','display_active_screen','time' ]
    
    def getdata(self,parameter):
        data=sio.loadmat(self.filename,struct_as_record=True,squeeze_me=True)
        flightdata=data['flightdata']
        parameterdata=flightdata[parameter][()]['data'][()]
        return parameterdata
    
    def getalldata(self):
        data=[]
        for i in range(len(self.parameters)):
            data=np.c_[data,self.getdata(self.filename,self.parameters[i])]
        return data
    
    def getunit(self,parameter):
        data=sio.loadmat(self.filename,struct_as_record=True,squeeze_me=True)
        flightdata=data['flightdata']
        parameterunit=flightdata[parameter][()]['units'][()]
        return parameterunit
    
    def getdata_at_time(self,parameter,start_time_in_seconds,stop_time_in_seconds):
        time = self.getdata('time')
        start = np.where(time==start_time_in_seconds)[0]
        stop = np.where(time==stop_time_in_seconds)[0]
        times= np.arange(start,stop)
        timeparameterdata=np.take(self.getdata(parameter),times)
        return timeparameterdata
    
    def getalldata_at_time(self,start_time_in_seconds,stop_time_in_seconds):
        time = self.getdata('time')
        start = np.where(time==start_time_in_seconds)[0]
        stop = np.where(time==stop_time_in_seconds)[0]
        times= np.arange(start,stop)
        timeparameterdata=np.take(self.getdata('time'),times)
        data=timeparameterdata
        for i in range(len(self.parameters)-1,0,-1):
            data=np.column_stack((self.getdata_at_time(self.parameters[i],start_time_in_seconds,stop_time_in_seconds),data))
        return data



"""
put testing/debugging code in the if-statement below
it will only run if you run this python file (matlab_tools.py)
"""
if __name__ == "__main__":
    tools=Matlab_Tools('FTISxprt-20190305_124649.mat')
#    data=sio.loadmat('FTISxprt-20180305_124437.mat',struct_as_record=True, squeeze_me=True)
#    data=data['flightdata']
    
    
#    elevator_dte=tools.getdata('FTISxprt-20180305_124437.mat','elevator_dte')
#    time=tools.getdata('FTISxprt-20180305_124437.mat','time')
#    alldata=tools.getalldata('FTISxprt-20180305_124437.mat')
    outputall=tools.getalldata_at_time(10,20)
    output=tools.getdata_at_time('time',10,20)
    print(output)
    print(outputall)
    