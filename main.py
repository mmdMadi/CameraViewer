#!/usr/bin/env python3
"""
Multi-Camera CCTV Viewer Application
A modern GUI application for viewing multiple camera streams simultaneously
"""

import sys
import os
import logging
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import Qt
from src.main_window import MainWindow
from src.settings_manager import SettingsManager
from src.logger import init_logger

def setup_logging(settings_manager):
    """Initialize logging based on settings"""
    level_map = {
        "Debug": logging.DEBUG,
        "Info": logging.INFO,
        "Warning": logging.WARNING,
        "Error": logging.ERROR,
        "Critical": logging.CRITICAL,
    }
    level_str = settings_manager.settings.value("logging/level", "Info")
    log_level = level_map.get(level_str, logging.INFO)
    log_to_file = settings_manager.settings.value("logging/to_file", False, type=bool)
    log_file = settings_manager.settings.value("logging/file_path", "logs/cctv_viewer.log")
    init_logger(log_level, log_to_file, log_file)

def main():
    # Enable high DPI scaling
    os.environ.setdefault("QT_AUTO_SCREEN_SCALE_FACTOR", "1")

    app = QApplication(sys.argv)
    app.setApplicationName("CCTV Viewer")
    app.setApplicationVersion("2.0.0")
    app.setOrganizationName("CCTV Solutions")

    settings_manager = SettingsManager()
    setup_logging(settings_manager)

    window = MainWindow(settings_manager)
    window.show()

    sys.exit(app.exec())

if __name__ == "__main__":
    main()
