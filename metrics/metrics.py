from prometheus_client import Counter, start_http_server


class Metrics:

    def __init__(self, port=8000):
        self.backup_counter = Counter(
            "backup_total",
            "Total number of backups"
        )
        start_http_server(port)

    def increment_backup_counter(self):
        self.backup_counter.inc()
