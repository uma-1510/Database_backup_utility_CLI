import subprocess
from pathlib import Path
from core.interfaces import DatabaseInterface


class MongoDBAdapter(DatabaseInterface):

    def backup(self, db_name, config, output_file: Path):
        command = [
            "mongodump",
            "--db", db_name,
            "--out", str(output_file)
        ]
        subprocess.run(command, check=True)
        return output_file

    def restore(self, backup_file: Path, config):
        command = [
            "mongorestore",
            "--db", config['database'],
            str(backup_file)
        ]
        subprocess.run(command, check=True)
