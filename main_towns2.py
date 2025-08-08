import arcpy

aprx_path = r"C:\Files\old\blank.aprx"
mxd_path = r"C:\Files\MXDs\IPAWS_Floodplain_.mxd"
shapefile_path = r"C:\Files\shapes\lw\Landscape_Wetlands.shp"
output_aprx_path = r"C:\Files\MXDs\IPAWS_Floodplain_final.aprx"

aprx = arcpy.mp.ArcGISProject(aprx_path)
aprx.importDocument(mxd_path)
map_obj = aprx.listMaps()[0]

target_group = None
anchor_layer = None

for lyr in map_obj.listLayers():
    if lyr.name == "Waterways" and lyr.isGroupLayer:
        target_group = lyr
        break

if target_group:
    for lyr in target_group.listLayers():
        anchor_layer = lyr
        break

temp_layer = map_obj.addDataFromPath(shapefile_path)
temp_layer.name = "Dummy"

if anchor_layer:
    map_obj.moveLayer(anchor_layer, temp_layer, "BEFORE")

aprx.saveACopy(output_aprx_path)
