import arcpy

def build_leaf_layer_dict(map_obj):
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

def find_group_layer(map_obj, path_parts):
    current = None
    for part in path_parts:
        candidates = map_obj.listLayers(current) if current else map_obj.listLayers()
        current = next((g for g in candidates if g.isGroupLayer and g.name == part), None)
        if current is None:
            break
    return current

def main():
    mxd_path = r"C:\Files\MXDs\IPAWS_Floodplain_.mxd"
    blank_aprx = r"C:\Files\old\blank.aprx"
    shapefile_path = r"C:\Files\shapes\lw\Landscape_Wetlands.shp"

    aprx = arcpy.mp.ArcGISProject(blank_aprx)
    aprx.importDocument(mxd_path)

    for m in aprx.listMaps():
        layers = build_leaf_layer_dict(m)
        target = None
        for entry in layers:
            if entry["name"] == "Major Towns":
                target = entry
                break

        if not target:
            print("Major Towns not found")
            continue

        group_path = target["path"][:-1]
        group_layer = find_group_layer(m, group_path)
        siblings = m.listLayers(group_layer)

        target_index = -1
        for i, lyr in enumerate(siblings):
            if lyr.name == "Major Towns":
                target_index = i
                break

        if target_index == -1:
            print("Layer found in path but not as sibling — skipping")
            continue

        m.removeLayer(target["layer"])
        print("Removed original Major Towns")

        new_layer = m.addDataFromPath(shapefile_path)
        new_layer.name = "Major Towns"

        reference_layer = siblings[target_index - 1] if target_index > 0 else None
        m.insertLayer(group_layer, reference_layer, new_layer, "AFTER")
        print("Inserted new 'Major Towns' layer from shapefile into:", " > ".join(group_path))

    aprx.saveACopy(r"C:\Files\dest.aprx")

if __name__ == "__main__":
    main()
