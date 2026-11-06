#!/usr/bin/env python3
"""
Test script to open just the settings dialog
"""

import sys
from PySide6.QtWidgets import QApplication
from src.settings_manager import SettingsManager
from src.settings_dialog import SettingsDialog

def main():
    app = QApplication(sys.argv)
    
    # Initialize settings
    settings_manager = SettingsManager()
    
    # Create and show settings dialog
    dialog = SettingsDialog(settings_manager)
    dialog.show()
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()