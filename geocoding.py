import pandas as pd
import requests
import geopandas as gpd

def readMe():
    print("READ FIRST! PLEASE MAKE SURE YOU ALREADY HAVE HERE MAP API'S KEY FOR GEOCODING")
    print("\n If you haven't got the API KEY, then go through https://developer.here.com/tutorials/getting-here-credentials/ first.")
    print("Thank You!")
    
def start():
    path_status = False
    addressIsTrue = False
    address_list = []
    
    readMe()
    
    while path_status == False:
        try:
            file_path = input("Enter your file path: \n") #taking user input
            file = pd.read_csv(file_path)
            path_status = True
        except:
            print("Your File Path is Not Found. Please Re-Check Your Input")
    
    if path_status == True:
        df = pd.DataFrame(file)
        print("\n This is your data frame columns name: \n")
        for i in df.columns :
            print(i)
            
    while addressIsTrue == False:
        address_attributes = input("\n Enter your address attributes: \n")
        addressIsTrue = check_address(file,address_attributes)
    
    print("\n DataFrame: \n",df.head())
    
    for i in range(0,len(df[address_attributes])-1):
        address_list.append(df[address_attributes][i])
    
    loc_df = start_geo_coding(df,address_list)
    final_df = pd.concat([df,loc_df], axis=1).reindex(df.index)
    
    #String Maniupation for File Path
    fp = file_path.replace('.',' ')
    
    # Export File to CSV,SHP and JPEG
    final_df.to_csv(f"{fp} _ geocode results .csv")
    export_geojson(final_df,fp)
    
    print("\n",final_df.head())
    print("\n Thank you! Please check my github at: github.com/nooglersoon")

def start_geo_coding(df,address):
    longitudes=[]
    latitudes=[]
    api_key = input("\n Enter your Here API Key: ") #taking user apikey
    bound = input("\n Enter your Specific Boundaries (Country/Region/City/Village): ") #taking user apikey
    
    for loc in address:
        try:
            long,lat=start_network(df,loc, api_key,bound)
            longitudes.append(long)
            latitudes.append(lat)
        except:
            print("\n The location at {} is not located or re-check your address".format(loc))
    loc_df = pd.DataFrame(list(zip(longitudes,latitudes)), columns =['Longitudes','Latitudes'])
    print("\n This is your geocoding results from your address: \n")
    print(loc_df.head())
    return loc_df
        

def check_address(df,att):
    if att in df.columns :
        return True
    else :
        print("\n There is no column with that input \n")
        return False
    

def start_network(df,loc, api_key,bound):
    # Setting up the network
    URL = "https://geocode.search.hereapi.com/v1/geocode"
    # sending get request and saving the response as response object
    PARAMS = {'apikey':api_key,'q':loc+f' {bound}'}
    r = requests.get(url = URL, params = PARAMS)
    data = r.json()
    long,lat = retrieve_data(loc,data)
    return long,lat
    

def retrieve_data (loc,data):
    #sub = data['items'][0]['address']['city']
    #print(data)
    latitude = data['items'][0]['position']['lat']
    longitude = data['items'][0]['position']['lng']
    print("\n Your location is at {} with the latitude is: {} and the longitude is: {}".format(loc,latitude, longitude))
    return latitude,longitude

def export_geojson(df,name):
    gdf = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df.Latitudes, df.Longitudes))
    gdf.crs = 'epsg:4326'
    gdf.to_file(f"{name}.geojson", driver="GeoJSON")
