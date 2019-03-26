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
    
    #Phugoid#
    fugoiddata = matlab.getdata_at_time('Ahrs1_Pitch',matlab.fugoidstart,matlab.fugoidstart+matlab.fugoidtime)
    fugoidtime = matlab.getdata_at_time('time',matlab.fugoidstart,matlab.fugoidstart+matlab.fugoidtime)/60
    
    idx_max =  np.r_[True, fugoiddata[1:] > fugoiddata[:-1]] & np.r_[fugoiddata[:-1] > fugoiddata[1:], True]
    idx_min = np.r_[True, fugoiddata[1:] < fugoiddata[:-1]] & np.r_[fugoiddata[:-1] < fugoiddata[1:], True]
    
    mx = (fugoiddata[idx_max])[:-1]
    mn = (fugoiddata[idx_min])[1:-1]
    
    t_max=(fugoidtime[idx_max])[:-1]
    t_min=(fugoidtime[idx_min])[1:-1]
    
    fit_mx=np.polyfit(t_max-min(t_max),np.log(mx),1)
#    fit_mn=np.polyfit(t_min-min(t_min),np.log(mn),1)
    trend=np.polyfit(fugoidtime,fugoiddata,1)
    
    y = np.exp((fugoidtime-min(t_max))*fit_mx[0]+fit_mx[1])
    trendline=trend[0]*fugoidtime+trend[1]
    
#    plt.plot(fugoidtime,y)
#    plt.plot(fugoidtime,np.exp((fugoidtime-min(t_min))*fit_mn[0]+fit_mn[1]))
#    plt.plot(fugoidtime,fugoiddata)
#    plt.plot(fugoidtime,trendline)
    
    amplitude = y-trendline
    
    i = 0
    while amplitude[i]>amplitude[0]/2:
        i=i+1
    
    half_fugoid=(fugoidtime[i]-fugoidtime[0])*60
    
    
    #Dutch roll - roll#
    dutchRdata = matlab.getdata_at_time('Ahrs1_bRollRate',matlab.dutchRstart,matlab.dutchRstart+matlab.dutchRtime)/180*np.pi
    dutchRdata2 = matlab.getdata_at_time('Ahrs1_bYawRate',matlab.dutchRstart,matlab.dutchRstart+matlab.dutchRtime)/180*np.pi
    dutchRtime = matlab.getdata_at_time('time',matlab.dutchRstart,matlab.dutchRstart+matlab.dutchRtime)/60
    
    idx_max =  np.r_[True, dutchRdata[1:] > dutchRdata[:-1]] & np.r_[dutchRdata[:-1] > dutchRdata[1:], True]
    idx_min = np.r_[True, dutchRdata[1:] < dutchRdata[:-1]] & np.r_[dutchRdata[:-1] < dutchRdata[1:], True]
    
    mx = (dutchRdata[idx_max])[1:-1]
    mn = (dutchRdata[idx_min])[1:-2]
    
    t_max=(dutchRtime[idx_max])[1:-1]
    t_min=(dutchRtime[idx_min])[1:-2]
    start=np.where(dutchRtime==t_max[0])
    start = start[0][0]
    end=np.where(dutchRtime==t_max[3])
    end = end[0][0]

    fit_mx=np.polyfit(t_max-min(t_max),np.log(mx),1)
#    fit_mn=np.polyfit(t_min-min(t_min),np.log(mn),1)
    trend=np.polyfit(dutchRtime[start:end],dutchRdata[start:end],1)
    
    y = np.exp((dutchRtime-min(t_max))*fit_mx[0]+fit_mx[1])
    trendline=trend[0]*dutchRtime+trend[1]
    
#    plt.plot(dutchRtime,y)
#    plt.plot(fugoidtime,np.exp((fugoidtime-min(t_min))*fit_mn[0]+fit_mn[1]))
#    plt.plot(dutchRtime,dutchRdata)
#    plt.plot(dutchRtime,trendline)
    
    amplitude = y-trendline
    
    i = 0
    while amplitude[i]>(mx[0]-trendline[start])/2:
        i=i+1
    half_dutchR=((dutchRtime[i])-dutchRtime[start])*60
    
    
    #Dutch roll - yaw#
    idx_max =  np.r_[True, dutchRdata2[1:] > dutchRdata2[:-1]] & np.r_[dutchRdata2[:-1] > dutchRdata2[1:], True]
    idx_min = np.r_[True, dutchRdata2[1:] < dutchRdata2[:-1]] & np.r_[dutchRdata2[:-1] < dutchRdata2[1:], True]
    
    mx = (dutchRdata2[idx_max])[2:-1]
    mn = (dutchRdata2[idx_min])[2:-1]

    t_max=(dutchRtime[idx_max])[2:-1]
    t_min=(dutchRtime[idx_min])[2:-1]
    start=np.where(dutchRtime==t_max[0])
    start = start[0][0]
    end=np.where(dutchRtime==t_max[3])
    end = end[0][0]
    
    fit_mx=np.polyfit(t_max-min(t_max),np.log(mx),1)
#    fit_mn=np.polyfit(t_min-min(t_min),np.log(mn),1)
    trend=np.polyfit(dutchRtime[start:end],dutchRdata2[start:end],1)
    y = np.exp((dutchRtime-min(t_max))*fit_mx[0]+fit_mx[1])
    trendline=trend[0]*dutchRtime+trend[1]
    
#    plt.plot(dutchRtime,y)
#    plt.plot(fugoidtime,np.exp((fugoidtime-min(t_min))*fit_mn[0]+fit_mn[1]))
#    plt.plot(dutchRtime,dutchRdata2)
#    plt.plot(dutchRtime,trendline)
    
    amplitude = y-trendline
    
    i = 0
    while amplitude[i]>(mx[0]-trendline[start])/2:
        i=i+1
    half_dutchY=((dutchRtime[i])-dutchRtime[start])*60
    
    #short period#
    sh_perioddata = matlab.getdata_at_time('Ahrs1_bPitchRate',matlab.sh_periodstart,matlab.sh_periodstart+matlab.sh_periodtime)
    sh_periodtime = matlab.getdata_at_time('time',matlab.sh_periodstart,matlab.sh_periodstart+matlab.sh_periodtime)
    
    idx_max =  np.r_[True, sh_perioddata[1:] > sh_perioddata[:-1]] & np.r_[sh_perioddata[:-1] > sh_perioddata[1:], True]
    mx = (sh_perioddata[idx_max])[1:]
    t_max=(sh_periodtime[idx_max])[1:]
    half = np.where(sh_perioddata>=(mx[0]-sh_perioddata[-1])/2+sh_perioddata[-1])[0][-1]
    half_short = (sh_periodtime[half]-t_max[0])*60

#    plt.plot(sh_periodtime,sh_perioddata)
    
    
    