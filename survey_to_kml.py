import pandas as pd
from pyproj import Transformer, CRS
import simplekml
import os

# =============================================================================
# NAD83 State Plane Zones (US Survey Feet) — proj.org definitions
# =============================================================================
ZONES = {
    "AR: Arkansas North": "+proj=lcc +lat_0=34.3333333333333 +lon_0=-92 +lat_1=36.2333333333333 +lat_2=34.9333333333333 +x_0=400000.0000 +y_0=0.0000 +ellps=GRS80 +datum=NAD83 +to_meter=0.3048006096012192 +no_defs",
    "AR: Arkansas South": "+proj=lcc +lat_0=32.6666666666667 +lon_0=-92 +lat_1=34.7666666666667 +lat_2=33.3 +x_0=400000.0000 +y_0=400000.0000 +ellps=GRS80 +datum=NAD83 +to_meter=0.3048006096012192 +no_defs",
    "AZ: Arizona Central (ft)": "+proj=tmerc +lat_0=31 +lon_0=-111.916666666667 +k=0.9999 +x_0=213360.0000 +y_0=0.0000 +ellps=GRS80 +datum=NAD83 +to_meter=0.3048006096012192 +no_defs",
    "AZ: Arizona East (ft)": "+proj=tmerc +lat_0=31 +lon_0=-110.166666666667 +k=0.9999 +x_0=213360.0000 +y_0=0.0000 +ellps=GRS80 +datum=NAD83 +to_meter=0.3048006096012192 +no_defs",
    "AZ: Arizona West (ft)": "+proj=tmerc +lat_0=31 +lon_0=-113.75 +k=0.999933333 +x_0=213360.0000 +y_0=0.0000 +ellps=GRS80 +datum=NAD83 +to_meter=0.3048006096012192 +no_defs",
    "CA: California zone 1": "+proj=lcc +lat_0=39.3333333333333 +lon_0=-122 +lat_1=41.6666666666667 +lat_2=40 +x_0=2000000.0001 +y_0=500000.0001 +ellps=GRS80 +datum=NAD83 +to_meter=0.3048006096012192 +no_defs",
    "CA: California zone 2": "+proj=lcc +lat_0=37.6666666666667 +lon_0=-122 +lat_1=39.8333333333333 +lat_2=38.3333333333333 +x_0=2000000.0001 +y_0=500000.0001 +ellps=GRS80 +datum=NAD83 +to_meter=0.3048006096012192 +no_defs",
    "CA: California zone 3": "+proj=lcc +lat_0=36.5 +lon_0=-120.5 +lat_1=38.4333333333333 +lat_2=37.0666666666667 +x_0=2000000.0001 +y_0=500000.0001 +ellps=GRS80 +datum=NAD83 +to_meter=0.3048006096012192 +no_defs",
    "CA: California zone 4": "+proj=lcc +lat_0=35.3333333333333 +lon_0=-119 +lat_1=37.25 +lat_2=36 +x_0=2000000.0001 +y_0=500000.0001 +ellps=GRS80 +datum=NAD83 +to_meter=0.3048006096012192 +no_defs",
    "CA: California zone 5": "+proj=lcc +lat_0=33.5 +lon_0=-118 +lat_1=35.4666666666667 +lat_2=34.0333333333333 +x_0=2000000.0001 +y_0=500000.0001 +ellps=GRS80 +datum=NAD83 +to_meter=0.3048006096012192 +no_defs",
    "CA: California zone 6": "+proj=lcc +lat_0=32.1666666666667 +lon_0=-116.25 +lat_1=33.8833333333333 +lat_2=32.7833333333333 +x_0=2000000.0001 +y_0=500000.0001 +ellps=GRS80 +datum=NAD83 +to_meter=0.3048006096012192 +no_defs",
    "CO: Colorado Central": "+proj=lcc +lat_0=37.8333333333333 +lon_0=-105.5 +lat_1=39.75 +lat_2=38.45 +x_0=914401.8288 +y_0=304800.6096 +ellps=GRS80 +datum=NAD83 +to_meter=0.3048006096012192 +no_defs",
    "CO: Colorado North": "+proj=lcc +lat_0=39.3333333333333 +lon_0=-105.5 +lat_1=40.7833333333333 +lat_2=39.7166666666667 +x_0=914401.8288 +y_0=304800.6096 +ellps=GRS80 +datum=NAD83 +to_meter=0.3048006096012192 +no_defs",
    "CO: Colorado South": "+proj=lcc +lat_0=36.6666666666667 +lon_0=-105.5 +lat_1=38.4333333333333 +lat_2=37.2333333333333 +x_0=914401.8288 +y_0=304800.6096 +ellps=GRS80 +datum=NAD83 +to_meter=0.3048006096012192 +no_defs",
    "CT: Connecticut": "+proj=lcc +lat_0=40.8333333333333 +lon_0=-72.75 +lat_1=41.8666666666667 +lat_2=41.2 +x_0=304800.6096 +y_0=152400.3048 +ellps=GRS80 +datum=NAD83 +to_meter=0.3048006096012192 +no_defs",
    "DE: Delaware": "+proj=tmerc +lat_0=38 +lon_0=-75.4166666666667 +k=0.999995 +x_0=200000.0001 +y_0=0.0000 +ellps=GRS80 +datum=NAD83 +to_meter=0.3048006096012192 +no_defs",
    "FL: Florida East": "+proj=tmerc +lat_0=24.3333333333333 +lon_0=-81 +k=0.999941177 +x_0=200000.0001 +y_0=0.0000 +ellps=GRS80 +datum=NAD83 +to_meter=0.3048006096012192 +no_defs",
    "FL: Florida North": "+proj=lcc +lat_0=29 +lon_0=-84.5 +lat_1=30.75 +lat_2=29.5833333333333 +x_0=600000.0000 +y_0=0.0000 +ellps=GRS80 +datum=NAD83 +to_meter=0.3048006096012192 +no_defs",
    "FL: Florida West": "+proj=tmerc +lat_0=24.3333333333333 +lon_0=-82 +k=0.999941177 +x_0=200000.0001 +y_0=0.0000 +ellps=GRS80 +datum=NAD83 +to_meter=0.3048006096012192 +no_defs",
    "GA: Georgia East": "+proj=tmerc +lat_0=30 +lon_0=-82.1666666666667 +k=0.9999 +x_0=200000.0001 +y_0=0.0000 +ellps=GRS80 +datum=NAD83 +to_meter=0.3048006096012192 +no_defs",
    "GA: Georgia West": "+proj=tmerc +lat_0=30 +lon_0=-84.1666666666667 +k=0.9999 +x_0=699999.9999 +y_0=0.0000 +ellps=GRS80 +datum=NAD83 +to_meter=0.3048006096012192 +no_defs",
    "IA: Iowa North": "+proj=lcc +lat_0=41.5 +lon_0=-93.5 +lat_1=43.2666666666667 +lat_2=42.0666666666667 +x_0=1500000.0000 +y_0=1000000.0000 +ellps=GRS80 +datum=NAD83 +to_meter=0.3048006096012192 +no_defs",
    "IA: Iowa South": "+proj=lcc +lat_0=40 +lon_0=-93.5 +lat_1=41.7833333333333 +lat_2=40.6166666666667 +x_0=500000.0000 +y_0=0.0000 +ellps=GRS80 +datum=NAD83 +to_meter=0.3048006096012192 +no_defs",
    "ID: Idaho Central": "+proj=tmerc +lat_0=41.6666666666667 +lon_0=-114 +k=0.999947368 +x_0=500000.0001 +y_0=0.0000 +ellps=GRS80 +datum=NAD83 +to_meter=0.3048006096012192 +no_defs",
    "ID: Idaho East": "+proj=tmerc +lat_0=41.6666666666667 +lon_0=-112.166666666667 +k=0.999947368 +x_0=200000.0001 +y_0=0.0000 +ellps=GRS80 +datum=NAD83 +to_meter=0.3048006096012192 +no_defs",
    "ID: Idaho West": "+proj=tmerc +lat_0=41.6666666666667 +lon_0=-115.75 +k=0.999933333 +x_0=800000.0001 +y_0=0.0000 +ellps=GRS80 +datum=NAD83 +to_meter=0.3048006096012192 +no_defs",
    "IL: Illinois East": "+proj=tmerc +lat_0=36.6666666666667 +lon_0=-88.3333333333333 +k=0.999975 +x_0=300000.0000 +y_0=0.0000 +ellps=GRS80 +datum=NAD83 +to_meter=0.3048006096012192 +no_defs",
    "IL: Illinois West": "+proj=tmerc +lat_0=36.6666666666667 +lon_0=-90.1666666666667 +k=0.999941177 +x_0=700000.0000 +y_0=0.0000 +ellps=GRS80 +datum=NAD83 +to_meter=0.3048006096012192 +no_defs",
    "IN: Indiana East": "+proj=tmerc +lat_0=37.5 +lon_0=-85.6666666666667 +k=0.999966667 +x_0=99999.9999 +y_0=249999.9999 +ellps=GRS80 +datum=NAD83 +to_meter=0.3048006096012192 +no_defs",
    "IN: Indiana West": "+proj=tmerc +lat_0=37.5 +lon_0=-87.0833333333333 +k=0.999966667 +x_0=900000.0000 +y_0=249999.9999 +ellps=GRS80 +datum=NAD83 +to_meter=0.3048006096012192 +no_defs",
    "KS: Kansas LCC": "+proj=lcc +lat_0=36 +lon_0=-98.25 +lat_1=39.5 +lat_2=37.5 +x_0=400000.0000 +y_0=0.0000 +ellps=GRS80 +datum=NAD83 +to_meter=0.3048006096012192 +no_defs",
    "KS: Kansas North": "+proj=lcc +lat_0=38.3333333333333 +lon_0=-98 +lat_1=39.7833333333333 +lat_2=38.7166666666667 +x_0=400000.0000 +y_0=0.0000 +ellps=GRS80 +datum=NAD83 +to_meter=0.3048006096012192 +no_defs",
    "KS: Kansas South": "+proj=lcc +lat_0=36.6666666666667 +lon_0=-98.5 +lat_1=38.5666666666667 +lat_2=37.2666666666667 +x_0=400000.0000 +y_0=400000.0000 +ellps=GRS80 +datum=NAD83 +to_meter=0.3048006096012192 +no_defs",
    "KY: Kentucky North": "+proj=lcc +lat_0=37.5 +lon_0=-84.25 +lat_1=37.9666666666667 +lat_2=38.9666666666667 +x_0=500000.0001 +y_0=0.0000 +ellps=GRS80 +datum=NAD83 +to_meter=0.3048006096012192 +no_defs",
    "KY: Kentucky South": "+proj=lcc +lat_0=36.3333333333333 +lon_0=-85.75 +lat_1=37.9333333333333 +lat_2=36.7333333333333 +x_0=500000.0001 +y_0=500000.0001 +ellps=GRS80 +datum=NAD83 +to_meter=0.3048006096012192 +no_defs",
    "LA: Louisiana North": "+proj=lcc +lat_0=30.5 +lon_0=-92.5 +lat_1=32.6666666666667 +lat_2=31.1666666666667 +x_0=1000000.0000 +y_0=0.0000 +ellps=GRS80 +datum=NAD83 +to_meter=0.3048006096012192 +no_defs",
    "LA: Louisiana Offshore": "+proj=lcc +lat_0=25.5 +lon_0=-91.3333333333333 +lat_1=27.8333333333333 +lat_2=26.1666666666667 +x_0=1000000.0000 +y_0=0.0000 +ellps=GRS80 +datum=NAD83 +to_meter=0.3048006096012192 +no_defs",
    "LA: Louisiana South": "+proj=lcc +lat_0=28.5 +lon_0=-91.3333333333333 +lat_1=30.7 +lat_2=29.3 +x_0=1000000.0000 +y_0=0.0000 +ellps=GRS80 +datum=NAD83 +to_meter=0.3048006096012192 +no_defs",
    "MA: Massachusetts Island": "+proj=lcc +lat_0=41 +lon_0=-70.5 +lat_1=41.4833333333333 +lat_2=41.2833333333333 +x_0=500000.0001 +y_0=0.0000 +ellps=GRS80 +datum=NAD83 +to_meter=0.3048006096012192 +no_defs",
    "MA: Massachusetts Mainland": "+proj=lcc +lat_0=41 +lon_0=-71.5 +lat_1=42.6833333333333 +lat_2=41.7166666666667 +x_0=200000.0001 +y_0=750000.0000 +ellps=GRS80 +datum=NAD83 +to_meter=0.3048006096012192 +no_defs",
    "MD: Maryland": "+proj=lcc +lat_0=37.6666666666667 +lon_0=-77 +lat_1=39.45 +lat_2=38.3 +x_0=399999.9999 +y_0=0.0000 +ellps=GRS80 +datum=NAD83 +to_meter=0.3048006096012192 +no_defs",
    "ME: Maine East": "+proj=tmerc +lat_0=43.6666666666667 +lon_0=-68.5 +k=0.9999 +x_0=300000.0000 +y_0=0.0000 +ellps=GRS80 +datum=NAD83 +to_meter=0.3048006096012192 +no_defs",
    "ME: Maine West": "+proj=tmerc +lat_0=42.8333333333333 +lon_0=-70.1666666666667 +k=0.999966667 +x_0=900000.0000 +y_0=0.0000 +ellps=GRS80 +datum=NAD83 +to_meter=0.3048006096012192 +no_defs",
    "MI: Michigan Central (ft)": "+proj=lcc +lat_0=43.3166666666667 +lon_0=-84.3666666666667 +lat_1=45.7 +lat_2=44.1833333333333 +x_0=6000000.0000 +y_0=0.0000 +ellps=GRS80 +datum=NAD83 +to_meter=0.3048006096012192 +no_defs",
    "MI: Michigan North (ft)": "+proj=lcc +lat_0=44.7833333333333 +lon_0=-87 +lat_1=47.0833333333333 +lat_2=45.4833333333333 +x_0=8000000.0000 +y_0=0.0000 +ellps=GRS80 +datum=NAD83 +to_meter=0.3048006096012192 +no_defs",
    "MI: Michigan South (ft)": "+proj=lcc +lat_0=41.5 +lon_0=-84.3666666666667 +lat_1=43.6666666666667 +lat_2=42.1 +x_0=4000000.0000 +y_0=0.0000 +ellps=GRS80 +datum=NAD83 +to_meter=0.3048006096012192 +no_defs",
    "MN: Minnesota Central": "+proj=lcc +lat_0=45 +lon_0=-94.25 +lat_1=47.05 +lat_2=45.6166666666667 +x_0=800000.0000 +y_0=100000.0000 +ellps=GRS80 +datum=NAD83 +to_meter=0.3048006096012192 +no_defs",
    "MN: Minnesota North": "+proj=lcc +lat_0=46.5 +lon_0=-93.1 +lat_1=48.6333333333333 +lat_2=47.0333333333333 +x_0=800000.0000 +y_0=100000.0000 +ellps=GRS80 +datum=NAD83 +to_meter=0.3048006096012192 +no_defs",
    "MN: Minnesota South": "+proj=lcc +lat_0=43 +lon_0=-94 +lat_1=45.2166666666667 +lat_2=43.7833333333333 +x_0=800000.0000 +y_0=100000.0000 +ellps=GRS80 +datum=NAD83 +to_meter=0.3048006096012192 +no_defs",
    "MS: Mississippi East": "+proj=tmerc +lat_0=29.5 +lon_0=-88.8333333333333 +k=0.99995 +x_0=300000.0000 +y_0=0.0000 +ellps=GRS80 +datum=NAD83 +to_meter=0.3048006096012192 +no_defs",
    "MS: Mississippi West": "+proj=tmerc +lat_0=29.5 +lon_0=-90.3333333333333 +k=0.99995 +x_0=699999.9999 +y_0=0.0000 +ellps=GRS80 +datum=NAD83 +to_meter=0.3048006096012192 +no_defs",
    "MT: Montana (ft)": "+proj=lcc +lat_0=44.25 +lon_0=-109.5 +lat_1=49 +lat_2=45 +x_0=600000.0000 +y_0=0.0000 +ellps=GRS80 +datum=NAD83 +to_meter=0.3048006096012192 +no_defs",
    "NC: North Carolina": "+proj=lcc +lat_0=33.75 +lon_0=-79 +lat_1=36.1666666666667 +lat_2=34.3333333333333 +x_0=609601.2192 +y_0=0.0000 +ellps=GRS80 +datum=NAD83 +to_meter=0.3048006096012192 +no_defs",
    "ND: North Dakota North (ft)": "+proj=lcc +lat_0=47 +lon_0=-100.5 +lat_1=48.7333333333333 +lat_2=47.4333333333333 +x_0=600000.0000 +y_0=0.0000 +ellps=GRS80 +datum=NAD83 +to_meter=0.3048006096012192 +no_defs",
    "ND: North Dakota South (ft)": "+proj=lcc +lat_0=45.6666666666667 +lon_0=-100.5 +lat_1=47.4833333333333 +lat_2=46.1833333333333 +x_0=600000.0000 +y_0=0.0000 +ellps=GRS80 +datum=NAD83 +to_meter=0.3048006096012192 +no_defs",
    "NE: Nebraska": "+proj=lcc +lat_0=39.8333333333333 +lon_0=-100 +lat_1=43 +lat_2=40 +x_0=500000.0000 +y_0=0.0000 +ellps=GRS80 +datum=NAD83 +to_meter=0.3048006096012192 +no_defs",
    "NH: New Hampshire": "+proj=tmerc +lat_0=42.5 +lon_0=-71.6666666666667 +k=0.999966667 +x_0=300000.0000 +y_0=0.0000 +ellps=GRS80 +datum=NAD83 +to_meter=0.3048006096012192 +no_defs",
    "NJ: New Jersey": "+proj=tmerc +lat_0=38.8333333333333 +lon_0=-74.5 +k=0.9999 +x_0=150000.0000 +y_0=0.0000 +ellps=GRS80 +datum=NAD83 +to_meter=0.3048006096012192 +no_defs",
    "NM: New Mexico Central": "+proj=tmerc +lat_0=31 +lon_0=-106.25 +k=0.9999 +x_0=500000.0001 +y_0=0.0000 +ellps=GRS80 +datum=NAD83 +to_meter=0.3048006096012192 +no_defs",
    "NM: New Mexico East": "+proj=tmerc +lat_0=31 +lon_0=-104.333333333333 +k=0.999909091 +x_0=165000.0000 +y_0=0.0000 +ellps=GRS80 +datum=NAD83 +to_meter=0.3048006096012192 +no_defs",
    "NM: New Mexico West": "+proj=tmerc +lat_0=31 +lon_0=-107.833333333333 +k=0.999916667 +x_0=830000.0001 +y_0=0.0000 +ellps=GRS80 +datum=NAD83 +to_meter=0.3048006096012192 +no_defs",
    "NV: Nevada Central": "+proj=tmerc +lat_0=34.75 +lon_0=-116.666666666667 +k=0.9999 +x_0=500000.0000 +y_0=6000000.0000 +ellps=GRS80 +datum=NAD83 +to_meter=0.3048006096012192 +no_defs",
    "NV: Nevada East": "+proj=tmerc +lat_0=34.75 +lon_0=-115.583333333333 +k=0.9999 +x_0=200000.0000 +y_0=8000000.0000 +ellps=GRS80 +datum=NAD83 +to_meter=0.3048006096012192 +no_defs",
    "NV: Nevada West": "+proj=tmerc +lat_0=34.75 +lon_0=-118.583333333333 +k=0.9999 +x_0=800000.0000 +y_0=4000000.0000 +ellps=GRS80 +datum=NAD83 +to_meter=0.3048006096012192 +no_defs",
    "NY: New York Central": "+proj=tmerc +lat_0=40 +lon_0=-76.5833333333333 +k=0.9999375 +x_0=249999.9999 +y_0=0.0000 +ellps=GRS80 +datum=NAD83 +to_meter=0.3048006096012192 +no_defs",
    "NY: New York East": "+proj=tmerc +lat_0=38.8333333333333 +lon_0=-74.5 +k=0.9999 +x_0=150000.0000 +y_0=0.0000 +ellps=GRS80 +datum=NAD83 +to_meter=0.3048006096012192 +no_defs",
    "NY: New York West": "+proj=tmerc +lat_0=40 +lon_0=-78.5833333333333 +k=0.9999375 +x_0=350000.0001 +y_0=0.0000 +ellps=GRS80 +datum=NAD83 +to_meter=0.3048006096012192 +no_defs",
    "OH: Ohio North": "+proj=lcc +lat_0=39.6666666666667 +lon_0=-82.5 +lat_1=41.7 +lat_2=40.4333333333333 +x_0=600000.0000 +y_0=0.0000 +ellps=GRS80 +datum=NAD83 +to_meter=0.3048006096012192 +no_defs",
    "OH: Ohio South": "+proj=lcc +lat_0=38 +lon_0=-82.5 +lat_1=40.0333333333333 +lat_2=38.7333333333333 +x_0=600000.0000 +y_0=0.0000 +ellps=GRS80 +datum=NAD83 +to_meter=0.3048006096012192 +no_defs",
    "OK: Oklahoma North": "+proj=lcc +lat_0=35 +lon_0=-98 +lat_1=36.7666666666667 +lat_2=35.5666666666667 +x_0=600000.0000 +y_0=0.0000 +ellps=GRS80 +datum=NAD83 +to_meter=0.3048006096012192 +no_defs",
    "OK: Oklahoma South": "+proj=lcc +lat_0=33.3333333333333 +lon_0=-98 +lat_1=35.2333333333333 +lat_2=33.9333333333333 +x_0=600000.0000 +y_0=0.0000 +ellps=GRS80 +datum=NAD83 +to_meter=0.3048006096012192 +no_defs",
    "OR: Oregon North (ft)": "+proj=lcc +lat_0=43.6666666666667 +lon_0=-120.5 +lat_1=46 +lat_2=44.3333333333333 +x_0=2500000.0001 +y_0=0.0000 +ellps=GRS80 +datum=NAD83 +to_meter=0.3048006096012192 +no_defs",
    "OR: Oregon South (ft)": "+proj=lcc +lat_0=41.6666666666667 +lon_0=-120.5 +lat_1=44 +lat_2=42.3333333333333 +x_0=1500000.0001 +y_0=0.0000 +ellps=GRS80 +datum=NAD83 +to_meter=0.3048006096012192 +no_defs",
    "PA: Pennsylvania North": "+proj=lcc +lat_0=40.1666666666667 +lon_0=-77.75 +lat_1=41.95 +lat_2=40.8833333333333 +x_0=600000.0000 +y_0=0.0000 +ellps=GRS80 +datum=NAD83 +to_meter=0.3048006096012192 +no_defs",
    "PA: Pennsylvania South": "+proj=lcc +lat_0=39.3333333333333 +lon_0=-77.75 +lat_1=40.9666666666667 +lat_2=39.9333333333333 +x_0=600000.0000 +y_0=0.0000 +ellps=GRS80 +datum=NAD83 +to_meter=0.3048006096012192 +no_defs",
    "RI: Rhode Island": "+proj=tmerc +lat_0=41.0833333333333 +lon_0=-71.5 +k=0.99999375 +x_0=100000.0000 +y_0=0.0000 +ellps=GRS80 +datum=NAD83 +to_meter=0.3048006096012192 +no_defs",
    "SC: South Carolina (ft)": "+proj=lcc +lat_0=31.8333333333333 +lon_0=-81 +lat_1=34.8333333333333 +lat_2=32.5 +x_0=609600.0000 +y_0=0.0000 +ellps=GRS80 +datum=NAD83 +to_meter=0.3048006096012192 +no_defs",
    "TN: Tennessee": "+proj=lcc +lat_0=34.3333333333333 +lon_0=-86 +lat_1=36.4166666666667 +lat_2=35.25 +x_0=600000.0000 +y_0=0.0000 +ellps=GRS80 +datum=NAD83 +to_meter=0.3048006096012192 +no_defs",
    "TX: Texas Central": "+proj=lcc +lat_0=29.6666666666667 +lon_0=-100.333333333333 +lat_1=31.8833333333333 +lat_2=30.1166666666667 +x_0=699999.9999 +y_0=3000000.0000 +ellps=GRS80 +datum=NAD83 +to_meter=0.3048006096012192 +no_defs",
    "TX: Texas North Central": "+proj=lcc +lat_0=31.6666666666667 +lon_0=-98.5 +lat_1=33.9666666666667 +lat_2=32.1333333333333 +x_0=600000.0000 +y_0=2000000.0001 +ellps=GRS80 +datum=NAD83 +to_meter=0.3048006096012192 +no_defs",
    "TX: Texas North": "+proj=lcc +lat_0=34 +lon_0=-101.5 +lat_1=36.1833333333333 +lat_2=34.65 +x_0=200000.0001 +y_0=999999.9999 +ellps=GRS80 +datum=NAD83 +to_meter=0.3048006096012192 +no_defs",
    "TX: Texas South Central": "+proj=lcc +lat_0=27.8333333333333 +lon_0=-99 +lat_1=30.2833333333333 +lat_2=28.3833333333333 +x_0=600000.0000 +y_0=3999999.9999 +ellps=GRS80 +datum=NAD83 +to_meter=0.3048006096012192 +no_defs",
    "TX: Texas South": "+proj=lcc +lat_0=25.6666666666667 +lon_0=-98.5 +lat_1=27.8333333333333 +lat_2=26.1666666666667 +x_0=300000.0000 +y_0=5000000.0001 +ellps=GRS80 +datum=NAD83 +to_meter=0.3048006096012192 +no_defs",
    "UT: Utah Central (ft)": "+proj=lcc +lat_0=38.3333333333333 +lon_0=-111.5 +lat_1=40.65 +lat_2=39.0166666666667 +x_0=500000.0002 +y_0=2000000.0000 +ellps=GRS80 +datum=NAD83 +to_meter=0.3048006096012192 +no_defs",
    "UT: Utah Central": "+proj=lcc +lat_0=38.3333333333333 +lon_0=-111.5 +lat_1=40.65 +lat_2=39.0166666666667 +x_0=500000.0000 +y_0=2000000.0000 +ellps=GRS80 +datum=NAD83 +to_meter=0.3048006096012192 +no_defs",
    "UT: Utah North (ft)": "+proj=lcc +lat_0=40.3333333333333 +lon_0=-111.5 +lat_1=41.7833333333333 +lat_2=40.7166666666667 +x_0=500000.0002 +y_0=1000000.0000 +ellps=GRS80 +datum=NAD83 +to_meter=0.3048006096012192 +no_defs",
    "UT: Utah North": "+proj=lcc +lat_0=40.3333333333333 +lon_0=-111.5 +lat_1=41.7833333333333 +lat_2=40.7166666666667 +x_0=500000.0000 +y_0=1000000.0000 +ellps=GRS80 +datum=NAD83 +to_meter=0.3048006096012192 +no_defs",
    "UT: Utah South (ft)": "+proj=lcc +lat_0=36.6666666666667 +lon_0=-111.5 +lat_1=38.35 +lat_2=37.2166666666667 +x_0=500000.0002 +y_0=3000000.0000 +ellps=GRS80 +datum=NAD83 +to_meter=0.3048006096012192 +no_defs",
    "UT: Utah South": "+proj=lcc +lat_0=36.6666666666667 +lon_0=-111.5 +lat_1=38.35 +lat_2=37.2166666666667 +x_0=500000.0000 +y_0=3000000.0000 +ellps=GRS80 +datum=NAD83 +to_meter=0.3048006096012192 +no_defs",
    "VA: Virginia North": "+proj=lcc +lat_0=37.6666666666667 +lon_0=-78.5 +lat_1=39.2 +lat_2=38.0333333333333 +x_0=3500000.0001 +y_0=2000000.0001 +ellps=GRS80 +datum=NAD83 +to_meter=0.3048006096012192 +no_defs",
    "VA: Virginia South": "+proj=lcc +lat_0=36.3333333333333 +lon_0=-78.5 +lat_1=37.9666666666667 +lat_2=36.7666666666667 +x_0=3500000.0001 +y_0=999999.9999 +ellps=GRS80 +datum=NAD83 +to_meter=0.3048006096012192 +no_defs",
    "WA: Washington North": "+proj=lcc +lat_0=47 +lon_0=-120.833333333333 +lat_1=48.7333333333333 +lat_2=47.5 +x_0=500000.0001 +y_0=0.0000 +ellps=GRS80 +datum=NAD83 +to_meter=0.3048006096012192 +no_defs",
    "WA: Washington South": "+proj=lcc +lat_0=45.3333333333333 +lon_0=-120.5 +lat_1=47.3333333333333 +lat_2=45.8333333333333 +x_0=500000.0001 +y_0=0.0000 +ellps=GRS80 +datum=NAD83 +to_meter=0.3048006096012192 +no_defs",
    "WI: Wisconsin Central": "+proj=lcc +lat_0=43.8333333333333 +lon_0=-90 +lat_1=45.5 +lat_2=44.25 +x_0=600000.0000 +y_0=0.0000 +ellps=GRS80 +datum=NAD83 +to_meter=0.3048006096012192 +no_defs",
    "WI: Wisconsin North": "+proj=lcc +lat_0=45.1666666666667 +lon_0=-90 +lat_1=46.7666666666667 +lat_2=45.5666666666667 +x_0=600000.0000 +y_0=0.0000 +ellps=GRS80 +datum=NAD83 +to_meter=0.3048006096012192 +no_defs",
    "WI: Wisconsin South": "+proj=lcc +lat_0=42 +lon_0=-90 +lat_1=44.0666666666667 +lat_2=42.7333333333333 +x_0=600000.0000 +y_0=0.0000 +ellps=GRS80 +datum=NAD83 +to_meter=0.3048006096012192 +no_defs",
    "WY: Wyoming East": "+proj=tmerc +lat_0=40.5 +lon_0=-105.166666666667 +k=0.9999375 +x_0=200000.0000 +y_0=0.0000 +ellps=GRS80 +datum=NAD83 +to_meter=0.3048006096012192 +no_defs",
    "WY: Wyoming West": "+proj=tmerc +lat_0=40.5 +lon_0=-110.083333333333 +k=0.9999375 +x_0=800000.0000 +y_0=100000.0000 +ellps=GRS80 +datum=NAD83 +to_meter=0.3048006096012192 +no_defs",
}


