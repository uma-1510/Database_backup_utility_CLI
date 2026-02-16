import subprocess
from core.interfaces import DatabaseInterface


class MySQLAdapter(DatabaseInterface):

    def backup(self, db_name, config, output_file):
        command = [
            "mysqldump",
            "-u", config['user'],
            f"-p{config['password']}",
            db_name
        ]

        with open(output_file, 'w') as f:
            subprocess.run(command, stdout=f, check=True)
        
        print(f"Backing up from {db_name} to {output_file}")

        return output_file

    def restore(self, backup_file, config):
        command = [
            "mysql",
            "-u", config['user'],
            f"-p{config['password']}",
            config['database']
        ]

        with open(backup_file, 'r') as f:
            subprocess.run(command, stdin=f, check=True)
