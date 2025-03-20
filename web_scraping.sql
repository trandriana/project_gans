/***************************
Setting up the environment
***************************/
DROP DATABASE IF EXISTS metropolis;
CREATE DATABASE metropolis;
USE metropolis;

/***************************
Creating the table 'city'
***************************/
CREATE TABLE City (
    CityId INT AUTO_INCREMENT,
    CityName VARCHAR(45) NOT NULL,
    PRIMARY KEY (CityId)
);

SELECT *
FROM City;

/***************************
Creating the table 'country'
***************************/
CREATE TABLE country (
    CountryName VARCHAR(45) NOT NULL,
    CityId INT,
    FOREIGN KEY (CityId) REFERENCES City (CityId) 
);

SELECT *
FROM country;

/***************************
Creating the table 'geolocation'
***************************/
CREATE TABLE geolocation (
    Latitude FLOAT NOT NULL,
    Longitude FLOAT NOT NULL,
    CityId INT,
    FOREIGN KEY (CityId) REFERENCES City (CityId) 
);

SELECT *
FROM geolocation;

/***************************
Creating the table 'population'
***************************/
CREATE TABLE population (
    YearDataRetrieved YEAR NOT NULL,
    Population INT NOT NULL,
    CityId INT NOT NULL,
    FOREIGN KEY (CityId) REFERENCES City (CityId) 
);

SELECt *
FROM population;

/***************************
Creating the table 'weather'
***************************/
CREATE TABLE weather (
	WeatherId INT AUTO_INCREMENT,
    CityId INT,
    CityName VARCHAR(45) NOT NULL,
    ForecastTime DATETIME NOT NULL,
    Temperature FLOAT NOT NULL,
    WeatherCondition VARCHAR(45) NOT NULL,
    RainVolume FLOAT NOT NULL,
    ProbOfRain FLOAT NOT NULL,
    DateOfRetrieval DATETIME,
    PRIMARY KEY (WeatherId),
    FOREIGN KEY (CityId) REFERENCES City (CityId) 
);

SELECT *
FROM weather;

/***************************
Creating the table 'NearbyAirport'
***************************/
CREATE TABLE NearbyAirport (
IATA VARCHAR(3) NOT NULL,
CityId INT NOT NULL,
PRIMARY KEY (IATA),
FOREIGN KEY (CityId) REFERENCES City (CityId)
);

SELECT *
FROM NearbyAirport;

/***************************
Creating the table 'NearbyAirport'
***************************/
CREATE TABLE FlightArrivals (
IATA VARCHAR (3),
ScheduledTime DATETIME,
DateOfRetrieval DATETIME,
FOREIGN KEY (IATA) REFERENCES NearbyAirport (IATA)
);

SELECT *
FROM FlightArrivals;