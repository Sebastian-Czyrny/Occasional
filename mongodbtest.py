"""
NOTE: need to create secret.py file in local directory.
Add two variables to secret.py: 
    userdb (your database username)
    passworddb (your database password)
This script tests if you can connect to the database.
"""

import secret

from pymongo.mongo_client import MongoClient

uri = f"mongodb+srv://{secret.MONGO_USERNAME}:{secret.MONGO_PASSWORD}@cluster0.9dnqbir.mongodb.net/?retryWrites=true&w=majority"

print(uri)
# Create a new client and connect to the server

client = MongoClient(uri)

# Send a ping to confirm a successful connection

try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

