# from flask_pymongo import PyMongo

# Setup MongoDB here
# mongo = PyMongo(uri="mongodb://localhost:27017/database")
from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client["webhook_db"]
collection = db["events"]
