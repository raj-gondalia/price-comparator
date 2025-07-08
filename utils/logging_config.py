import logging
import sys
from logging.handlers import RotatingFileHandler
from pathlib import Path

from config import settings


class LoggingConfig:
    @staticmethod
    def setup_logging():
        log_dir = Path("logs")
        log_dir.mkdir(exist_ok=True)

        log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        formatter = logging.Formatter(log_format)

        handlers = []
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(formatter)
        console_handler.setLevel(logging.INFO)
        handlers.append(console_handler)

        file_handler = RotatingFileHandler(
            log_dir / settings.log_file,
            maxBytes=10 * 1024 * 1024,  # 10MB
            backupCount=5,
        )
        file_handler.setFormatter(formatter)
        file_handler.setLevel(logging.DEBUG)
        handlers.append(file_handler)

        error_handler = RotatingFileHandler(
            log_dir / "error.log", maxBytes=10 * 1024 * 1024, backupCount=5  # 10MB
        )
        error_handler.setFormatter(formatter)
        error_handler.setLevel(logging.ERROR)
        handlers.append(error_handler)

        logging.basicConfig(
            level=getattr(logging, settings.log_level.upper()),
            format=log_format,
            handlers=handlers,
        )

        return logging.getLogger(__name__)

    @staticmethod
    def get_logger(name: str = None) -> logging.Logger:
        return logging.getLogger(name or __name__)


LoggingConfig.setup_logging()
