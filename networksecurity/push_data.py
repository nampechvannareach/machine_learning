import certifi
from pymongo import MongoClient
from pymongo.server_api import ServerApi
import sys
import os
import pandas as pd
import pymongo

from networksecurity.exception import NetworkSecurityException
from networksecurity.logger import logging

# 🔐 Your MongoDB URI
MONGO_DB_URL = "mongodb+srv://reachnam119_db_user:nana3132@cluster0.c5kg3xj.mongodb.net/?appName=Cluster0"

# SSL certificate
ca = certifi.where()


class NetworkDataExtract:
    def __init__(self):
        try:
            # ✅ Proper MongoDB client with TLS + Server API
            self.mongo_client = MongoClient(
                MONGO_DB_URL,
                server_api=ServerApi('1'),
                tlsCAFile=ca
            )

            # ✅ Test connection
            self.mongo_client.admin.command('ping')
            print("✅ Connected to MongoDB!")

        except Exception as e:
            raise NetworkSecurityException(e, sys)

    # ✅ FIXED FUNCTION
    def csv_to_json_convertor(self, file_path):
        try:
            data = pd.read_csv(file_path)

            # reset index
            data.reset_index(drop=True, inplace=True)

            # ✅ BEST WAY (NO json.load issue)
            records = data.to_dict(orient="records")

            print(f"✅ CSV Loaded: {data.shape}")
            print(f"✅ Total Records: {len(records)}")

            return records

        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def insert_data_mongodb(self, records, database, collection):
        try:
            db = self.mongo_client[database]
            collection = db[collection]

            # ✅ Optional: clear old data (IMPORTANT for retraining)
            collection.delete_many({})

            # ✅ Insert new data
            result = collection.insert_many(records)

            print(f"✅ Inserted {len(result.inserted_ids)} records")

            return len(result.inserted_ids)

        except Exception as e:
            raise NetworkSecurityException(e, sys)


if __name__ == "__main__":
    try:
        FILE_PATH = r"Network_Data\phisingData.csv"
        DATABASE = "KRISHAI"
        COLLECTION = "NetworkData"

        networkobj = NetworkDataExtract()

        # Step 1: Load CSV
        records = networkobj.csv_to_json_convertor(file_path=FILE_PATH)

        # Step 2: Insert into MongoDB
        no_of_records = networkobj.insert_data_mongodb(
            records, DATABASE, COLLECTION
        )

        print(f"✅ Total inserted records: {no_of_records}")

    except Exception as e:
        raise NetworkSecurityException(e, sys)