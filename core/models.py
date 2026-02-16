from dataclasses import dataclass
from pathlib import Path


@dataclass
class BackupRequest:
    db_type: str
    db_name: str
    output_file: Path
    compress: bool
    cloud_provider: str | None = None
    bucket_name: str | None = None
