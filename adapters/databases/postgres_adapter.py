import os
import subprocess
from pathlib import Path
from core.interfaces import DatabaseInterface


class PostgresAdapter(DatabaseInterface):

    def __init__(self, config: dict):
        # validate config
        required = ["host", "port", "user", "password", "database"]
        for key in required:
            if key not in config:
                raise ValueError(f"Missing postgres config field: {key}")

        self.host = config["host"]
        self.port = config["port"]
        self.user = config["user"]
        self.password = config["password"]
        self.database = config["database"]

    def backup(self, output_file: Path):

        env = os.environ.copy()
        env["PGPASSWORD"] = self.password

        command = [
            "pg_dump",
            "-h", self.host,
            "-p", str(self.port),
            "-U", self.user,
            "-F", "c",
            "-b",
            "-v",
            "-f", str(output_file),
            self.database
        ]

        subprocess.run(command, check=True, env=env)
        return output_file

    def restore(self, backup_file: Path):

        env = os.environ.copy()
        env["PGPASSWORD"] = self.password

        command = [
            "pg_restore",
            "-h", self.host,
            "-p", str(self.port),
            "-U", self.user,
            "-d", self.database,
            "-v",
            str(backup_file)
        ]

        subprocess.run(command, check=True, env=env)
