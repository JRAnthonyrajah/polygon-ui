"""Enhanced structured logging for PolyBook debugging and monitoring."""

import logging
import json
from datetime import datetime
from typing import Dict, Any, Optional
from pathlib import Path

from PySide6.QtCore import QStandardPaths


class PolyBookLogger:
    """
    Structured logging system for PolyBook with file rotation and console output.
    """

    def __init__(self, log_level: str = "INFO", log_dir: Optional[Path] = None):
        self.log_dir = (
            log_dir
            or Path(QStandardPaths.writableLocation(QStandardPaths.AppDataLocation))
            / "logs"
        )
        self.log_dir.mkdir(parents=True, exist_ok=True)

        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(StructuredFormatter())

        # File handler with rotation
        log_file = self.log_dir / f"polybook_{datetime.now().strftime('%Y%m%d')}.log"
        file_handler = logging.handlers.RotatingFileHandler(
            log_file, maxBytes=10 * 1024 * 1024, backupCount=5  # 10MB, 5 backups
        )
        file_handler.setFormatter(StructuredFormatter())

        self.logger = logging.getLogger("PolyBook")
        self.logger.setLevel(getattr(logging, log_level.upper()))
        self.logger.addHandler(console_handler)
        self.logger.addHandler(file_handler)

    def log_event(
        self,
        level: str,
        event: str,
        details: Dict[str, Any] = None,
        error: Optional[Exception] = None,
    ):
        """
        Log structured event.

        Args:
            level (str): Log level (INFO, WARNING, ERROR).
            event (str): Event name.
            details (Dict): Additional context.
            error (Exception, optional): Error details.
        """
        timestamp = datetime.now().isoformat()
        record = {
            "timestamp": timestamp,
            "level": level,
            "event": event,
            "details": details or {},
        }
        if error:
            record["error"] = str(error)
            record["traceback"] = self._get_traceback(error)

        self.logger.log(getattr(logging, level.upper()), json.dumps(record))

    def _get_traceback(self, error: Exception) -> str:
        """Get error traceback."""
        import traceback

        return traceback.format_exc()

    def error(self, event: str, error: Exception, details: Dict[str, Any] = None):
        self.log_event("ERROR", event, details, error)

    def warning(self, event: str, details: Dict[str, Any] = None):
        self.log_event("WARNING", event, details)

    def info(self, event: str, details: Dict[str, Any] = None):
        self.log_event("INFO", event, details)


class StructuredFormatter(logging.Formatter):
    """JSON formatter for structured logs."""

    def format(self, record):
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "level": record.levelname,
            "message": record.getMessage(),
            "module": record.module,
            "funcName": record.funcName,
            "lineno": record.lineno,
        }
        if hasattr(record, "details"):
            log_entry["details"] = record.details
        return json.dumps(log_entry)


# Global instance
logger = None


def get_logger() -> PolyBookLogger:
    global logger
    if logger is None:
        logger = PolyBookLogger()
    return logger
