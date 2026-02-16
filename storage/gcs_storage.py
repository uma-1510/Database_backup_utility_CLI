import os
from google.cloud import storage
from core.interfaces import StorageInterface


class GCSStorage(StorageInterface):

    def __init__(self, config, logger):
        self.config = config
        self.logger = logger

    def upload(self, file_path, bucket_name):
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = \
            self.config['gcs']['service_account_key']

        client = storage.Client()
        bucket = client.bucket(bucket_name)
        blob = bucket.blob(file_path.name)
        blob.upload_from_filename(str(file_path))

        self.logger.info("Uploaded to GCS")
