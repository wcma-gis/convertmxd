import arcpy, os

class Toolbox(object):
    def __init__(self):
        self.label = "PixelLabels"
        self.alias = "PixelLabels"
        self.tools = [ClipRasterToSelectionAndPoints]

class ClipRasterToSelectionAndPoints(object):
    def __init__(self):
        self.label = "Raster→Points (label-ready)"
        self.canRunInBackground = False
    def getParameterInfo(self):
        p0 = arcpy.Parameter(displayName="Input raster layer", name="in_raster", datatype="GPRasterLayer", parameterType="Required", direction="Input")
        p1 = arcpy.Parameter(displayName="Parcel layer (use current selection)", name="parcel_lyr", datatype="GPFeatureLayer", parameterType="Required", direction="Input")
        p2 = arcpy.Parameter(displayName="Output points", name="out_points", datatype="DEFeatureClass", parameterType="Required", direction="Output")
        p3 = arcpy.Parameter(displayName="Decimals", name="decimals", datatype="GPLong", parameterType="Optional", direction="Input")
        p3.value = 2
        return [p0,p1,p2,p3]
    def execute(self, params, messages):
        in_ras = params[0].valueAsText
        parcels = params[1].valueAsText
        out_pts = params[2].valueAsText
        decs = int(params[3].value or 2)
        arcpy.env.overwriteOutput = True
        mxd = arcpy.mapping.MapDocument("CURRENT")
        df = mxd.activeDataFrame
        tmp_gdb = arcpy.env.scratchGDB
        tmp_clip = os.path.join(tmp_gdb, "tmp_clip_ras")
        arcpy.Clip_management(in_ras, "#", tmp_clip, parcels, "#", "ClippingGeometry", "NONE")
        arcpy.RasterToPoint_conversion(tmp_clip, out_pts, "VALUE")
        try:
            arcpy.Delete_management(tmp_clip)
        except:
            pass
        try:
            lyr = arcpy.mapping.Layer(out_pts)
            arcpy.mapping.AddLayer(df, lyr, "TOP")
            for l in arcpy.mapping.ListLayers(mxd, os.path.basename(out_pts), df):
                if l.supports("SHOWLABELS"):
                    l.showLabels = True
                    lc = l.labelClasses[0]
                    lc.expressionParser = "VBScript"
                    lc.expression = 'FormatNumber([grid_code], {0})'.format(decs) if "grid_code" in [f.name for f in arcpy.ListFields(out_pts)] else 'FormatNumber([VALUE], {0})'.format(decs)
            arcpy.RefreshActiveView(); arcpy.RefreshTOC()
        except:
            pass