def select_zone():
    """Display a numbered list of zones and let the user pick one."""
    zone_names = sorted(ZONES.keys())

    print("\n" + "=" * 60)
    print("  NAD83 State Plane Zone Selection")
    print("=" * 60)

    # Print zones in two columns for readability
    col_width = 40
    for i, name in enumerate(zone_names, start=1):
        print(f"  {i:>3}. {name:<{col_width}}", end="")
        if i % 2 == 0:
            print()
    if len(zone_names) % 2 != 0:
        print()

    print("=" * 60)

    while True:
        try:
            choice = int(input(f"\nEnter zone number (1–{len(zone_names)}): ").strip())
            if 1 <= choice <= len(zone_names):
                selected = zone_names[choice - 1]
                print(f"\n✔  Selected: {selected}\n")
                return selected
            else:
                print(f"  Please enter a number between 1 and {len(zone_names)}.")
        except ValueError:
            print("  Invalid input — please enter a number.")


def export_survey_data(filename, zone_name):
    """Convert CSV survey data to KML using the chosen State Plane zone."""
    try:
        if not os.path.exists(filename):
            print(f"Error: Could not find '{filename}' in this folder.")
            return

        proj_string = ZONES[zone_name]
        transformer = Transformer.from_crs(
            CRS.from_proj4(proj_string), "EPSG:4326", always_xy=True
        )

        column_names = ["point_name", "northing", "easting", "elevation", "description"]
        df = pd.read_csv(filename, header=None, names=column_names, encoding="latin1")
        print(f"Successfully loaded {len(df)} survey points.")

        lon, lat = transformer.transform(df["easting"].values, df["northing"].values)
        df["latitude"] = lat
        df["longitude"] = lon

        kml = simplekml.Kml()
        for _, row in df.iterrows():
            pnt = kml.newpoint(name=str(row["point_name"]))
            pnt.coords = [(row["longitude"], row["latitude"], row["elevation"])]
            pnt.description = f"Desc: {row['description']}\nElev: {row['elevation']}"
            # TODO: Add custom icon style here if desired
            # pnt.style.iconstyle.icon.href = "https://your-icon-url.png"

        kml.save("Survey_Points.kml")
        df.to_csv("Plotted_Data.csv", index=False)

        print("\n--- Success! ---")
        print(f"Zone used : {zone_name}")
        print(f"Files saved to: {os.getcwd()}")

    except Exception as e:
        print(f"Error: {e}")


# =============================================================================
# Main
# =============================================================================
if __name__ == "__main__":
    csv_file = r"csv.csv"          # ← change this to your CSV filename if needed

    zone = select_zone()
    export_survey_data(csv_file, zone)
