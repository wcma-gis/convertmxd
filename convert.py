import arcpy
import os
import shutil

to_migrate = "IPAWS_A4_4cats"
print("Start")
src_folder = r"I:\Admin\Software\ESRI\MapTemplates\WCMA Layouts"
src_mxd = os.path.join(src_folder, f"{to_migrate}.mxd")
dest_mxd = fr"C:\files\mig\Original\{to_migrate}.mxd"
shutil.copy(src_mxd, dest_mxd)
aprx = arcpy.mp.ArcGISProject(r"C:\Files\mig\blank.aprx")
aprx.importDocument(dest_mxd)
os.makedirs(fr"C:\files\mig\Converted\{to_migrate}", exist_ok=True)
aprx.saveACopy(fr"C:\files\mig\Converted\{to_migrate}\{to_migrate}.aprx")
print("End")
