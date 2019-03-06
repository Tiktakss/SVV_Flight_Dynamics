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
from aero_tools import Aero_Tools
aero = Aero_Tools()
from excel_tools import import_excel
excel = import_excel('./Post_Flight_Datasheet_Flight_test.xlsx')
from matlab_tools import Matlab_Tools
matlab = Matlab_Tools()



print(aero.a_alt(1000))




