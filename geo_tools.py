
import numpy as np
import zipfile
from xml.dom import minidom
import geopandas as gp

class Geo_Tools:
    def __init__(self,filename):
        self.filename = filename# './FTIScal-20190305_124649.kmz'
        self.file = self.filename[0:-3]+'kml'

    def kmz_to_kml(self):
        """save kmz to kml"""
        zf = zipfile.ZipFile(self.filename,'r')
        for fn in zf.namelist():
            if fn.endswith('.kml'):
                content = zf.read(fn)
                xmldoc = minidom.parseString(content)
                out_name = (self.filename.replace(".kmz",".kml")).replace("\\","/")
                out = open(out_name,'w')
                out.writelines(xmldoc.toxml())
                out.close()
            else:
                print("no kml file")
                

"""
put testing/debugging code in the if-statement below
it will only run if you run this python file (import_files.py)
"""
if __name__ == "__main__":
    geo = Geo_Tools('./FTIScal-20190305_124649.kmz')
    geo.kmz_to_kml()
