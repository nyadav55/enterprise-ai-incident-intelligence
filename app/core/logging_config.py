

import logging
import os
from logging.handlers import RotatingFileHandler
from pathlib import Path

# Store logs in the project root/logs directory.
LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)

# Read log level from environment; default to INFO.
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()

# Define a common log format.
LOG_FORMAT = (
    "%(asctime)s | %(levelname)s | "
    "%(name)s | %(message)s"
)

# Rotate logs when the file reaches 5 MB.
file_handler = RotatingFileHandler(
    LOG_DIR / "eaiirp.log",
    maxBytes=5 * 1024 * 1024,
    backupCount=3,
    encoding="utf-8",
)

# Also display logs in the terminal.
console_handler = logging.StreamHandler()

# Apply the same format to both handlers.
formatter = logging.Formatter(LOG_FORMAT)
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

# Configure the root application logger.
logging.basicConfig(
    level=getattr(logging, LOG_LEVEL, logging.INFO),
    handlers=[file_handler, console_handler],
)
