from PySide6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QFormLayout,
                               QLineEdit, QPushButton, QLabel, QComboBox,
                               QSpinBox, QCheckBox, QGroupBox, QTextEdit,
                               QMessageBox)
from PySide6.QtCore import Qt


class AddCameraDialog(QDialog):
    def __init__(self, parent=None, camera_info=None):
        super().__init__(parent)
        self.camera_info = camera_info or {}

        self.setWindowTitle("Add Camera" if not camera_info else "Edit Camera")
        self.setModal(True)
        self.setMinimumSize(450, 400)

        self.setup_ui()
        self.load_camera_info()

    def setup_ui(self):
        layout = QVBoxLayout(self)

        # Basic
        basic_group = QGroupBox("Basic Settings")
        bl = QFormLayout(basic_group)

        self.name_edit = QLineEdit()
        self.name_edit.setPlaceholderText("Enter camera name")
        bl.addRow("Name:", self.name_edit)

        self.url_edit = QLineEdit()
        self.url_edit.setPlaceholderText("rtsp://username:password@ip:port/path")
        bl.addRow("Stream URL:", self.url_edit)

        self.description_edit = QTextEdit()
        self.description_edit.setMaximumHeight(60)
        self.description_edit.setPlaceholderText("Optional description")
        bl.addRow("Description:", self.description_edit)

        layout.addWidget(basic_group)

        # Video
        video_group = QGroupBox("Video Settings")
        vl = QFormLayout(video_group)

        self.fps_spin = QSpinBox()
        self.fps_spin.setRange(1, 60)
        self.fps_spin.setValue(30)
        self.fps_spin.setSuffix(" FPS")
        vl.addRow("Frame Rate:", self.fps_spin)

        self.resolution_combo = QComboBox()
        self.resolution_combo.addItems([
            "Auto (Camera Default)",
            "1920x1080 (Full HD)",
            "1280x720 (HD)",
            "640x480 (VGA)",
            "320x240 (QVGA)",
        ])
        vl.addRow("Resolution:", self.resolution_combo)

        self.mode_combo = QComboBox()
        self.mode_combo.addItems([
            "Low Latency (Minimal delay)",
            "Balanced (Good quality & speed)",
            "High Quality (Best image quality)",
        ])
        vl.addRow("Stream Mode:", self.mode_combo)

        layout.addWidget(video_group)

        # Connection
        conn_group = QGroupBox("Connection Settings")
        cl = QFormLayout(conn_group)

        self.timeout_spin = QSpinBox()
        self.timeout_spin.setRange(1, 60)
        self.timeout_spin.setValue(10)
        self.timeout_spin.setSuffix(" seconds")
        cl.addRow("Timeout:", self.timeout_spin)

        self.retry_spin = QSpinBox()
        self.retry_spin.setRange(0, 10)
        self.retry_spin.setValue(3)
        cl.addRow("Retry Count:", self.retry_spin)

        self.auto_start_check = QCheckBox("Auto-start stream")
        self.auto_start_check.setChecked(True)
        cl.addRow("", self.auto_start_check)

        layout.addWidget(conn_group)

        # Examples
        examples_group = QGroupBox("Common URL Examples")
        el = QVBoxLayout(examples_group)
        examples = QLabel(
            "\u2022 RTSP: rtsp://username:password@192.168.1.100:554/stream1\n"
            "\u2022 HTTP: http://192.168.1.100:8080/video\n"
            "\u2022 MJPEG: http://192.168.1.100/mjpg/video.mjpg\n"
            "\u2022 USB Camera: 0 (for first USB camera)")
        examples.setWordWrap(True)
        examples.setStyleSheet("font-size: 10px; color: #666666;")
        el.addWidget(examples)
        layout.addWidget(examples_group)

        # Buttons
        btn = QHBoxLayout()
        btn.addStretch()

        self.test_button = QPushButton("Test Connection")
        self.test_button.clicked.connect(self.test_connection)
        btn.addWidget(self.test_button)

        cancel = QPushButton("Cancel")
        cancel.clicked.connect(self.reject)
        btn.addWidget(cancel)

        ok = QPushButton("OK")
        ok.clicked.connect(self.accept)
        ok.setDefault(True)
        btn.addWidget(ok)

        layout.addLayout(btn)

    def load_camera_info(self):
        if not self.camera_info:
            return
        self.name_edit.setText(self.camera_info.get('name', ''))
        self.url_edit.setText(self.camera_info.get('url', ''))
        self.description_edit.setPlainText(self.camera_info.get('description', ''))
        self.timeout_spin.setValue(self.camera_info.get('timeout', 10))
        self.retry_spin.setValue(self.camera_info.get('retry_count', 3))
        self.fps_spin.setValue(self.camera_info.get('fps', 30))
        self.auto_start_check.setChecked(self.camera_info.get('auto_start', True))
        self.resolution_combo.setCurrentText(
            self.camera_info.get('resolution', 'Auto (Camera Default)'))
        self.mode_combo.setCurrentText(
            self.camera_info.get('mode', 'Low Latency (Minimal delay)'))

    def get_camera_info(self):
        return {
            'name': self.name_edit.text().strip() or 'Unnamed Camera',
            'url': self.url_edit.text().strip(),
            'description': self.description_edit.toPlainText().strip(),
            'timeout': self.timeout_spin.value(),
            'retry_count': self.retry_spin.value(),
            'fps': self.fps_spin.value(),
            'auto_start': self.auto_start_check.isChecked(),
            'resolution': self.resolution_combo.currentText(),
            'mode': self.mode_combo.currentText(),
        }

    def test_connection(self):
        url = self.url_edit.text().strip()
        if not url:
            self._show_msg("Please enter a stream URL first.")
            return

        import cv2
        self.test_button.setText("Testing...")
        self.test_button.setEnabled(False)

        try:
            cap = cv2.VideoCapture(url)
            if cap.isOpened():
                ret, frame = cap.read()
                cap.release()
                if ret:
                    h, w = frame.shape[:2]
                    self._show_msg(f"Connection successful! ({w}x{h})")
                else:
                    self._show_msg("Connected but no frames received.")
            else:
                self._show_msg("Failed to connect to stream.")
        except Exception as e:
            self._show_msg(f"Connection error: {e}")
        finally:
            self.test_button.setText("Test Connection")
            self.test_button.setEnabled(True)

    def _show_msg(self, message):
        QMessageBox.information(self, "Connection Test", message)

    def accept(self):
        if not self.url_edit.text().strip():
            self._show_msg("Please enter a stream URL.")
            return
        super().accept()
