from azure.storage.blob import BlobServiceClient
from core.interfaces import StorageInterface


class AzureStorage(StorageInterface):

    def __init__(self, config, logger):
        self.config = config
        self.logger = logger

    def upload(self, file_path, bucket_name):
        connection_string = self.config['azure']['connection_string']

        blob_service_client = BlobServiceClient.from_connection_string(
            connection_string
        )

        blob_client = blob_service_client.get_blob_client(
            container=bucket_name,
            blob=file_path.name
        )

        with open(file_path, "rb") as data:
            blob_client.upload_blob(data, overwrite=True)

        self.logger.info("Uploaded to Azure Blob Storage")
