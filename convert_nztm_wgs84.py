import pandas as pd
from pyproj import CRS, Transformer
import json
 
input_file = "Consent.geojson"
output_file = f"Consent_.wgs84_crs.geojson"

nztm_crs = CRS("EPSG:2193")
wgs84_crs = CRS("EPSG:4326")
 
transformer = Transformer.from_crs(nztm_crs, wgs84_crs, always_xy=True)


def csv_convert_to_wgs84(input_file, output_file):
    df = pd.read_csv(input_file)

    # Create a new column using iterrows()
    for index, row in df.iterrows():
    
        longitude, latitude = transformer.transform(row['X'] , row['Y'])
    
        df.loc[index, 'longitude'] = longitude
        df.loc[index, 'latitude'] =  latitude
    
    
    df.head()
    df.to_csv(output_file)


    
def json_convert_to_wgs84(input_file, output_file):
    with open(input_file, 'r') as file:
        data = json.load(file)
 
    for item in data["features"]:
        print(item)
        longitude, latitude = transformer.transform(item["properties"]['X'] , item["properties"]['Y'])
        print(longitude, latitude)
        item["properties"]["longitude"]=longitude
        item["properties"]["latitude"]=latitude
 
    with open(output_file, 'w') as f:
        json.dump(data,f, indent=4)

