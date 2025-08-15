import arcpy
import os
import shutil

dest = r"C:\files\Bryana\grid_aprx\grid_aprx.aprx"
print("Start")
src_mxd = r"C:\files\Bryana\grid\Working.mxd"
aprx = arcpy.mp.ArcGISProject(r"C:\files\mig\blank.aprx")
aprx.importDocument(src_mxd)
aprx.saveACopy(dest)
print("End")
