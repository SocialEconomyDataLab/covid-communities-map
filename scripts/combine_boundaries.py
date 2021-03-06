import geopandas as gpd
import pandas as pd

# msoa columns
# msoa11cd, msoa11nm, MSOA11NM, MSOA11HCLNM, 
# LAD17CD, LAD20CD, LAD20NM, UTLACD, UTLANM, 
# CAUTHCD, CAUTHNM, RGNCD, RGNNM, CTRYCD, 
# CTRYNM, EWCD, EWNM, GBCD, GBNM, UKCD, UKNM, 
# jobs_at_risk_workplace, jobs_at_risk_residence, 
# sales_change_total, sales_change_total_bucket, 
# sales_change_grocery, sales_change_grocery_bucket, 
# vulnerability_score, vulnerability_rank, 
# vulnerability_decile, vulnerability_quintile

# ward columns
# objectid,wd17cd,wd17nm,wd17nmw,bng_e,bng_n,long,lat,
# st_area(shape),st_length(shape),WDNM,
# LADCD,LADNM,SOURCEFILE,LAD20CD,LAD20NM,
# UTLACD,UTLANM,CAUTHCD,CAUTHNM,RGNCD,RGNNM,
# CTRYCD,CTRYNM,EWCD,EWNM,GBCD,GBNM,UKCD,UKNM,
# vulnerability_quintile,sales_change_total,
# sales_change_total_bucket,sales_change_grocery,
# sales_change_grocery_bucket

columns_to_include = [
    'areacode', 'areaname', 'areatype',
    'LAD20CD', 'LAD20NM', 'UTLACD', 'UTLANM',
    'CAUTHCD', 'CAUTHNM', 'RGNCD', 'RGNNM', 'CTRYCD', 'CTRYNM', 
    'EWCD', 'EWNM', 'GBCD', 'GBNM', 'UKCD', 'UKNM',
    'jobs_at_risk_workplace', 'jobs_at_risk_residence',
    'sales_change_total', 'sales_change_total_bucket',
    'sales_change_grocery', 'sales_change_grocery_bucket',
    'vulnerability_quintile', 'geometry',
]

# data on msoas for England, Wales & Scotland
ews = gpd.read_file('data/boundaries/msoa_data.geojson')
ews = ews[ews.CTRYCD != 'N92000002']
ews.loc[:, "areatype"] = 'MSOA'
ews = ews.rename(columns={
    'msoa11cd': 'areacode',
    'MSOA11HCLNM': 'areaname'
})
ews_cols = []
# THIS PART DOESN'T WORK!!
for c in ews.columns:
    if c in columns_to_include:
        ews_cols.append(c)
        continue
    for ci in columns_to_include:
        if c.startswith(ci):
            ews_cols.append(c)
ews = ews[ews_cols]

# data on wards for Northern Ireland
ni = gpd.read_file('data/boundaries/ward_data_ni.geojson')
ni.loc[:, "areatype"] = 'ward'
ni = ni.rename(columns={
    'wd17cd': 'areacode',
    'wd17nm': 'areaname'
})

for c in ews_cols:
    if c not in ni.columns:
        ni.loc[:, c] = None
        ni.loc[:, c] = ni[c].astype('float64')

ni = ni[ews_cols]

uk = gpd.GeoDataFrame(
    pd.concat([ews, ni], ignore_index=True),
    crs=ews.crs
)
uk.drop(columns='geometry').to_csv('data/all_data.csv', index=False)
uk.to_file('data/boundaries/all_data.geojson', driver='GeoJSON')
