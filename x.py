import arcpy, os

class Toolbox(object):
    def __init__(self):
        self.label = "PixelLabels"
        self.alias = "PixelLabels"
        self.tools = [RasterToPointsLabel]

class RasterToPointsLabel(object):
    def __init__(self):
        self.label = "Raster→Points (whole raster)"
        self.canRunInBackground = False
    def getParameterInfo(self):
        p0 = arcpy.Parameter(displayName="Input raster layer", name="in_raster", datatype="GPRasterLayer", parameterType="Required", direction="Input")
        p1 = arcpy.Parameter(displayName="Output points", name="out_points", datatype="DEFeatureClass", parameterType="Required", direction="Output")
        p2 = arcpy.Parameter(displayName="Decimals", name="decimals", datatype="GPLong", parameterType="Optional", direction="Input")
        p2.value = 2
        return [p0,p1,p2]
    def execute(self, params, messages):
        in_ras = params[0].valueAsText
        out_pts = params[1].valueAsText
        decs = int(params[2].value or 2)
        arcpy.env.overwriteOutput = True
        mxd = arcpy.mapping.MapDocument("CURRENT")
        df = mxd.activeDataFrame
        arcpy.RasterToPoint_conversion(in_ras, out_pts, "VALUE")
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
