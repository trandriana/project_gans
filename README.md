# Project GANS

The objective of the project is to create a data pipeline locally. It involves collecting data from external sources:
- web scraping on Wikipedia
- Data Collection via APIs

In parallel, we transforming the data collected, and store it in a SQL database.

To run the codes, have your MySQL password and APIs keys ready. Store them in 'secret_keys.env' as follows:

        - API_key = OpenWeatherMap API key
        - mysql_password = MySQL password
        - RapidAPI_Key = RapidAPI key
