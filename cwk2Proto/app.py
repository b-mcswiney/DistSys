"""
Connects to SQL database using pyodbc
"""

import pyodbc

SERVER = "tcp:distsys.database.windows.net,14433"
DATABASE = "coursework 2"
USERNAME = "ed20b3mdistsys"
PASSWORD = "distsysed20b3m123."

connectionString = "Driver={ODBC Driver 18 for SQL Server};Server=tcp:distsys.database.windows.net,1433;Database=coursework 2;Uid=ed20b3mdistsys;Pwd=distsysed20b3m123.;Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;"

conn = pyodbc.connect(connectionString)

SQL_QUERY = """
SELECT 
TOP 5 c.CustomerID, 
c.CompanyName, 
COUNT(soh.SalesOrderID) AS OrderCount 
FROM 
SalesLT.Customer AS c 
LEFT OUTER JOIN SalesLT.SalesOrderHeader AS soh ON c.CustomerID = soh.CustomerID 
GROUP BY 
c.CustomerID, 
c.CompanyName 
ORDER BY 
OrderCount DESC;
"""

cursor = conn.cursor()
cursor.execute(SQL_QUERY)
records = cursor.fetchall()

for r in records:
    print(r)

