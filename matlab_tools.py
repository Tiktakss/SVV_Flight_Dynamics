# -*- coding: utf-8 -*-
"""
Created on Wed Mar  6 09:54:48 2019

@author: Jeije
"""

import scipy.io as sio
import numpy as np
import matplotlib.pyplot as plt
import Cit_par as p

class Matlab_Tools:
    def __init__(self,filename):
        self.lol = 0 #not used
        self.filename = filename#'FTISxprt-20190305_124649.mat'
        self.fugoidstart = 60*49 +1
        self.fugoidtime = 159
        self.ap_rollstart = 60*53 + 5
        self.ap_rolltime = 5
        self.sh_periodstart = 60*54 + 0.9
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
    
    def Xs(self,manouvre):
        if manouvre == 'fugoid':
            start=self.fugoidstart
        elif manouvre=='ap_roll':
            start=self.ap_rollstart
        elif manouvre=='sh_period':
            start=self.sh_periodstart
        elif manouvre=='dutchR':
            start=self.dutchRstart
        elif manouvre=='dutchR_damp':
            start=self.dutchR_dampstart
        elif manouvre=='spiral':
            start=self.spiralstart
        else:
            print ('invalid manouvre')
            start=0
        
        dt= 0.2
        uhat=0 #dimensionlessvelocity vt true airspeed vt0 stationary airspead
        aoa=self.getdata_at_time('vane_AOA',start,start+dt)[0]/180*np.pi
        theta=self.getdata_at_time('Ahrs1_Pitch',start,start+dt)[0]/180*np.pi
        vtas = self.getdata_at_time('Dadc1_tas',start,start+dt)[0]*0.51 #knots -> m/s
        qcoverv=self.getdata_at_time('Ahrs1_bPitchRate',start,start+dt)[0]/180*np.pi*p.c/vtas#q is pitchrate
        X_s=np.matrix([[uhat],[aoa],[theta],[qcoverv]])
        return X_s, vtas

    def Xa(self,manouvre):
        if manouvre == 'fugoid':
            start=self.fugoidstart
        elif manouvre=='ap_roll':
            start=self.ap_rollstart
        elif manouvre=='sh_period':
            start=self.sh_periodstart
        elif manouvre=='dutchR':
            start=self.dutchRstart
        elif manouvre=='dutchR_damp':
            start=self.dutchR_dampstart
        elif manouvre=='spiral':
            start=self.spiralstart
        else:
            print ('invalid manouvre')
            start=0
        
        dt= 0.2
        Beta=self.getdata_at_time('Fms1_trueHeading',start,start+dt)[0]
        Phi=self.getdata_at_time('vane_AOA',start,start+dt)[0]
        pbover2v=self.getdata_at_time('vane_AOA',start,start+dt)[0]
        rbover2v=self.getdata_at_time('Ahrs1_bPitchRate',start,start+dt)[0]*p.c/self.getdata_at_time('Dadc1_tas',start,start+dt)[0]#q is pitchrate
        X_a=np.matrix([[Beta],[Phi],[pbover2v],[rbover2v]])
        return X_a


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
    