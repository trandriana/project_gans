import os 
import pandas as pd
import requests

#=============================================================================================
# Get airports nearby the cities
#=============================================================================================
def get_NearbyAirports(city_df):
    # API headers
    headers = {
        "X-RapidAPI-Key": os.getenv("RapidAPI_Key"),
        "X-RapidAPI-Host": "aerodatabox.p.rapidapi.com"
    }
    
    # Construct the URL with the latitude and longitude
    url = "https://aerodatabox.p.rapidapi.com/airports/search/location"

    # DataFrame to store results
    all_airports = []

    # for lat, lon in zip(latitudes, longitudes):
    for _, city in city_df.iterrows():
        lat, lon, CityId = city["Latitude"], city["Longitude"], city["CityId"] 
        
        # querystring = {"withFlightInfoOnly": "true"}
        querystring = {"lat":lat,"lon":lon,"radiusKm":"50","limit":"5","withFlightInfoOnly":"True"}
    
        # Make the API request
        response = requests.get(url, headers=headers, params=querystring)
    
        if response.status_code == 200:
            data = response.json()
            for item in data['items']:
                airport ={'IATA': item['iata'],'CityId': CityId}
                all_airports.append(airport)
        
    NearbyAirport_df = pd.DataFrame(all_airports)
    return NearbyAirport_df
#=============================================================================================
# Get the Flights arrivals time for each airport
#=============================================================================================
def get_FlightArrivals(Airports):
    one_day = pd.to_timedelta(1, unit = 'day')
    today = pd.to_datetime('today')
    tomorrow = today + one_day
    date_of_today, date_of_tomorrow = today.strftime('%Y-%m-%d'), tomorrow.strftime('%Y-%m-%d')
    
    FlightArrivals_items = []
    for _,Airport in Airports.iterrows():
        iata = Airport['IATA']
        url = f"https://aerodatabox.p.rapidapi.com/flights/airports/iata/{iata}/{date_of_tomorrow}T06:00/{date_of_tomorrow}T18:00"
        
        querystring = {"withLeg":"false","direction":"Arrival","withCancelled":"false","withCodeshared":"false","withCargo":"false","withPrivate":"false","withLocation":"false"}

        api_key = "687292277emsh6620811a3972b04p1a4ee9jsn8c02f9bc139b"
        headers = {
            "x-rapidapi-key": os.getenv("RapidAPI_Key"),
        	"x-rapidapi-host": "aerodatabox.p.rapidapi.com"
        }

        response = requests.get(url, headers=headers, params=querystring)
        print(f'IATA = {iata}, response status_code = {response.status_code}')
        if response.status_code == 200:
            FlightArrivals_json = response.json()

            for item in FlightArrivals_json['arrivals']:
                FlightArrivals_item = {
                    'IATA' : iata,
                    'ScheduledTime' : pd.to_datetime(item['movement']['scheduledTime']['local']),
                    'DateOfRetrieval': pd.to_datetime(date_of_today)
                }
                FlightArrivals_items.append(FlightArrivals_item)
        
    FlightArrivals_df = pd.DataFrame(FlightArrivals_items)
    
    return FlightArrivals_df