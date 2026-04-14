from pymongo import MongoClient
from pymongo.server_api import ServerApi
import certifi

uri = "mongodb+srv://reachnam119_db_user:nana3132@cluster0.c5kg3xj.mongodb.net/?appName=Cluster0"

client = MongoClient(
    uri,
    server_api=ServerApi('1'),
    tlsCAFile=certifi.where()
)

try:
    client.admin.command('ping')
    print("✅ Connected to MongoDB!")
except Exception as e:
    print("❌ Error:", e)
    #58.97.229.52/32
'''from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

def get_mongo_client():
    uri = os.getenv("MONGO_DB_URL")

    if not uri:
        raise Exception("MONGO_DB_URL is missing in .env")

    client = MongoClient(
        uri,
        tls=True,
        serverSelectionTimeoutMS=5000
    )

    return client'''