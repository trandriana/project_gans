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



SELECT *
FROM city
LEFT JOIN country USING(CityID)
LEFT JOIN geolocation USING(CityID)
LEFT JOIN population USING(CityID);