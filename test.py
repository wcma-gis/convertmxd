import arcpy

sde_path = r"C:\Files\old\MXDs\blank\PostgreSQL-gisap01-sdc(gisuser)2.sde"
arcpy.env.workspace = sde_path

datasets = arcpy.ListFeatureClasses()
for ds in datasets:
    if "locality" in ds.lower():
        print(ds)
