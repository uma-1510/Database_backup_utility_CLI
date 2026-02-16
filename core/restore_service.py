class RestoreService:

    def __init__(self, db_adapter, notifier, logger):
        self.db_adapter = db_adapter
        self.notifier = notifier
        self.logger = logger

    def execute(self, backup_file, config):
        self.db_adapter.restore(backup_file, config)
        self.notifier.send(f"Restore completed: {backup_file}")
