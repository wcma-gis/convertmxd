import arcpy

def walk_layers(map_obj, parent=None, path=None, depth=0, visited=None, max_depth=10):
    if parent is None:
        print("Top level")
    else:
        print("Parent: ",parent.longName)
    if visited is None:
        visited = set()
    if path is None:
        path = []
    if depth > max_depth:
        return []

    result = []
    layers = map_obj.listLayers(parent) if parent else [lyr for lyr in map_obj.listLayers() if lyr.longName.count('\\') == 0]
    print("Children: ",len(layers))

    for i, lyr in enumerate(layers):
        if parent and lyr == parent:
            continue
        if lyr.isGroupLayer:
            lid = id(lyr)
            if lid in visited:
                continue
            visited.add(lid)
            result.extend(
                walk_layers(map_obj, lyr, path + [lyr.name], depth + 1, visited, max_depth)
            )
        else:
            result.append({
                "layer": lyr,
                "name": lyr.name,
                "parent": parent,
                "index": i,
                "path": path + [lyr.name]
            })
    return result

def collect_layer_hierarchy(map_obj, max_depth=10):
    return walk_layers(map_obj, max_depth=max_depth)

def main():
    mxd_path = r"C:\Files\MXDs\IPAWS_Floodplain_.mxd"
    blank_aprx = r"C:\Files\old\blank.aprx"
    aprx = arcpy.mp.ArcGISProject(blank_aprx)
    aprx.importDocument(mxd_path)

    for m in aprx.listMaps():
        print(f"Map: {m.name}")
        leaf_layers = collect_layer_hierarchy(m)
        for entry in leaf_layers:
            print(" > ".join(entry["path"]))

if __name__ == "__main__":
    main()
