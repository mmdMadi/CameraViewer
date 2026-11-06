from PySide6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QToolBar,
                               QMessageBox, QStatusBar)
from PySide6.QtCore import Qt, QTimer, QSettings
from PySide6.QtGui import QKeySequence, QAction

from .camera_grid import CameraGrid
from .settings_dialog import SettingsDialog
from .camera_manager import CameraManager
from .theme_manager import ThemeManager
from .system_tray import SystemTrayManager


class MainWindow(QMainWindow):
    def __init__(self, settings_manager):
        super().__init__()
        self.settings_manager = settings_manager
        self.camera_manager = CameraManager()
        self.theme_manager = ThemeManager(self, settings_manager)
        self.system_tray = SystemTrayManager(self, settings_manager)

        self.setWindowTitle("CCTV Multi-Camera Viewer")
        self.setMinimumSize(1200, 800)

        # Window opacity
        opacity = self.settings_manager.settings.value("ui/window_opacity", 100, type=int)
        self.setWindowOpacity(opacity / 100.0)

        self.setup_ui()
        self.setup_menu_bar()
        self.setup_toolbar()
        self.setup_status_bar()

        self.theme_manager.apply_theme()

        if self.system_tray.is_available():
            self.system_tray.show_tray_icon()

        self._restore_geometry()
        self.load_cameras()
        self.apply_startup_settings()

    # ── UI setup ───────────────────────────────────────────
    def setup_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(5, 5, 5, 5)

        self.camera_grid = CameraGrid(self.camera_manager, self)
        layout.addWidget(self.camera_grid)

    def setup_menu_bar(self):
        menubar = self.menuBar()

        # File
        file_menu = menubar.addMenu("&File")

        add_camera_action = QAction("&Add Camera", self)
        add_camera_action.setShortcut(QKeySequence.StandardKey.New)
        add_camera_action.triggered.connect(self.add_camera)
        file_menu.addAction(add_camera_action)

        file_menu.addSeparator()

        exit_action = QAction("E&xit", self)
        exit_action.setShortcut(QKeySequence.StandardKey.Quit)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        # View
        view_menu = menubar.addMenu("&View")

        fullscreen_action = QAction("&Fullscreen", self)
        fullscreen_action.setShortcut(QKeySequence.StandardKey.FullScreen)
        fullscreen_action.triggered.connect(self.toggle_fullscreen)
        view_menu.addAction(fullscreen_action)

        view_menu.addSeparator()

        start_all_action = QAction("Start &All Cameras", self)
        start_all_action.setShortcut(Qt.Key.Key_F5)
        start_all_action.triggered.connect(self.start_all_cameras)
        view_menu.addAction(start_all_action)

        stop_all_action = QAction("&Stop All Cameras", self)
        stop_all_action.setShortcut(Qt.Key.Key_F6)
        stop_all_action.triggered.connect(self.stop_all_cameras)
        view_menu.addAction(stop_all_action)

        view_menu.addSeparator()

        record_all_action = QAction("&Record All", self)
        record_all_action.setShortcut(Qt.Key.Key_F7)
        record_all_action.triggered.connect(self.record_all_cameras)
        view_menu.addAction(record_all_action)

        stop_record_all_action = QAction("Stop All &Recording", self)
        stop_record_all_action.setShortcut(Qt.Key.Key_F8)
        stop_record_all_action.triggered.connect(self.stop_all_recording)
        view_menu.addAction(stop_record_all_action)

        view_menu.addSeparator()

        snapshot_all_action = QAction("Snapshot &All", self)
        snapshot_all_action.setShortcut(Qt.Key.Key_F9)
        snapshot_all_action.triggered.connect(self.snapshot_all_cameras)
        view_menu.addAction(snapshot_all_action)

        # Settings
        settings_menu = menubar.addMenu("&Settings")

        preferences_action = QAction("&Preferences", self)
        preferences_action.setShortcut(QKeySequence.StandardKey.Preferences)
        preferences_action.triggered.connect(self.show_settings)
        settings_menu.addAction(preferences_action)

        # Help
        help_menu = menubar.addMenu("&Help")

        shortcuts_action = QAction("&Keyboard Shortcuts", self)
        shortcuts_action.triggered.connect(self.show_shortcuts)
        help_menu.addAction(shortcuts_action)

        about_action = QAction("&About", self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)

    def setup_toolbar(self):
        toolbar = QToolBar("Main Toolbar")
        self.addToolBar(toolbar)

        add_action = QAction("Add Camera", self)
        add_action.triggered.connect(self.add_camera)
        toolbar.addAction(add_action)

        toolbar.addSeparator()

        self.start_all_action = QAction("Start All", self)
        self.start_all_action.triggered.connect(self.start_all_cameras)
        toolbar.addAction(self.start_all_action)

        self.stop_all_action = QAction("Stop All", self)
        self.stop_all_action.triggered.connect(self.stop_all_cameras)
        toolbar.addAction(self.stop_all_action)

        toolbar.addSeparator()

        self.record_all_action = QAction("Record All", self)
        self.record_all_action.triggered.connect(self.record_all_cameras)
        toolbar.addAction(self.record_all_action)

        self.stop_record_all_action = QAction("Stop All Recording", self)
        self.stop_record_all_action.triggered.connect(self.stop_all_recording)
        toolbar.addAction(self.stop_record_all_action)

        toolbar.addSeparator()

        self.snapshot_all_action = QAction("Snapshot All", self)
        self.snapshot_all_action.triggered.connect(self.snapshot_all_cameras)
        toolbar.addAction(self.snapshot_all_action)

    def setup_status_bar(self):
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Ready")

    # ── Camera operations ──────────────────────────────────
    def add_camera(self):
        from .add_camera_dialog import AddCameraDialog
        dialog = AddCameraDialog(self)
        if dialog.exec():
            camera_info = dialog.get_camera_info()
            self.camera_manager.add_camera(camera_info)
            self.save_cameras()

    def show_settings(self):
        dialog = SettingsDialog(self.settings_manager, self)
        if dialog.exec():
            self.theme_manager.apply_theme()

            opacity = self.settings_manager.settings.value("ui/window_opacity", 100, type=int)
            self.setWindowOpacity(opacity / 100.0)

            toolbar_visible = self.settings_manager.settings.value("ui/show_toolbar", True, type=bool)
            for tb in self.findChildren(QToolBar):
                tb.setVisible(toolbar_visible)

            statusbar_visible = self.settings_manager.settings.value("ui/show_statusbar", True, type=bool)
            self.status_bar.setVisible(statusbar_visible)

            # Grid columns may have changed
            self.camera_grid.refresh_grid()

    def toggle_fullscreen(self):
        if self.isFullScreen():
            self.showNormal()
        else:
            self.showFullScreen()

    def show_shortcuts(self):
        QMessageBox.information(self, "Keyboard Shortcuts",
            "F1 - Add Camera\n"
            "F5 - Start All Cameras\n"
            "F6 - Stop All Cameras\n"
            "F7 - Record All\n"
            "F8 - Stop All Recording\n"
            "F9 - Snapshot All\n"
            "F11 / Esc - Fullscreen\n"
            "Double-click camera - Fullscreen view\n"
            "Right-click camera - Context menu")

    def show_about(self):
        QMessageBox.about(self, "About CCTV Viewer",
            "<h3>CCTV Multi-Camera Viewer</h3>"
            "<p>Version 2.0.0</p>"
            "<p>A modern application for viewing multiple "
            "camera streams simultaneously.</p>"
            "<p>Features: Recording, Snapshots, System Tray, "
            "Multiple themes, Stream optimization.</p>")

    # ── Bulk camera controls ───────────────────────────────
    def start_all_cameras(self):
        count = sum(1 for w in self.camera_manager.camera_widgets.values() if not w.is_streaming)
        self.camera_manager.start_all()
        self.status_bar.showMessage(f"Started {count} cameras")

    def stop_all_cameras(self):
        count = sum(1 for w in self.camera_manager.camera_widgets.values() if w.is_streaming)
        self.camera_manager.stop_all()
        self.status_bar.showMessage(f"Stopped {count} cameras")

    def record_all_cameras(self):
        count = 0
        for widget in self.camera_grid.camera_widgets.values():
            if widget.is_streaming and not widget.recording_manager.is_recording(widget.camera_id):
                widget.toggle_recording()
                count += 1
        self.status_bar.showMessage(f"Started recording {count} cameras")

    def stop_all_recording(self):
        count = 0
        for widget in self.camera_grid.camera_widgets.values():
            if widget.recording_manager.is_recording(widget.camera_id):
                widget.toggle_recording()
                count += 1
        self.status_bar.showMessage(f"Stopped recording {count} cameras")

    def snapshot_all_cameras(self):
        count = 0
        for widget in self.camera_grid.camera_widgets.values():
            if widget.is_streaming and widget.current_frame is not None:
                widget.take_snapshot()
                count += 1
        self.status_bar.showMessage(f"Took snapshots of {count} cameras")

    # ── Persistence ────────────────────────────────────────
    def load_cameras(self):
        cameras = self.settings_manager.get_cameras()
        for camera_info in cameras:
            cam_id = camera_info.pop("id", None)
            self.camera_manager.add_camera(camera_info, camera_id=cam_id)

    def save_cameras(self):
        cameras = self.camera_manager.get_all_cameras()
        self.settings_manager.save_cameras(cameras)

    def _restore_geometry(self):
        if not self.settings_manager.settings.value("startup/restore_layout", True, type=bool):
            return
        geometry = self.settings_manager.get_window_geometry()
        state = self.settings_manager.get_window_state()
        if geometry:
            self.restoreGeometry(geometry)
        if state:
            self.restoreState(state)
        if self.settings_manager.get_window_maximized():
            self.showMaximized()

    def _save_geometry(self):
        self.settings_manager.set_window_geometry(self.saveGeometry())
        self.settings_manager.set_window_state(self.saveState())
        self.settings_manager.set_window_maximized(self.isMaximized())

    def apply_startup_settings(self):
        if self.settings_manager.settings.value("ui/fullscreen_startup", False, type=bool):
            self.showFullScreen()

        if self.settings_manager.get_auto_start():
            QTimer.singleShot(1000, self.start_all_cameras)

    # ── Close ──────────────────────────────────────────────
    def closeEvent(self, event):
        if (self.settings_manager.settings.value("startup/close_to_tray", False, type=bool)
                and self.system_tray.is_available()):
            self.hide()
            if self.settings_manager.settings.value("notifications/show_notifications", True, type=bool):
                self.system_tray.show_message(
                    "CCTV Viewer",
                    "Application closed to system tray. Right-click tray icon to quit.",
                    timeout=3000)
            event.ignore()
            return

        if self.settings_manager.settings.value("ui/confirm_exit", True, type=bool):
            reply = QMessageBox.question(
                self, "Confirm Exit",
                "Are you sure you want to exit CCTV Viewer?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.No)
            if reply != QMessageBox.StandardButton.Yes:
                event.ignore()
                return

        # Save state
        self._save_geometry()
        self.save_cameras()

        # Stop everything
        for widget in self.camera_manager.camera_widgets.values():
            widget.stop_stream()
        self.camera_manager.stop_all()

        if self.system_tray.is_available():
            self.system_tray.hide_tray_icon()

        event.accept()
