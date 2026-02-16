import boto3
from core.interfaces import StorageInterface


class S3Storage(StorageInterface):

    def __init__(self, config, logger):
        self.config = config
        self.logger = logger

    def upload(self, file_path, bucket_name):
        session = boto3.Session(
            aws_access_key_id=self.config['aws']['access_key'],
            aws_secret_access_key=self.config['aws']['secret_key'],
            region_name=self.config['aws']['region']
        )
        s3 = session.client('s3')
        s3.upload_file(str(file_path), bucket_name, file_path.name)
        self.logger.info("Uploaded to S3")
