import requests
import geopandas as gpd
from shapely.geometry import shape

#lists = [0,1,2]
#lists = [520,613,535,631,442,446,445,444,451,453,454,456,457,461,462,466,470,401,398,402,418,389,563,564,565,566,567,569,338,498,351,492,500,355,506,361,369,376]
geojson_list = []

for ls in range(1,1000):
    URL = f"https://angkot.web.id/route/transportation/{ls}.json"
    r = requests.get(url = URL)
    try:
        data = r.json()
        json_data = data['geojson']
        geojson_list.append(json_data)
    except ValueError:
        print(ls)
        print("Data not Found")
    
for d in geojson_list:
    d['geometry'] = shape(d['geometry'])
    d['City'] = d['properties']['city']
    d['Company'] = d['properties']['company']
    d['Destination'] = d['properties']['destination']
    d['Origin'] = d['properties']['origin']
    
gdf = gpd.GeoDataFrame(geojson_list).set_geometry('geometry')
gdf.head()
gdf.to_file('Transportasi_Publik_Darat_Indonesia.geojson', driver="GeoJSON")
