from PySide6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QTabWidget,
                               QWidget, QFormLayout, QComboBox, QSpinBox,
                               QCheckBox, QPushButton, QGroupBox, QLabel,
                               QSlider, QLineEdit, QFileDialog, QScrollArea)
from PySide6.QtCore import Qt


class SettingsDialog(QDialog):
    def __init__(self, settings_manager, parent=None):
        super().__init__(parent)
        self.settings_manager = settings_manager

        self.setWindowTitle("CCTV Viewer - Settings")
        self.setModal(True)
        self.setMinimumSize(700, 600)
        self.resize(800, 700)

        self.setup_ui()
        self.load_settings()

    # ── Layout ─────────────────────────────────────────────
    def setup_ui(self):
        layout = QVBoxLayout(self)

        self.tab_widget = QTabWidget()
        self._setup_appearance_tab()
        self._setup_display_tab()
        self._setup_network_tab()
        self._setup_general_tab()
        layout.addWidget(self.tab_widget)

        btn = QHBoxLayout()
        btn.addStretch()

        restore = QPushButton("Restore Defaults")
        restore.clicked.connect(self.restore_defaults)
        btn.addWidget(restore)

        cancel = QPushButton("Cancel")
        cancel.clicked.connect(self.reject)
        btn.addWidget(cancel)

        ok = QPushButton("OK")
        ok.clicked.connect(self.accept)
        ok.setDefault(True)
        btn.addWidget(ok)

        layout.addLayout(btn)

    # ── Appearance ─────────────────────────────────────────
    def _setup_appearance_tab(self):
        w = QWidget()
        layout = QVBoxLayout(w)

        theme_group = QGroupBox("Theme & Colors")
        tl = QFormLayout(theme_group)
        self.theme_combo = QComboBox()
        self.theme_combo.addItems(["Light", "Dark", "Auto (System)"])
        tl.addRow("Theme:", self.theme_combo)
        layout.addWidget(theme_group)

        ui_group = QGroupBox("User Interface")
        ul = QFormLayout(ui_group)

        self.show_toolbar_check = QCheckBox("Show toolbar on startup")
        ul.addRow("", self.show_toolbar_check)

        self.show_statusbar_check = QCheckBox("Show status bar")
        ul.addRow("", self.show_statusbar_check)

        self.fullscreen_startup_check = QCheckBox("Start in fullscreen mode")
        ul.addRow("", self.fullscreen_startup_check)

        self.confirm_exit_check = QCheckBox("Confirm before exiting")
        ul.addRow("", self.confirm_exit_check)

        self.opacity_slider = QSlider(Qt.Orientation.Horizontal)
        self.opacity_slider.setRange(50, 100)
        self.opacity_slider.setTickPosition(QSlider.TickPosition.TicksBelow)
        self.opacity_slider.setTickInterval(10)
        self.opacity_label = QLabel("100%")
        self.opacity_slider.valueChanged.connect(lambda v: self.opacity_label.setText(f"{v}%"))
        ol = QHBoxLayout()
        ol.addWidget(self.opacity_slider)
        ol.addWidget(self.opacity_label)
        ul.addRow("Window Opacity:", ol)

        layout.addWidget(ui_group)
        layout.addStretch()
        self.tab_widget.addTab(w, "Appearance")

    # ── Display ────────────────────────────────────────────
    def _setup_display_tab(self):
        w = QWidget()
        layout = QVBoxLayout(w)

        grid_group = QGroupBox("Camera Grid Layout")
        gl = QFormLayout(grid_group)

        self.columns_spin = QSpinBox()
        self.columns_spin.setRange(1, 10)
        gl.addRow("Grid Columns:", self.columns_spin)

        self.aspect_ratio_combo = QComboBox()
        self.aspect_ratio_combo.addItems(["16:9", "4:3", "1:1", "Auto"])
        gl.addRow("Camera Aspect Ratio:", self.aspect_ratio_combo)

        self.grid_spacing_spin = QSpinBox()
        self.grid_spacing_spin.setRange(0, 20)
        self.grid_spacing_spin.setSuffix(" px")
        gl.addRow("Grid Spacing:", self.grid_spacing_spin)

        self.show_camera_names_check = QCheckBox("Show camera names")
        gl.addRow("", self.show_camera_names_check)

        self.show_camera_status_check = QCheckBox("Show camera status")
        gl.addRow("", self.show_camera_status_check)

        layout.addWidget(grid_group)

        video_group = QGroupBox("Video Display & Performance")
        vl = QFormLayout(video_group)

        self.fps_limit_spin = QSpinBox()
        self.fps_limit_spin.setRange(1, 60)
        self.fps_limit_spin.setSuffix(" FPS")
        vl.addRow("Default FPS Limit:", self.fps_limit_spin)

        self.buffer_size_spin = QSpinBox()
        self.buffer_size_spin.setRange(1, 10)
        vl.addRow("Stream Buffer Size:", self.buffer_size_spin)

        self.hardware_accel_check = QCheckBox("Use hardware acceleration (if available)")
        vl.addRow("", self.hardware_accel_check)

        self.smooth_scaling_check = QCheckBox("Smooth video scaling")
        vl.addRow("", self.smooth_scaling_check)

        self.video_quality_combo = QComboBox()
        self.video_quality_combo.addItems(["High", "Medium", "Low", "Auto"])
        vl.addRow("Video Quality:", self.video_quality_combo)

        layout.addWidget(video_group)
        layout.addStretch()
        self.tab_widget.addTab(w, "Display")

    # ── Network ────────────────────────────────────────────
    def _setup_network_tab(self):
        w = QWidget()
        layout = QVBoxLayout(w)

        conn_group = QGroupBox("Connection")
        cl = QFormLayout(conn_group)

        self.timeout_spin = QSpinBox()
        self.timeout_spin.setRange(1, 60)
        self.timeout_spin.setSuffix(" seconds")
        cl.addRow("Connection Timeout:", self.timeout_spin)

        self.reconnect_spin = QSpinBox()
        self.reconnect_spin.setRange(1, 60)
        self.reconnect_spin.setSuffix(" seconds")
        cl.addRow("Reconnect Interval:", self.reconnect_spin)

        self.max_retries_spin = QSpinBox()
        self.max_retries_spin.setRange(0, 20)
        cl.addRow("Max Retries:", self.max_retries_spin)

        layout.addWidget(conn_group)

        adv_group = QGroupBox("Advanced")
        al = QFormLayout(adv_group)

        self.user_agent_combo = QComboBox()
        self.user_agent_combo.setEditable(True)
        self.user_agent_combo.addItems([
            "CCTV Viewer/1.0",
            "VLC/3.0.0",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
        ])
        al.addRow("User Agent:", self.user_agent_combo)

        self.tcp_transport_check = QCheckBox("Force TCP transport")
        al.addRow("", self.tcp_transport_check)

        layout.addWidget(adv_group)
        layout.addStretch()
        self.tab_widget.addTab(w, "Network")

    # ── General ────────────────────────────────────────────
    def _setup_general_tab(self):
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)

        w = QWidget()
        layout = QVBoxLayout(w)

        # Startup
        startup_group = QGroupBox("Application Startup & Behavior")
        sl = QFormLayout(startup_group)
        self.auto_start_check = QCheckBox("Auto-start all cameras on startup")
        sl.addRow("Camera Startup:", self.auto_start_check)
        self.restore_layout_check = QCheckBox("Restore window size and position")
        sl.addRow("Window Layout:", self.restore_layout_check)
        layout.addWidget(startup_group)

        # Tray
        tray_group = QGroupBox("System Tray Integration")
        tl = QFormLayout(tray_group)
        self.close_tray_check = QCheckBox("Close to system tray (don't exit)")
        tl.addRow("Close Behavior:", self.close_tray_check)
        layout.addWidget(tray_group)

        # Paths
        paths_group = QGroupBox("File Storage Locations")
        pl = QFormLayout(paths_group)

        self.recording_path_edit = QLineEdit()
        self.recording_path_edit.setText("recordings")
        rec_btn = QPushButton("Browse...")
        rec_btn.setMaximumWidth(80)
        rec_btn.clicked.connect(lambda: self._browse_folder(self.recording_path_edit))
        rl = QHBoxLayout()
        rl.addWidget(self.recording_path_edit)
        rl.addWidget(rec_btn)
        pl.addRow("Recordings:", rl)

        self.snapshot_path_edit = QLineEdit()
        self.snapshot_path_edit.setText("snapshots")
        snap_btn = QPushButton("Browse...")
        snap_btn.setMaximumWidth(80)
        snap_btn.clicked.connect(lambda: self._browse_folder(self.snapshot_path_edit))
        sl2 = QHBoxLayout()
        sl2.addWidget(self.snapshot_path_edit)
        sl2.addWidget(snap_btn)
        pl.addRow("Snapshots:", sl2)

        layout.addWidget(paths_group)

        # Recording
        rec_group = QGroupBox("Recording & Snapshot Settings")
        rl2 = QFormLayout(rec_group)

        self.record_format_combo = QComboBox()
        self.record_format_combo.addItems(["MP4", "AVI", "MOV", "MKV"])
        rl2.addRow("Video Format:", self.record_format_combo)

        self.record_quality_combo = QComboBox()
        self.record_quality_combo.addItems(["High", "Medium", "Low", "Lossless"])
        rl2.addRow("Video Quality:", self.record_quality_combo)

        self.snapshot_format_combo = QComboBox()
        self.snapshot_format_combo.addItems(["JPG", "PNG", "BMP"])
        rl2.addRow("Image Format:", self.snapshot_format_combo)

        self.auto_record_check = QCheckBox("Auto-record when camera starts")
        rl2.addRow("Auto Recording:", self.auto_record_check)

        self.record_audio_check = QCheckBox("Record audio (if available)")
        rl2.addRow("Audio Recording:", self.record_audio_check)

        layout.addWidget(rec_group)

        # Notifications
        notif_group = QGroupBox("Notifications & Alerts")
        nl = QFormLayout(notif_group)
        self.show_notifications_check = QCheckBox("Enable system notifications")
        nl.addRow("System Notifications:", self.show_notifications_check)
        self.notify_connection_check = QCheckBox("Camera connection/disconnection events")
        nl.addRow("Connection Events:", self.notify_connection_check)
        self.notify_recording_check = QCheckBox("Recording start/stop events")
        nl.addRow("Recording Events:", self.notify_recording_check)
        self.sound_alerts_check = QCheckBox("Play sound alerts")
        nl.addRow("Sound Alerts:", self.sound_alerts_check)
        layout.addWidget(notif_group)

        # Logging
        log_group = QGroupBox("Logging & Debugging")
        ll = QFormLayout(log_group)
        self.log_level_combo = QComboBox()
        self.log_level_combo.addItems(["Debug", "Info", "Warning", "Error", "Critical"])
        ll.addRow("Log Level:", self.log_level_combo)
        self.log_to_file_check = QCheckBox("Enable file logging")
        ll.addRow("File Logging:", self.log_to_file_check)
        self.log_file_path_edit = QLineEdit()
        self.log_file_path_edit.setText("logs/cctv_viewer.log")
        log_btn = QPushButton("Browse...")
        log_btn.setMaximumWidth(80)
        log_btn.clicked.connect(
            lambda: self._browse_file(self.log_file_path_edit, "Log Files (*.log *.txt)"))
        lp = QHBoxLayout()
        lp.addWidget(self.log_file_path_edit)
        lp.addWidget(log_btn)
        ll.addRow("Log File Path:", lp)
        self.max_log_size_spin = QSpinBox()
        self.max_log_size_spin.setRange(1, 1000)
        self.max_log_size_spin.setSuffix(" MB")
        ll.addRow("Max File Size:", self.max_log_size_spin)
        layout.addWidget(log_group)

        layout.addStretch()

        scroll.setWidget(w)
        self.tab_widget.addTab(scroll, "General")

    # ── Load ───────────────────────────────────────────────
    def load_settings(self):
        s = self.settings_manager.settings

        theme = self.settings_manager.get_theme()
        self.theme_combo.setCurrentText("Dark" if theme == "dark" else "Auto (System)" if theme == "auto" else "Light")

        self.columns_spin.setValue(self.settings_manager.get_grid_columns())
        self.timeout_spin.setValue(self.settings_manager.get_connection_timeout())
        self.reconnect_spin.setValue(self.settings_manager.get_reconnect_interval())
        self.auto_start_check.setChecked(self.settings_manager.get_auto_start())

        self.show_toolbar_check.setChecked(s.value("ui/show_toolbar", True, type=bool))
        self.show_statusbar_check.setChecked(s.value("ui/show_statusbar", True, type=bool))
        self.fullscreen_startup_check.setChecked(s.value("ui/fullscreen_startup", False, type=bool))
        self.confirm_exit_check.setChecked(s.value("ui/confirm_exit", True, type=bool))
        self.opacity_slider.setValue(int(s.value("ui/window_opacity", 100)))

        self.aspect_ratio_combo.setCurrentText(s.value("display/aspect_ratio", "16:9"))
        self.grid_spacing_spin.setValue(int(s.value("display/grid_spacing", 5)))
        self.show_camera_names_check.setChecked(s.value("display/show_names", True, type=bool))
        self.show_camera_status_check.setChecked(s.value("display/show_status", True, type=bool))

        self.fps_limit_spin.setValue(int(s.value("video/fps_limit", 30)))
        self.buffer_size_spin.setValue(int(s.value("video/buffer_size", 1)))
        self.hardware_accel_check.setChecked(s.value("video/hardware_accel", False, type=bool))
        self.smooth_scaling_check.setChecked(s.value("video/smooth_scaling", True, type=bool))
        self.video_quality_combo.setCurrentText(s.value("video/quality", "Medium"))

        self.max_retries_spin.setValue(int(s.value("network/max_retries", 3)))
        self.user_agent_combo.setCurrentText(s.value("network/user_agent", "CCTV Viewer/1.0"))
        self.tcp_transport_check.setChecked(s.value("network/tcp_transport", False, type=bool))

        self.restore_layout_check.setChecked(s.value("startup/restore_layout", True, type=bool))
        self.close_tray_check.setChecked(s.value("startup/close_to_tray", False, type=bool))

        self.recording_path_edit.setText(s.value("paths/recording", "recordings"))
        self.snapshot_path_edit.setText(s.value("paths/snapshots", "snapshots"))

        self.record_format_combo.setCurrentText(s.value("recording/format", "MP4"))
        self.record_quality_combo.setCurrentText(s.value("recording/quality", "Medium"))
        self.snapshot_format_combo.setCurrentText(s.value("recording/snapshot_format", "JPG"))
        self.auto_record_check.setChecked(s.value("recording/auto_record", False, type=bool))
        self.record_audio_check.setChecked(s.value("recording/record_audio", False, type=bool))

        self.show_notifications_check.setChecked(s.value("notifications/show_notifications", True, type=bool))
        self.notify_connection_check.setChecked(s.value("notifications/connection_events", True, type=bool))
        self.notify_recording_check.setChecked(s.value("notifications/recording_events", True, type=bool))
        self.sound_alerts_check.setChecked(s.value("notifications/sound_alerts", False, type=bool))

        self.log_level_combo.setCurrentText(s.value("logging/level", "Info"))
        self.log_to_file_check.setChecked(s.value("logging/to_file", False, type=bool))
        self.log_file_path_edit.setText(s.value("logging/file_path", "logs/cctv_viewer.log"))
        self.max_log_size_spin.setValue(int(s.value("logging/max_size_mb", 10)))

    # ── Save ───────────────────────────────────────────────
    def save_settings(self):
        s = self.settings_manager.settings

        theme_map = {"Dark": "dark", "Auto (System)": "auto", "Light": "light"}
        self.settings_manager.set_theme(theme_map.get(self.theme_combo.currentText(), "light"))

        s.setValue("ui/show_toolbar", self.show_toolbar_check.isChecked())
        s.setValue("ui/show_statusbar", self.show_statusbar_check.isChecked())
        s.setValue("ui/fullscreen_startup", self.fullscreen_startup_check.isChecked())
        s.setValue("ui/confirm_exit", self.confirm_exit_check.isChecked())
        s.setValue("ui/window_opacity", self.opacity_slider.value())

        self.settings_manager.set_grid_columns(self.columns_spin.value())
        s.setValue("display/aspect_ratio", self.aspect_ratio_combo.currentText())
        s.setValue("display/grid_spacing", self.grid_spacing_spin.value())
        s.setValue("display/show_names", self.show_camera_names_check.isChecked())
        s.setValue("display/show_status", self.show_camera_status_check.isChecked())

        s.setValue("video/fps_limit", self.fps_limit_spin.value())
        s.setValue("video/buffer_size", self.buffer_size_spin.value())
        s.setValue("video/hardware_accel", self.hardware_accel_check.isChecked())
        s.setValue("video/smooth_scaling", self.smooth_scaling_check.isChecked())
        s.setValue("video/quality", self.video_quality_combo.currentText())

        self.settings_manager.set_connection_timeout(self.timeout_spin.value())
        self.settings_manager.set_reconnect_interval(self.reconnect_spin.value())
        s.setValue("network/max_retries", self.max_retries_spin.value())
        s.setValue("network/user_agent", self.user_agent_combo.currentText())
        s.setValue("network/tcp_transport", self.tcp_transport_check.isChecked())

        self.settings_manager.set_auto_start(self.auto_start_check.isChecked())
        s.setValue("startup/restore_layout", self.restore_layout_check.isChecked())
        s.setValue("startup/close_to_tray", self.close_tray_check.isChecked())

        s.setValue("paths/recording", self.recording_path_edit.text())
        s.setValue("paths/snapshots", self.snapshot_path_edit.text())

        s.setValue("recording/format", self.record_format_combo.currentText())
        s.setValue("recording/quality", self.record_quality_combo.currentText())
        s.setValue("recording/snapshot_format", self.snapshot_format_combo.currentText())
        s.setValue("recording/auto_record", self.auto_record_check.isChecked())
        s.setValue("recording/record_audio", self.record_audio_check.isChecked())

        s.setValue("notifications/show_notifications", self.show_notifications_check.isChecked())
        s.setValue("notifications/connection_events", self.notify_connection_check.isChecked())
        s.setValue("notifications/recording_events", self.notify_recording_check.isChecked())
        s.setValue("notifications/sound_alerts", self.sound_alerts_check.isChecked())

        s.setValue("logging/level", self.log_level_combo.currentText())
        s.setValue("logging/to_file", self.log_to_file_check.isChecked())
        s.setValue("logging/file_path", self.log_file_path_edit.text())
        s.setValue("logging/max_size_mb", self.max_log_size_spin.value())

    # ── Defaults ───────────────────────────────────────────
    def restore_defaults(self):
        self.theme_combo.setCurrentText("Light")
        self.columns_spin.setValue(3)
        self.timeout_spin.setValue(10)
        self.reconnect_spin.setValue(5)
        self.max_retries_spin.setValue(3)
        self.auto_start_check.setChecked(True)
        self.restore_layout_check.setChecked(True)
        self.close_tray_check.setChecked(False)
        self.show_toolbar_check.setChecked(True)
        self.show_statusbar_check.setChecked(True)
        self.fullscreen_startup_check.setChecked(False)
        self.confirm_exit_check.setChecked(True)
        self.opacity_slider.setValue(100)
        self.fps_limit_spin.setValue(30)
        self.buffer_size_spin.setValue(1)
        self.hardware_accel_check.setChecked(False)
        self.smooth_scaling_check.setChecked(True)
        self.video_quality_combo.setCurrentText("Medium")
        self.aspect_ratio_combo.setCurrentText("16:9")
        self.grid_spacing_spin.setValue(5)
        self.show_camera_names_check.setChecked(True)
        self.show_camera_status_check.setChecked(True)
        self.user_agent_combo.setCurrentText("CCTV Viewer/1.0")
        self.tcp_transport_check.setChecked(False)
        self.recording_path_edit.setText("recordings")
        self.snapshot_path_edit.setText("snapshots")
        self.record_format_combo.setCurrentText("MP4")
        self.record_quality_combo.setCurrentText("Medium")
        self.snapshot_format_combo.setCurrentText("JPG")
        self.auto_record_check.setChecked(False)
        self.record_audio_check.setChecked(False)
        self.show_notifications_check.setChecked(True)
        self.notify_connection_check.setChecked(True)
        self.notify_recording_check.setChecked(True)
        self.sound_alerts_check.setChecked(False)
        self.log_level_combo.setCurrentText("Info")
        self.log_to_file_check.setChecked(False)
        self.log_file_path_edit.setText("logs/cctv_viewer.log")
        self.max_log_size_spin.setValue(10)

    # ── Helpers ────────────────────────────────────────────
    def _browse_folder(self, line_edit):
        folder = QFileDialog.getExistingDirectory(self, "Select Folder", line_edit.text())
        if folder:
            line_edit.setText(folder)

    def _browse_file(self, line_edit, file_filter="All Files (*)"):
        file_path, _ = QFileDialog.getSaveFileName(self, "Select File", line_edit.text(), file_filter)
        if file_path:
            line_edit.setText(file_path)

    def accept(self):
        self.save_settings()
        super().accept()
