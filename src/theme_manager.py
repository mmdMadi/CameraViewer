from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QObject

class ThemeManager(QObject):
    def __init__(self, main_window, settings_manager):
        super().__init__()
        self.main_window = main_window
        self.settings_manager = settings_manager
        
    def apply_theme(self):
        """Apply the current theme"""
        theme = self.settings_manager.get_theme()
        
        if theme == "dark":
            self.apply_dark_theme()
        else:
            self.apply_light_theme()
            
    def apply_light_theme(self):
        """Apply light theme"""
        light_style = """
        QMainWindow {
            background-color: #f0f0f0;
            color: #333333;
        }
        
        QMenuBar {
            background-color: #ffffff;
            color: #333333;
            border-bottom: 1px solid #cccccc;
        }
        
        QMenuBar::item {
            background-color: transparent;
            padding: 4px 8px;
        }
        
        QMenuBar::item:selected {
            background-color: #e0e0e0;
        }
        
        QMenu {
            background-color: #ffffff;
            color: #333333;
            border: 1px solid #cccccc;
        }
        
        QMenu::item:selected {
            background-color: #e0e0e0;
        }
        
        QToolBar {
            background-color: #f8f8f8;
            border: 1px solid #cccccc;
            spacing: 3px;
        }
        
        QStatusBar {
            background-color: #f8f8f8;
            color: #333333;
            border-top: 1px solid #cccccc;
        }
        
        QWidget {
            background-color: #ffffff;
            color: #333333;
        }
        
        QPushButton {
            background-color: #e0e0e0;
            border: 1px solid #cccccc;
            padding: 5px 10px;
            border-radius: 3px;
        }
        
        QPushButton:hover {
            background-color: #d0d0d0;
        }
        
        QPushButton:pressed {
            background-color: #c0c0c0;
        }
        
        QLineEdit {
            background-color: #ffffff;
            border: 1px solid #cccccc;
            padding: 5px;
            border-radius: 3px;
        }
        
        QComboBox {
            background-color: #ffffff;
            border: 1px solid #cccccc;
            padding: 5px;
            border-radius: 3px;
        }
        
        QSpinBox {
            background-color: #ffffff;
            border: 1px solid #cccccc;
            padding: 5px;
            border-radius: 3px;
        }
        
        QCheckBox {
            spacing: 5px;
        }
        
        QGroupBox {
            font-weight: bold;
            border: 2px solid #cccccc;
            border-radius: 5px;
            margin-top: 1ex;
            padding-top: 10px;
        }
        
        QGroupBox::title {
            subcontrol-origin: margin;
            left: 10px;
            padding: 0 5px 0 5px;
        }
        """
        
        QApplication.instance().setStyleSheet(light_style)
        
    def apply_dark_theme(self):
        """Apply dark theme"""
        dark_style = """
        QMainWindow {
            background-color: #2b2b2b;
            color: #ffffff;
        }
        
        QMenuBar {
            background-color: #3c3c3c;
            color: #ffffff;
            border-bottom: 1px solid #555555;
        }
        
        QMenuBar::item {
            background-color: transparent;
            padding: 4px 8px;
        }
        
        QMenuBar::item:selected {
            background-color: #555555;
        }
        
        QMenu {
            background-color: #3c3c3c;
            color: #ffffff;
            border: 1px solid #555555;
        }
        
        QMenu::item:selected {
            background-color: #555555;
        }
        
        QToolBar {
            background-color: #3c3c3c;
            border: 1px solid #555555;
            spacing: 3px;
        }
        
        QStatusBar {
            background-color: #3c3c3c;
            color: #ffffff;
            border-top: 1px solid #555555;
        }
        
        QWidget {
            background-color: #2b2b2b;
            color: #ffffff;
        }
        
        QPushButton {
            background-color: #4a4a4a;
            border: 1px solid #666666;
            padding: 5px 10px;
            border-radius: 3px;
            color: #ffffff;
        }
        
        QPushButton:hover {
            background-color: #5a5a5a;
        }
        
        QPushButton:pressed {
            background-color: #6a6a6a;
        }
        
        QLineEdit {
            background-color: #3c3c3c;
            border: 1px solid #666666;
            padding: 5px;
            border-radius: 3px;
            color: #ffffff;
        }
        
        QComboBox {
            background-color: #3c3c3c;
            border: 1px solid #666666;
            padding: 5px;
            border-radius: 3px;
            color: #ffffff;
        }
        
        QComboBox::drop-down {
            border: none;
        }
        
        QComboBox::down-arrow {
            image: none;
            border-left: 5px solid transparent;
            border-right: 5px solid transparent;
            border-top: 5px solid #ffffff;
        }
        
        QSpinBox {
            background-color: #3c3c3c;
            border: 1px solid #666666;
            padding: 5px;
            border-radius: 3px;
            color: #ffffff;
        }
        
        QCheckBox {
            spacing: 5px;
            color: #ffffff;
        }
        
        QCheckBox::indicator {
            width: 13px;
            height: 13px;
        }
        
        QCheckBox::indicator:unchecked {
            background-color: #3c3c3c;
            border: 1px solid #666666;
        }
        
        QCheckBox::indicator:checked {
            background-color: #0078d4;
            border: 1px solid #0078d4;
        }
        
        QGroupBox {
            font-weight: bold;
            border: 2px solid #666666;
            border-radius: 5px;
            margin-top: 1ex;
            padding-top: 10px;
            color: #ffffff;
        }
        
        QGroupBox::title {
            subcontrol-origin: margin;
            left: 10px;
            padding: 0 5px 0 5px;
        }
        
        QDialog {
            background-color: #2b2b2b;
            color: #ffffff;
        }
        
        QLabel {
            color: #ffffff;
        }
        """
        
        QApplication.instance().setStyleSheet(dark_style)