import pandas as pd
import re
import requests
from bs4 import BeautifulSoup
from lat_lon_parser  import parse
import os
from pytz import timezone
from datetime import datetime

# ===================================================================================================================
# collect
# ===================================================================================================================
def city_info(new_cities):
    '''
    Description: This function uses the function scraping to extracts information of a list of cities. The information are collected from its wikipedia page. 
    We collect information such as the coordinates, the country, the population (with year of data retrieved) 'https://openweathermap.org/api'.
    We fix also appropriate datatypes for the columns 'Population', 'YearDataRetrieved, 'Latitude', and 'Longitude' 
    Author: Tsiry Avisoa Randrianasolo
    Syntax: [CityName, latitude, longitude, country, year, pop] = collect(CityName)
    Input: 
        -- CityName: A series of city name
    Output:
        -- CityName: The name of the city
        -- latitude, longitude: the coordinate of the city
        -- country: the country it belongs to
        -- date: the year the data about the population was retrieved
        -- pop: population of the city 
    '''

    scraping_city_df = pd.DataFrame(columns = ['CityName', 'Latitude', 'Longitude', 'CountryName', 'YearDataRetrieved', 'Population'])
    
    scraping_city_df['CityName'] = new_cities

    # scraping the info on wikipedia
    scraping_city_df[:] = list(scraping_city_df['CityName'].apply(scraping))

    # Fix the datatypes
    scraping_city_df['Population'] = pd.to_numeric(scraping_city_df['Population'], downcast = 'unsigned')
    scraping_city_df['YearDataRetrieved'] = pd.to_numeric(scraping_city_df['YearDataRetrieved'], downcast = 'unsigned')
    scraping_city_df['Latitude'] = pd.to_numeric(scraping_city_df['Latitude'])
    scraping_city_df['Longitude'] = pd.to_numeric(scraping_city_df['Longitude'])
    
    return scraping_city_df
# ===================================================================================================================
# scraping
# ===================================================================================================================
def scraping(CityName):
    '''
    Description: This function extracts information of the city. The information are collected from its wikipedia page. 
    We collect information such as the coordinates, the country, the population (with year of data retrieved) 'https://openweathermap.org/api'
    Author: Tsiry Avisoa Randrianasolo
    Syntax: [CityName, latitude, longitude, country, year, pop] = scraping(CityName)
    Input: 
        -- CityName: The name of the city 
    Output:
        -- CityName: The name of the city
        -- latitude, longitude: the coordinate of the city
        -- country: the country it belongs to
        -- date: the year the data about the population was retrieved
        -- pop: population of the city 
    '''
    url = f'https://en.wikipedia.org/wiki/{CityName}'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Extract the latitude and longitude coordinates of the city
    latitude, longitude = soup.find_all(class_ = 'latitude')[0].get_text(), soup.find_all(class_ = 'longitude')[0].get_text()
    latitude, longitude = parse(latitude), parse(longitude)

    # Extract the number of populations
    pop = soup.find(string = 'Population').find_next('td').get_text()
    pop = pop.replace(',', '')
    match = re.search(r'^\d+', pop)
    pop = int(match.group())

    # Extract the date of retrieval of the number of populations
    date = soup.find(string = 'Population').find_next().get_text()
    date = date.strip()
    match = re.search(r'\d{4}', date)
    date = int(match.group())

    # Extract the country the city belongs to
    country = soup.find_all(class_ = 'infobox-label', string = 'Country')[0].find_next('td').get_text()
    country = country.strip().replace('_', ' ')

    CityName = CityName.strip().replace('_', ' ')

    return CityName, latitude, longitude, country, date, pop
# ===================================================================================================================
# weather_forcast
# ===================================================================================================================
def weather_forcast(city_df):
    '''
    Description: This function extracts 5 Day / 3 Hour weather forcast from the Weather API 'https://openweathermap.org/api'
    Author: Tsiry Avisoa Randrianasolo
    Syntax: weather_df = weather_forcast(city_df)
    Input: 
        -- city_df: a Pandas DataFrame with the names of city, CityId, and their respective latitude and longitude in decimale format 
    Output:
        -- weather_df: a pandas DataFrame containing a list of weather parameters 
        ['CityId', 'CityName', 'ForecastTime', 'Temperature', 'WeatherCondition', 'RainVolume', 'ProbOfRain', 'DateOfRetrieval']
                CityId: 
                CityName: 
                ForecastTime:
                Temperature: Temperature in Celcius
                WeatherCondition: Group of weather parameters (Rain, Snow, Clouds etc.)
                RainVolume: Rain volume for last 3 hours, mm
                ProbOfRain: Probability of rain
                DateOfRetrieval
    '''
    # Get access to the Weather API 
    API_key = os.getenv("api_key")  
    berlin_timezone = timezone('Europe/Berlin')
    weather_items = []
    
    for _, city in city_df.iterrows():
        lat, lon, CityId, CityName = city["Latitude"], city["Longitude"], city["CityId"], city["CityName"]
    
        weather = requests.get(f"https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={API_key}&units=metric")
        weather_json = weather.json()
 
        CityName = weather_json['city'].get('name')
        DateOfRetrieval = datetime.now(berlin_timezone).strftime("%Y-%m-%d %H:%M:%S")
    
        for item in weather_json["list"]:
            weather_item = {
                # Added the city name, so the information is clear when looking at multiple cities
                'CityId': CityId,
                'CityName': CityName,
                'ForecastTime': item.get("dt_txt", None),
                'Temperature': item["main"].get("temp", None),
                'WeatherCondition': item["weather"][0].get("main", None),
                'RainVolume': item.get("rain", {}).get("3h", 0),
                'ProbOfRain': item['pop'],
                'DateOfRetrieval': DateOfRetrieval
            }
            weather_items.append(weather_item)

    # Creating the DataFrame
    weather_df = pd.DataFrame(data = weather_items)
    
    return weather_df