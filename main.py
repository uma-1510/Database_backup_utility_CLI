from core.backup_service import BackupService
from adapters.databases.mysql_adapter import MySQLAdapter
from adapters.databases.sqlite_adapter import SQLiteAdapter
from adapters.databases.postgres_adapter import PostgresAdapter
from adapters.databases.mongodb_adapter import MongoDBAdapter
from storage.s3_storage import S3Storage
from storage.azure_storage import AzureStorage
from storage.gcs_storage import GCSStorage
from notifications.slack_notifier import SlackNotifier
from config.settings import load_config
from logging_config.logger import setup_logger


def main():
    parser = build_parser()
    args = parser.parse_args()

    # print(args)

    config = load_config(args.config)
    logger = setup_logger(args.log_file)


    # Select DB adapter dynamically
    if args.db_type == "sqlite":
        db_adapter = SQLiteAdapter(args.output)
    elif args.db_type == "mysql":
        db_adapter = MySQLAdapter(config["database"]["mysql"])
    elif args.db_type == "postgresql":
        db_adapter = PostgresAdapter(config["database"]["postgresql"])
    elif args.db_type == "mongodb":
        db_adapter = MongoDBAdapter(config["database"]["mongodb"])
    else:
        raise ValueError("Unsupported DB type")

    # Optional storage
    storage_adapter = None
    if args.cloud == "s3":
        storage_adapter = S3Storage(config, logger)
    elif args.cloud == "azure":
        storage_adapter = AzureStorage(config, logger)
    elif args.cloud == "gcs":
        storage_adapter = GCSStorage(config, logger)

    # Optional notifier
    slack_webhook = config.get("slack_webhook")
    notifier = SlackNotifier(slack_webhook, logger) if slack_webhook else None

    service = BackupService(db_adapter, storage_adapter, notifier, logger)
    service.execute(args)


def build_parser():
    import argparse
    parser = argparse.ArgumentParser(description="Database Backup CLI Tool")
    
    # Main arguments
    parser.add_argument('operation', choices=['backup', 'restore'], help="Operation to perform: backup or restore")
    
    # Database connection args
    parser.add_argument('--db-type', required=True,choices=["mysql", "postgresql", "mongodb", "sqlite"], help="Database type (mysql, postgresql, mongodb, sqlite)")
    parser.add_argument('--config', required=True, help="Path to JSON configuration file for database connection")
    
    # Backup args
    parser.add_argument('--output', help="Output backup file path")
    parser.add_argument('--compress', action='store_true', help="Compress the backup")
    
    # Restore args
    parser.add_argument('--backup-file', help="Backup file to restore")
    
    # Storage args
    parser.add_argument('--cloud', choices=['s3', 'gcs', 'azure'], help="Cloud storage option")
    parser.add_argument('--bucket', help="Cloud storage bucket name")
    
    # Log file argument
    parser.add_argument('--log-file', help="Path to the log file", default='backup.log')
    
    
    return parser


if __name__=='__main__':
    main()
