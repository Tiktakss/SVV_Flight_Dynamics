# -*- coding: utf-8 -*-
"""
Created on Wed Mar  6 09:54:48 2019

@author: Jeije
"""

import scipy.io as sio
import numpy as np

class Matlab_Tools:
    def __init__(self):
        self.lol = 0 #not used
        self.parameters=['vane_AOA','elevator_dte','column_fe','vane_AOA',' elevator_dte',' column_fe',' lh_engine_FMF',' rh_engine_FMF',' lh_engine_itt',' rh_engine_itt',' lh_engine_OP',' rh_engine_OP',' lh_engine_fan_N1',' lh_engine_turbine_N2','rh_engine_fan_N1',' rh_engine_turbine_N2','lh_engine_FU',' rh_engine_FU',' delta_a',' delta_e',' delta_r',' Gps_date',' Gps_utcSec',' Ahrs1_Roll',' Ahrs1_Pitch',' Fms1_trueHeading',' Gps_lat',' Gps_long',' Ahrs1_bRollRate',' Ahrs1_bPitchRate',' Ahrs1_bYawRate',' Ahrs1_bLongAcc',' Ahrs1_bLatAcc',' Ahrs1_bNormAcc',' Ahrs1_aHdgAcc',' Ahrs1_xHdgAcc',' Ahrs1_VertAcc',' Dadc1_sat',' Dadc1_tat',' Dadc1_alt',' Dadc1_bcAlt',' Dadc1_bcAltMb',' Dadc1_mach',' Dadc1_cas',' Dadc1_tas',' Dadc1_altRate',' measurement_running',' measurement_n_rdy',' display_graph_state',' display_active_screen',' time' ]
    
    def getdata(self,filename,parameter):
        data=sio.loadmat(filename)
        flightdata=data['flightdata']
        parameterdata=flightdata[0][0][parameter][0][0][0][0][0]
        return parameterdata
    
    def getalldata(self,filename):
        data=np.array(0)
        for i in range(len(self.parameters)):
            data=np.append(data,self.getdata(filename,self.parameters[i]))
        return data



"""
put testing/debugging code in the if-statement below
it will only run if you run this python file (matlab_tools.py)
"""
if __name__ == "__main__":
    tools=Matlab_Tools()
    data=sio.loadmat('FTISxprt-20180305_124437.mat')
    flightdata=data['flightdata']
    vane_AOA=flightdata['vane_AOA']
    
    vane_AOA=tools.getdata('FTISxprt-20180305_124437.mat','vane_AOA')
    
    alldata=tools.getalldata('FTISxprt-20180305_124437.mat')