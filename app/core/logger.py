import logging
from logging.handlers import RotatingFileHandler
import sys

from pythonjsonlogger.json import JsonFormatter


LOG_FILE = 'logs/app.log'


def get_logger(name: str = 'app', level: int = logging.INFO) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(level)

    if not logger.handlers:
        # Console handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_formatter = JsonFormatter(
            fmt='%(asctime)s %(levelname)s %(name)s %(filename)s %(lineno)d %(message)s'
        )
        console_handler.setFormatter(console_formatter)
        logger.addHandler(console_handler)

        # Rotating file handler
        file_handler = RotatingFileHandler(
            LOG_FILE, maxBytes=5 * 1024 * 1024, backupCount=3
        )
        file_handler.setFormatter(console_formatter)
        logger.addHandler(file_handler)

    return logger
