from src.configuration.aws_connection import S3Client
from src.logger import logger
from src.exception import CustomException
import sys
import os

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
    
    def load_model(self, model_name: str, bucket_name: str, model_dir: str = None):

    
        try:
            model_file = model_dir + "/" + model_name if model_dir else model_name
            file_object = self.get_file_object(model_file, bucket_name)
            model_obj = self.read_object(file_object, decode=False)
            model = pickle.loads(model_obj)
            logger.info("Production model loaded from S3 bucket.")
            return model
        except Exception as e:
            raise CustomException(e, sys) from e
        
    @staticmethod
    def read_object(object_name: str, decode: bool = True, make_readable: bool = False):
        try:
            # Read and decode the object content if decode=True
            func = (
                lambda: object_name.get()["Body"].read().decode()
                if decode else object_name.get()["Body"].read()
            )
            # Convert to StringIO if make_readable=True
            conv_func = lambda: StringIO(func()) if make_readable else func()
    
            return conv_func()
        except Exception as e:
            raise CustomException(e, sys) from e
   
   
    def get_file_object(self, filename: str, bucket_name: str):

        logger.info("Entered the get_file_object method of SimpleStorageService class")
        try:
            bucket = self.get_bucket(bucket_name)
            file_objects = [file_object for file_object in bucket.objects.filter(Prefix=filename)]
            func = lambda x: x[0] if len(x) == 1 else x
            file_objs = func(file_objects)
            logger.info("Exited the get_file_object method of SimpleStorageService class")
            return file_objs
        except Exception as e:
            raise CustomException(e, sys) from e

    def create_folder(self, folder_name: str, bucket_name: str) -> None:
        """
        Creates a folder in the specified S3 bucket.

        Args:
            folder_name (str): Name of the folder to create.
            bucket_name (str): Name of the S3 bucket.
        """
        logger.info("Entered the create_folder method of SimpleStorageService class")
        try:
            # Check if folder exists by attempting to load it
            self.s3_resource.Object(bucket_name, folder_name).load()
        except ClientError as e:
            # If folder does not exist, create it
            if e.response["Error"]["Code"] == "404":
                folder_obj = folder_name + "/"
                self.s3_client.put_object(Bucket=bucket_name, Key=folder_obj)
            logger.info("Exited the create_folder method of SimpleStorageService class")

    def upload_file(self, from_filename: str, to_filename: str, bucket_name: str, remove: bool = True):
    
        logger.info("Entered the upload_file method of StorageService class")
        try:
            logger.info(f"Uploading {from_filename} to {to_filename} in {bucket_name}")
            self.s3_resource.meta.client.upload_file(from_filename, bucket_name, to_filename)
            logger.info(f"Uploaded {from_filename} to {to_filename} in {bucket_name}")

            # Delete the local file if remove is True
            if remove:
                os.remove(from_filename)
                logger.info(f"Removed local file {from_filename} after upload")
            logger.info("Exited the upload_file method of SimpleStorageService class")
        except Exception as e:
            raise CustomException(e, sys) from e

    def upload_df_as_csv(self, data_frame: DataFrame, local_filename: str, bucket_filename: str, bucket_name: str) -> None:
        """
        Uploads a DataFrame as a CSV file to the specified S3 bucket.

        Args:
            data_frame (DataFrame): DataFrame to be uploaded.
            local_filename (str): Temporary local filename for the DataFrame.
            bucket_filename (str): Target filename in the bucket.
            bucket_name (str): Name of the S3 bucket.
        """
        logger.info("Entered the upload_df_as_csv method of SimpleStorageService class")
        try:
            # Save DataFrame to CSV locally and then upload it
            data_frame.to_csv(local_filename, index=None, header=True)
            self.upload_file(local_filename, bucket_filename, bucket_name)
            logger.info("Exited the upload_df_as_csv method of SimpleStorageService class")
        except Exception as e:
            raise CustomException(e, sys) from e

    def get_df_from_object(self, object_: object) -> DataFrame:
        """
        Converts an S3 object to a DataFrame.

        Args:
            object_ (object): The S3 object.

        Returns:
            DataFrame: DataFrame created from the object content.
        """
        logger.info("Entered the get_df_from_object method of SimpleStorageService class")
        try:
            content = self.read_object(object_, make_readable=True)
            df = read_csv(content, na_values="na")
            logger.info("Exited the get_df_from_object method of SimpleStorageService class")
            return df
        except Exception as e:
            raise CustomException(e, sys) from e

    def read_csv(self, filename: str, bucket_name: str) -> DataFrame:

        logger.info("Entered the read_csv method of SimpleStorageService class")
        try:
            csv_obj = self.get_file_object(filename, bucket_name)
            df = self.get_df_from_object(csv_obj)
            logger.info("Exited the read_csv method of SimpleStorageService class")
            return df
        except Exception as e:
            raise CustomException(e, sys) from e