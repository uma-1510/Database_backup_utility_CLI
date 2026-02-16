import logging
import json

class JsonFormatter(logging.Formatter):
    def format(self, record):
        log_record = {
            "timestamp": self.formatTime(record, self.datefmt),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line_no": record.lineno,
        }
        if record.exc_info:
            log_record["exception"] = self.formatException(record.exc_info)
        return json.dumps(log_record)

def setup_logger(log_file="backup.json"):
    logger = logging.getLogger("backup_cli")
    logger.setLevel(logging.INFO)

    json_formatter = JsonFormatter()

    # File handler (JSON logs)
    file_handler = logging.FileHandler(log_file)
    file_handler.setFormatter(json_formatter)

    # Console handler (optional, also JSON)
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(json_formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger
