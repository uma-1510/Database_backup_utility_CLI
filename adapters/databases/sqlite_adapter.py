import sqlite3
from pathlib import Path
from core.interfaces import DatabaseInterface


class SQLiteAdapter(DatabaseInterface):
    def __init__(self, config):
        self.db_path = config.get("path")
        if not self.db_path:
            raise ValueError("SQLite config requires 'path'")

    def backup(self, output_file: Path):
        conn = sqlite3.connect(self.db_path)
        with open(output_file, "w") as f:
            for line in conn.iterdump():
                f.write(f"{line}\n")
        conn.close()
        return output_file

    def restore(self, backup_file: Path, config):
        conn = sqlite3.connect(config['database']['sqlite'])
        with open(backup_file, "r") as f:
            conn.executescript(f.read())
        conn.commit()
        conn.close()
