from pymongo import MongoClient
import certifi

# Your DocumentDB endpoint
db_endpoint = 'your-documentdb-cluster-endpoint:27017'

# Your database name
db_name = 'your_database_name'

# Credentials
username = 'your_username'
password = 'your_password'

# Connection string
connection_string = f"mongodb://{username}:{password}@{db_endpoint}/?ssl=true&replicaSet=rs0&readpreference=secondaryPreferred&retryWrites=false"

# Connect to your DocumentDB cluster
client = MongoClient(connection_string, tlsCAFile=certifi.where())

# Specify the database to use
db = client[db_name]

# Now you can interact with your database
# For example, listing the collections
print(db.list_collection_names())
