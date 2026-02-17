from core.interfaces import DatabaseInterface, StorageInterface, NotificationInterface
from core.integrity_service import IntegrityService
from core.compression_service import CompressionService

class BackupService:

    def __init__(self, db_adapter: DatabaseInterface,
                 storage_adapter: StorageInterface | None,
                 notifier: NotificationInterface,
                 logger):
        self.db_adapter = db_adapter
        self.storage_adapter = storage_adapter
        self.notifier = notifier
        self.logger = logger

    def execute(self, request):
        if request.operation == "backup":
            self.logger.info("Starting backup process")
            backup_file = self.db_adapter.backup(request.output)

            if request.compress:
                self.logger.info("Compression enabled")
                compressed_file = CompressionService.compress(backup_file)
                backup_file.unlink()   # delete raw dump
                backup_file = compressed_file
                self.logger.info(f"Compressed file: {backup_file}")

            checksum = IntegrityService.generate_checksum(backup_file)
            self.logger.info(f"Checksum generated: {checksum}")
            if self.storage_adapter and request.bucket:
                self.storage_adapter.upload(backup_file, request.bucket)
            # self.notifier.send(f"Backup successful: {backup_file}")
            return backup_file

        elif request.operation == "restore":
            self.logger.info("Starting restore process")

            restore_file = request.backup_file

            if restore_file.endswith(".gz"):
                self.logger.info("Decompressing backup before restore")
                restore_file = CompressionService.decompress(restore_file)

            self.db_adapter.restore(restore_file)
            # self.notifier.send(f"Restore successful: {request.backup_file}")
            return request.backup_file

