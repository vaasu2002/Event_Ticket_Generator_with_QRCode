import os
import pymongo
from pymongo.errors import ConnectionFailure

DATABASE_NAME = 'QREventBooking'
COLLECTION_NAME = 'Test1'
MONGODB_URL = "mongodb+srv://vaasu:pcvaasu9dps@cluster0.wydi0u7.mongodb.net/13digital?retryWrites=true&w=majority"

def connectToDatabase()->pymongo.collection.Collection:
    try:
    
        client = pymongo.MongoClient(MONGODB_URL)
        collection = None

        if COLLECTION_NAME in client[DATABASE_NAME].list_collection_names():
                collection = client[DATABASE_NAME][COLLECTION_NAME]        
            
        else:
            print("Collection does not exist")
            return None

        if collection is not None:
            collection.create_index('registration_number', unique=True)
            return collection
        
    except:
        print("Failed to connect to database")