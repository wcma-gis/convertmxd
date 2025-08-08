import arcpy

def build_layer_hierarchy(map_obj):
    all_layers = map_obj.listLayers()
    result = []

    for i, lyr in enumerate(all_layers):
        parts = lyr.longName.split("\\")
        if not lyr.isGroupLayer:
            result.append({
                "layer": lyr,
                "name": lyr.name,
                "longName": lyr.longName,
                "path": parts,
                "depth": len(parts),
                "index": i
            })

    return result

def main():
    mxd_path = r"C:\Files\MXDs\IPAWS_Floodplain_.mxd"
    blank_aprx = r"C:\Files\old\blank.aprx"
    aprx = arcpy.mp.ArcGISProject(blank_aprx)
    aprx.importDocument(mxd_path)

    for m in aprx.listMaps():
        print(f"Map: {m.name}")
        leaf_layers = build_layer_hierarchy(m)
        for entry in leaf_layers:
            print(" > ".join(entry["path"]))

    aprx.saveACopy(r"C:\Files\dest.aprx")

if __name__ == "__main__":
    main()
