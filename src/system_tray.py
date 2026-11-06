from PySide6.QtWidgets import QSystemTrayIcon, QMenu, QApplication
from PySide6.QtCore import QObject, Signal, Qt
from PySide6.QtGui import QIcon, QPixmap, QPainter, QAction
import os

class SystemTrayManager(QObject):
    show_window = Signal()
    quit_application = Signal()
    
    def __init__(self, main_window, settings_manager):
        super().__init__()
        self.main_window = main_window
        self.settings_manager = settings_manager
        self.tray_icon = None
        
        # Check if system tray is available
        if not QSystemTrayIcon.isSystemTrayAvailable():
            print("System tray is not available on this system")
            return
            
        self.setup_tray_icon()
        self.setup_tray_menu()
        
    def setup_tray_icon(self):
        """Setup system tray icon"""
        # Create a simple icon if no icon file exists
        icon = self.create_default_icon()
        
        self.tray_icon = QSystemTrayIcon(icon, self.main_window)
        self.tray_icon.setToolTip("CCTV Multi-Camera Viewer")
        
        # Connect signals
        self.tray_icon.activated.connect(self.on_tray_icon_activated)
        self.show_window.connect(self.main_window.show)
        self.show_window.connect(self.main_window.raise_)
        self.show_window.connect(self.main_window.activateWindow)
        self.quit_application.connect(QApplication.instance().quit)
        
    def create_default_icon(self):
        """Create a default icon for the system tray"""
        # Create a simple 16x16 icon
        pixmap = QPixmap(16, 16)
        pixmap.fill(Qt.GlobalColor.white)
        
        painter = QPainter(pixmap)
        painter.setPen(Qt.GlobalColor.black)
        painter.setBrush(Qt.GlobalColor.black)
        
        # Draw a simple camera icon
        painter.fillRect(2, 4, 12, 8, Qt.GlobalColor.black)
        painter.fillRect(4, 6, 8, 4, Qt.GlobalColor.white)
        painter.fillRect(6, 7, 4, 2, Qt.GlobalColor.black)
        
        # Draw lens
        painter.drawEllipse(7, 7, 2, 2)
        
        painter.end()
        
        return QIcon(pixmap)
        
    def setup_tray_menu(self):
        """Setup system tray context menu"""
        if not self.tray_icon:
            return
            
        menu = QMenu()
        
        # Show/Hide window
        show_action = QAction("Show Window", self)
        show_action.triggered.connect(self.show_window.emit)
        menu.addAction(show_action)
        
        menu.addSeparator()
        
        # Camera controls
        start_all_action = QAction("Start All Cameras", self)
        start_all_action.triggered.connect(self.main_window.start_all_cameras)
        menu.addAction(start_all_action)
        
        stop_all_action = QAction("Stop All Cameras", self)
        stop_all_action.triggered.connect(self.main_window.stop_all_cameras)
        menu.addAction(stop_all_action)
        
        menu.addSeparator()
        
        # Recording controls
        record_all_action = QAction("Record All", self)
        record_all_action.triggered.connect(self.main_window.record_all_cameras)
        menu.addAction(record_all_action)
        
        stop_record_action = QAction("Stop All Recording", self)
        stop_record_action.triggered.connect(self.main_window.stop_all_recording)
        menu.addAction(stop_record_action)
        
        menu.addSeparator()
        
        # Settings
        settings_action = QAction("Settings", self)
        settings_action.triggered.connect(self.main_window.show_settings)
        menu.addAction(settings_action)
        
        menu.addSeparator()
        
        # Quit
        quit_action = QAction("Quit", self)
        quit_action.triggered.connect(self.quit_application.emit)
        menu.addAction(quit_action)
        
        self.tray_icon.setContextMenu(menu)
        
    def on_tray_icon_activated(self, reason):
        """Handle tray icon activation"""
        if reason == QSystemTrayIcon.ActivationReason.DoubleClick:
            if self.main_window.isVisible():
                self.main_window.hide()
            else:
                self.show_window.emit()
                
    def show_tray_icon(self):
        """Show the system tray icon"""
        if self.tray_icon:
            self.tray_icon.show()
            
    def hide_tray_icon(self):
        """Hide the system tray icon"""
        if self.tray_icon:
            self.tray_icon.hide()
            
    def is_available(self):
        """Check if system tray is available"""
        return self.tray_icon is not None
        
    def show_message(self, title, message, icon=QSystemTrayIcon.MessageIcon.Information, timeout=3000):
        """Show a system tray notification"""
        if self.tray_icon and self.tray_icon.isVisible():
            self.tray_icon.showMessage(title, message, icon, timeout)