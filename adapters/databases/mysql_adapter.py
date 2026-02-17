import subprocess
from pathlib import Path
from core.interfaces import DatabaseInterface


class MySQLAdapter(DatabaseInterface):

    def __init__(self, config: dict):
        self.host = config["host"]
        self.port = config["port"]
        self.user = config["user"]
        self.password = config["password"]
        self.database = config["database"]

    def backup(self, output_file: Path):

        command = [
            "mysqldump",
            "-h", self.host,
            "-P", str(self.port),
            "-u", self.user,
            self.database
        ]

        env = None
        if self.password:
            import os
            env = os.environ.copy()
            env["MYSQL_PWD"] = self.password   # ✅ safer than -p

        with open(output_file, "w") as f:
            subprocess.run(command, stdout=f, check=True, env=env)

        return output_file

    def restore(self, backup_file: Path):

        command = [
            "mysql",
            "-h", self.host,
            "-P", str(self.port),
            "-u", self.user,
            self.database
        ]

        import os
        env = os.environ.copy()
        env["MYSQL_PWD"] = self.password

        with open(backup_file, "r") as f:
            subprocess.run(command, stdin=f, check=True, env=env)
