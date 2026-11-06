"""
Logging system for CCTV Viewer.
"""

import logging
import os
from logging.handlers import RotatingFileHandler


class CCTVLogger:
    def __init__(self, log_level=logging.INFO, log_to_file=False,
                 log_file="logs/cctv_viewer.log", max_size_mb=10):
        self.logger = logging.getLogger("CCTV_Viewer")
        self.logger.setLevel(log_level)
        self.logger.handlers.clear()

        # Console
        console = logging.StreamHandler()
        console.setFormatter(logging.Formatter(
            '%(asctime)s [%(levelname)s] %(message)s', datefmt='%H:%M:%S'))
        self.logger.addHandler(console)

        # File with rotation
        if log_to_file:
            try:
                os.makedirs(os.path.dirname(log_file), exist_ok=True)
                file_handler = RotatingFileHandler(
                    log_file,
                    maxBytes=max_size_mb * 1024 * 1024,
                    backupCount=5,
                    encoding="utf-8")
                file_handler.setFormatter(logging.Formatter(
                    '%(asctime)s [%(levelname)s] %(name)s - %(message)s'))
                self.logger.addHandler(file_handler)
            except Exception as e:
                self.logger.error(f"Failed to create log file: {e}")

    def debug(self, msg):
        self.logger.debug(msg)

    def info(self, msg):
        self.logger.info(msg)

    def warning(self, msg):
        self.logger.warning(msg)

    def error(self, msg):
        self.logger.error(msg)

    def critical(self, msg):
        self.logger.critical(msg)


_logger = None


def get_logger():
    global _logger
    if _logger is None:
        _logger = CCTVLogger()
    return _logger


def init_logger(log_level=logging.INFO, log_to_file=False,
                log_file="logs/cctv_viewer.log", max_size_mb=10):
    global _logger
    _logger = CCTVLogger(log_level, log_to_file, log_file, max_size_mb)
    return _logger
