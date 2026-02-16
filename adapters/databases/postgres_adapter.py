import subprocess
from pathlib import Path
from core.interfaces import DatabaseInterface


class PostgresAdapter(DatabaseInterface):
    def __init__(self, config: dict):
        self.host = config["postgresql"]["host"]
        self.port = config["postgresql"]["port"]
        self.user = config["postgresql"]["user"]
        self.password = config["postgresql"]["password"]
        self.database = config["postgresql"]["database"]

    def backup(self, db_name, config, output_file: Path):
        command = [
            "pg_dump",
            "-h", self.post,
            "-p", str(self.port),
            "-U", self.user,
            "-F", "c",
            "-b",
            "-v",
            "-f", str(output_file),
            self.database
        ]
        subprocess.run(command, check=True)
        return output_file

    def restore(self, backup_file: Path, config):
        command = [
            "pg_restore",
            "-U", config['user'],
            "-d", config['database'],
            "-v",
            str(backup_file)
        ]
        subprocess.run(command, check=True)
