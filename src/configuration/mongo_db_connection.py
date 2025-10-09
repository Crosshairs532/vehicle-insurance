import os
import sys
import pymongo
import certifi

from src.exception import CustomException
from src.logger import logging
from src.constants import DATABASE_NAME, MONGODB_URL_KEY


class MongoDBClient:

    client = None

    def __init__(self, database_name: str = DATABASE_NAME) -> None:
        try:
            if MongoDBClient.client is None:
                mongo_db_url = MONGODB_URL_KEY
                if mongo_db_url is None:
                    raise Exception(f"Environment variable '{MONGODB_URL_KEY}' is not set.")

                # Establish a new MongoDB client connection
                MongoDBClient.client = pymongo.MongoClient(mongo_db_url)

            # Use the shared MongoClient for this instance
            self.client = MongoDBClient.client
            self.database = self.client[database_name]  # Connect to the specified database
            self.database_name = database_name
            logging.info("MongoDB connection successful.")

        except Exception as e:
            # Raise a custom exception with traceback details if connection fails
            raise CustomException(e, sys)