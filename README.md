



"""


pip install snowflake-connector-python

import snowflake.connector

--# Snowflake connection parameters
account = 'your_account_url'
warehouse = 'your_warehouse'
database = 'your_database'
schema = 'your_schema'
username = 'your_username'
password = 'your_password'

--# Create a connection object
conn = snowflake.connector.connect(
    user=username,
    password=password,
    account=account,
    warehouse=warehouse,
    database=database,
    schema=schema
)

--# Create a cursor object
cur = conn.cursor()

--# Execute a sample query
cur.execute("SELECT CURRENT_DATE()")

--# Fetch the result
result = cur.fetchone()
print("Current date from Snowflake:", result[0])

--# Close the cursor and connection
cur.close()
conn.close()


"""
