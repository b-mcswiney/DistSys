"""
Connects to SQL database using pyodbc and creates the table needed for simulation data
"""

import pyodbc

SERVER = "tcp:distsys.database.windows.net,14433"
DATABASE = "coursework 2"
USERNAME = "ed20b3mdistsys"
PASSWORD = "distsysed20b3m123."

connectionString = "Driver={ODBC Driver 18 for SQL Server};Server=tcp:distsys.database.windows.net,1433;Database=coursework 2;Uid=ed20b3mdistsys;Pwd=distsysed20b3m123.;Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;"

conn = pyodbc.connect(connectionString)

# Create sim_data table
CREATE_TABLE = """
CREATE TABLE sim_data (
    sensor_id CHAR(8) NOT NULL PRIMARY KEY,
    Temperature INT NOT NULL,
    wind_speed INT NOT NULL,
    humidity INT NOT NULL,
    co2 INT NOT NULL);
"""
conn.commit()
# # execute sql statement
cursor = conn.cursor()
cursor.execute(CREATE_TABLE)

INIT_TABLE = """
INSERT INTO sim_data
VALUES (1, 12, 20, 45, 750)
"""
cursor.execute(INIT_TABLE)

conn.commit()

cursor.close()
conn.close()
