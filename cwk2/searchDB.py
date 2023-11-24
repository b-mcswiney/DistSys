"""
Connects to SQL database using pyodbc and gets all sim data
"""

import pyodbc

SERVER = "tcp:distsys.database.windows.net,14433"
DATABASE = "coursework 2"
USERNAME = "ed20b3mdistsys"
PASSWORD = "distsysed20b3m123."

connectionString = "Driver={ODBC Driver 18 for SQL Server};Server=tcp:distsys.database.windows.net,1433;Database=coursework 2;Uid=ed20b3mdistsys;Pwd=distsysed20b3m123.;Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;"

conn = pyodbc.connect(connectionString)

SEARCH_TABLE = """
SELECT sensor_id, Temperature, wind_speed, humidity, co2
FROM sim_data
"""

cursor=conn.cursor()
cursor.execute(SEARCH_TABLE)

records = cursor.fetchall()
for r in records:
    print(f"{r.sensor_id}\t{r.Temperature}\t{r.wind_speed}\t{r.humidity}\t{r.co2}")
