from abc import ABC, abstractmethod
from pathlib import Path


class DatabaseInterface(ABC):
    
    def __init__(self, db_path: str):
        self.db_path = db_path

    @abstractmethod
    def backup(self, output_file):
        pass

    @abstractmethod
    def restore(self, backup_file):
        pass


class CompressionInterface(ABC):

    @abstractmethod
    def compress(self, backup_file: Path, output_file: Path):
        pass


class StorageInterface(ABC):

    @abstractmethod
    def upload(self, file_path: Path, bucket_name: str):
        pass


class NotificationInterface(ABC):

    @abstractmethod
    def send(self, message: str):
        pass


