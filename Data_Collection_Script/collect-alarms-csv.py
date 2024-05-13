import pandas as pd
import cx_Oracle  # Assuming you're using Oracle Database

# Input to insert connection details
username = input("Please insert DB Username: ")
password = input("Please insert DB Password: ")
hostname = input("Please insert DB Hostname or IP Address: ")
port = input("Please insert DB Connection Port #: ")
service_name = input("Please inform the Service Name: ")

# Set up your Oracle connection
dsn = cx_Oracle.makedsn(hostname, port, service_name)
connection = cx_Oracle.connect(username, password, dsn)

# Define your SQL query
sql_query = """
SELECT
  REPLACE(TO_CHAR(DATE '1970-01-01' + (1 / 24 / 60 / 60) * TROUBLE_CREATE_DATE, 'DD-MON-YYYY HH24:MI:SS'), '"', '""') AS TROUBLE_CREATE_DATE,
  REPLACE(TO_CHAR(DATE '1970-01-01' + (1 / 24 / 60 / 60) * CLOSED_DATE, 'DD-MON-YYYY HH24:MI:SS'), '"', '""') AS CLOSED_DATE,
  ELEMENT_ID,
  OWNER_GROUP,
  TROUBLE_ID,
  TROUBLE_SEVERITY,
  REPLACE(REPLACE(TROUBLE_STATUS, CHR(10), ' '), '"', '""') AS TROUBLE_STATUS,
  REPLACE(REPLACE(DESCRIPTION, CHR(10), ' '), '"', '""') AS DESCRIPTION,
  REPLACE(REPLACE(SUMMARY, CHR(10), ' '), '"', '""') AS SUMMARY
FROM ARADMIN.NTM_NETWORKTROUBLEOUTAGE_JOIN
WHERE
  NTM_NETWORKTROUBLEOUTAGE_JOIN.NETWORK = 'NAAS' AND
  NTM_NETWORKTROUBLEOUTAGE_JOIN.OWNER_GROUP = 'NaaS Infrastructure' AND
  DATE '1970-01-01' + (1 / 24 / 60 / 60) * TROUBLE_CREATE_DATE BETWEEN trunc(sysdate, 'YEAR') AND sysdate
"""

# Execute the query and fetch the results into a DataFrame
df = pd.read_sql_query(sql_query, connection)

# Close the database connection
connection.close()

# Save the DataFrame to a CSV file
df.to_csv('output.csv', index=False)
