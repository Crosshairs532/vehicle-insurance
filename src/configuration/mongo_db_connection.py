import os
import sys
import pymongo
import certifi

from src.exception import CustomException
from src.logger import get_logger
from src.constants import DATABASE_NAME, MONGODB_URL_KEY


logger =  get_logger("MongoDBClient")

class MongoDBClient:

    client = None

    def __init__(self, database_name: str = DATABASE_NAME) -> None:
        try:
            if MongoDBClient.client is None:
                mongo_db_url = MONGODB_URL_KEY
                if mongo_db_url is None:
                    raise CustomException(f"Environment variable '{MONGODB_URL_KEY}' is not set.", sys)
                MongoDBClient.client = pymongo.MongoClient(mongo_db_url)


            self.client = MongoDBClient.client
            self.database = self.client[database_name]  
            self.database_name = database_name
            logger.info("MongoDB connection successful.")

        except Exception as e:

            raise CustomException(e, sys)