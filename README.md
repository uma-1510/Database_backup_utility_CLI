# Database Backup Utility CLI

A **production-oriented** database backup and restore CLI built with **Clean Architecture**, supporting **PostgreSQL, MySQL, SQLite, and MongoDB** — with checksum validation, gzip compression, structured logging, metrics collection, notification hooks, and cloud storage integration.

---

## Why This Exists

Most backup scripts are tightly coupled to a single database. Adding a new DB engine means rewriting core logic. This project solves that by treating each database as a pluggable **adapter** — the orchestration, validation, and storage layers never know (or care) which database they're talking to.

---

## Architecture

```
Database_backup_utility_CLI/
├── core/                   # Abstract interfaces — BackupEngine, RestoreEngine
├── adapters/databases/     # Concrete DB adapters: PostgreSQL, MySQL, SQLite, MongoDB
├── orchestration/          # Coordinates backup/restore flow end-to-end
├── storage/                # Storage backends (local, cloud)
├── utils/                  # Checksum validation, compression (gzip)
├── logging_config/         # Structured JSON logging
├── metrics/                # Operation metrics & timing
├── notifications/          # Alert hooks (on success/failure)
├── config/                 # Config schema & loader
├── config.json             # User-defined runtime configuration
├── main.py                 # CLI entrypoint
├── DockerFile              # Containerized execution
└── requirements.txt
```

### Design Principles

| Principle | How it's applied |
|---|---|
| **Clean Architecture** | Core logic has zero dependency on any specific database or storage backend |
| **Adapter Pattern** | Each DB engine implements a shared interface — swap or add databases without touching orchestration |
| **Configuration-Driven** | All runtime behaviour (DB targets, storage paths, retention, compression) defined in `config.json` |
| **Fault Isolation** | Backup, validation, and restore are separate pipeline stages — a failure in one doesn't corrupt the others |

---

## Features

- **Multi-database support** — PostgreSQL, MySQL, SQLite, MongoDB
- **Checksum validation** — SHA-256 integrity checks on every backup file; restore is blocked if checksums don't match
- **Compression** — gzip compression applied automatically to reduce backup size
- **Cloud storage integration** — push backups to remote/cloud storage backends
- **Structured logging** — JSON-formatted logs with operation context for observability
- **Metrics collection** — tracks backup duration, file size, success/failure rates
- **Notifications** — configurable alerts on backup success or failure
- **Dockerized** — run the CLI in an isolated container with no local DB dependencies

---

## Quick Start

### 1. Clone & install dependencies

```bash
git clone https://github.com/uma-1510/Database_backup_utility_CLI.git
cd Database_backup_utility_CLI
pip install -r requirements.txt
```

### 2. Configure your target database

Edit `config.json`:

```json
{
  "database": {
    "type": "postgresql",
    "host": "localhost",
    "port": 5432,
    "name": "mydb",
    "user": "admin",
    "password": "secret"
  },
  "storage": {
    "local_path": "./backups",
    "cloud_enabled": false
  },
  "compression": true,
  "notifications": {
    "enabled": true,
    "on_failure": true
  }
}
```

### 3. Run a backup

```bash
python main.py backup
```

### 4. Restore from a backup

```bash
python main.py restore --file backups/mydb_2026-02-21.sql.gz
```

Restore will automatically **verify the checksum** before writing anything to the database.

---

## Run with Docker

```bash
docker build -t db-backup-cli .
docker run --env-file .env db-backup-cli backup
```

---

## How Checksum Validation Works

Every backup operation:
1. Dumps the database to a compressed `.sql.gz` file
2. Computes a **SHA-256 hash** of the file and stores it alongside the backup
3. On restore, recomputes the hash and compares — **restore is aborted** if there's a mismatch

This prevents silent data corruption from partial writes, network errors, or storage failures.

---

## Adding a New Database Engine

Because of the Adapter pattern, adding a new database requires only one thing — implementing the `DatabaseAdapter` interface in `adapters/databases/`:

```python
class MyNewDBAdapter(DatabaseAdapter):
    def backup(self, config: BackupConfig) -> BackupResult:
        ...
    def restore(self, config: RestoreConfig) -> RestoreResult:
        ...
```

No changes needed in `orchestration/`, `storage/`, `utils/`, or `main.py`.

---

## Tech Stack

| Layer | Technology |
|---|---|
| Language | Python 3.11+ |
| Databases | PostgreSQL, MySQL, SQLite, MongoDB |
| Compression | gzip |
| Checksum | hashlib (SHA-256) |
| Logging | Python `logging` + structured JSON formatter |
| Storage | Local filesystem + cloud backend |
| Containerization | Docker |
| Config | JSON |

---

## Project Status

Actively developed. Core backup/restore pipeline, checksum validation, compression, and multi-DB support are complete. Cloud storage and notification integrations are configurable.

---

## Author

**Uma Maheswari Chinnam**  
M.S. Computer Science, Clark University  
[LinkedIn](https://www.linkedin.com/in/uma-maheswari-ab030320b/)
