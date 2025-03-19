import os 
from dotenv import load_dotenv
import pandas as pd

#=============================================================================================
# Get Connection string
#=============================================================================================
def get_MySQL_instance():
    schema = "metropolis"
    host = "127.0.0.1"
    user = "root"
    password = os.getenv("mysql_password")
    port = 3306
    
    connection_string = f'mysql+pymysql://{user}:{password}@{host}:{port}/{schema}'

    return connection_string
#=============================================================================================
# Get MySQL instance
#=============================================================================================
def from_MySQL(connection_string, query):
    return pd.read_sql(sql = query, con=connection_string)
#=============================================================================================
# Send a Pandas DataFrame to MySQL
#=============================================================================================
def to_MySQL(df, connection_string, table):
    df.to_sql(table, if_exists = 'append', con = connection_string, index = False)
    return f'DataFrame sent to the MySQL table "{table}"!'