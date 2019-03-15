
import numpy as np
import pandas as pd

# this class contains "info" functions for column naming/data clearity in arrays

class import_excel:
    def __init__(self,filename):
        self.filename = filename#'./Post_Flight_Datasheet_Flight_test.xlsx'
        self.filename = filename# './Post_Flight_Datasheet_03_05_V3.xlsx'
        self.cg_seats = np.array([[131,131,170,214,214,251,251,288,288]])*0.025 # inch to m
        self.blockfuel = self.file().values[16,3]
        
    
    def file(self):
        return pd.read_excel(self.filename)
    
    def people(self):
        people = self.file().iloc[6:15,0:8].values
        people = people[:,[0,3,7]]
        return  np.c_[people,np.transpose(self.cg_seats)]
    
    def people_info(self):
        return ['location_name,name,weight,cg_location']
    
    def names(self):
        return self.people()[:,1]
    
    def location_name(self):
        return self.people()[:,0]
    
    def location(self,frontisTrue):
        normal = self.people()[:,3]
        if frontisTrue:
            normal[-1] = self.cg_seats[0]+0.30 # just behind pilot seats
        return normal
    
    def weights(self):
        return self.people()[:,2]
    
    # print for clearity
    def Cl_Cd_data_info(self):
        return self.file().values[23:25,0:10]
    
    def Cl_Cd_data(self):
        return self.file().values[26:32,0:10]
    
    def trimcurve_data(self):
        return self.file().values[57:64,0:14]
    
    def trimcurve_data_info(self):
        return self.file().values[54:56,0:14]
    
    def cg_shift_data(self):
        return self.file().values[73:75,0:14]
    
    def cg_shift_data_info(self):
        return self.file().values[71:73,0:14]
    
        
        
"""
put testing/debugging code in the if-statement below
it will only run if you run this python file (import_files.py)
"""
if __name__ == "__main__":
    excel = import_excel('./Post_Flight_Datasheet_03_05_V3.xlsx')
    
    print ('people: ', excel.people_info())
    print ('\nCl_Cd: ', excel.Cl_Cd_data_info())
    print ('\nTrimcurve: ', excel.trimcurve_data_info())

    

