import arcpy
import os
import shutil

to_migrate = "Drought refuge locations"
print("Start")
src_folder = r"C:\files\Deb\20250520_drought refuge locations"
src_mxd = os.path.join(src_folder, f"{to_migrate}.mxd")
aprx = arcpy.mp.ArcGISProject(r"C:\Files\mig\blank.aprx")
aprx.importDocument(src_mxd)
os.makedirs(fr"C:\files\mig\{to_migrate}", exist_ok=True)
aprx.saveACopy(fr"C:\files\mig\{to_migrate}\{to_migrate}.aprx")
print("End")
