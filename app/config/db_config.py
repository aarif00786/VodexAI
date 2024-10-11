from pymongo import MongoClient, UpdateMany, UpdateOne
from app.env import MONGO_URL

conn = MongoClient(MONGO_URL
                   )
db = conn['vodexai']

collection_names = db.list_collection_names()
