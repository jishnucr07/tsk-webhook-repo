# from flask_pymongo import PyMongo

# Setup MongoDB here

from pymongo import MongoClient

client = MongoClient("mongodb://mongo_container:27017/")
db = client["webhook_db"]
collection = db["events"]
