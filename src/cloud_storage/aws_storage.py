from src.configuration.aws_connection import S3Client
from src.logger import logger
from src.exception import CustomException
import sys

class StorageService:

    def __init__(self):
        """
            Initialize S3 client and resource 
        """
        s3_client = S3Client()
        self.s3_resource = s3_client.s3_resource
        self.s3_client = s3_client.s3_client

    def s3_key_path_available(self, bucket_name, s3_key):
        try:
            bucket = self.get_bucket(bucket_name)
            file_objects = [file_object for file_object in bucket.objects.filter(Prefix=s3_key)]
            return len(file_objects) > 0
        except Exception as e:
            logger.info(f"Something went wrong in checking s3 key path: {e}")
            raise CustomException(e, sys)
    
    def get_bucket(self, bucket_name):
        
        try:
            logger.info("<<< Getting bucket >>>")
            bucket = self.s3_resource.Bucket(bucket_name)
            logger.info(f"Bucket {bucket_name} found")
            return bucket
        except Exception as e:
            logger.info(f"Something went wrong in getting bucket: {e}")
            raise CustomException(e, sys)