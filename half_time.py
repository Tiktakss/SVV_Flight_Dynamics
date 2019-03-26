import numpy as np
import matplotlib.pyplot as plt
import scipy.io as sio
from matlab_tools import Matlab_Tools
import Cit_par as p

class Half_Time:
    def __init__(self):
        self.parameters=['vane_AOA','elevator_dte','column_fe','lh_engine_FMF','rh_engine_FMF','lh_engine_itt','rh_engine_itt','lh_engine_OP','rh_engine_OP','lh_engine_fan_N1','lh_engine_turbine_N2','rh_engine_fan_N1','rh_engine_turbine_N2','lh_engine_FU','rh_engine_FU','delta_a','delta_e','delta_r','Gps_date','Gps_utcSec','Ahrs1_Roll','Ahrs1_Pitch','Fms1_trueHeading','Gps_lat','Gps_long','Ahrs1_bRollRate','Ahrs1_bPitchRate','Ahrs1_bYawRate','Ahrs1_bLongAcc','Ahrs1_bLatAcc','Ahrs1_bNormAcc','Ahrs1_aHdgAcc','Ahrs1_xHdgAcc','Ahrs1_VertAcc','Dadc1_sat','Dadc1_tat','Dadc1_alt','Dadc1_bcAlt','Dadc1_bcAltMb','Dadc1_mach','Dadc1_cas','Dadc1_tas','Dadc1_altRate','measurement_running','measurement_n_rdy','display_graph_state','display_active_screen','time' ]
        self.fugoidstart = 60*49 
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
            
if __name__ == "__main__":
    matlab=Matlab_Tools('FTISxprt-20190305_124649.mat')
    fugoiddata = matlab.getdata_at_time('Ahrs1_Pitch',matlab.fugoidstart,matlab.fugoidstart+matlab.fugoidtime)
    fugoidtime = matlab.getdata_at_time('time',matlab.fugoidstart,matlab.fugoidstart+matlab.fugoidtime)/60
    
    idx_max =  np.r_[True, fugoiddata[1:] > fugoiddata[:-1]] & np.r_[fugoiddata[:-1] > fugoiddata[1:], True]
    idx_min = np.r_[True, fugoiddata[1:] < fugoiddata[:-1]] & np.r_[fugoiddata[:-1] < fugoiddata[1:], True]
    
    mx = (fugoiddata[idx_max])[:-1]
    mn = (fugoiddata[idx_min])[1:-1]
    
    t_max=(fugoidtime[idx_max])[:-1]
    t_min=(fugoidtime[idx_min])[1:-1]
    
    fit_mx=np.polyfit(t_max-min(t_max),np.log(mx),1)
    fit_mn=np.polyfit(t_min-min(t_min),np.log(mn),1)
    
    print(fit_mx)
    
    
    plt.plot(fugoidtime,np.exp((fugoidtime-min(t_max))*fit_mx[0]+fit_mx[1]))
    plt.plot(fugoidtime,np.exp((fugoidtime-min(t_min))*fit_mn[0]+fit_mn[1]))
    plt.plot(fugoidtime,fugoiddata)