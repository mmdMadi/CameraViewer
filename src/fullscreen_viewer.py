import cv2
import logging
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                               QPushButton, QFrame, QApplication)
from PySide6.QtCore import Qt, QTimer, Signal
from PySide6.QtGui import QPixmap, QImage, QKeySequence, QShortcut

logger = logging.getLogger("CCTV_Viewer")


class FullscreenViewer(QWidget):
    closed = Signal()

    def __init__(self, camera_widget, parent=None):
        super().__init__(parent)
        self.camera_widget = camera_widget
        self._recording = False
        self.setWindowFlags(Qt.WindowType.Window | Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose)

        self.showFullScreen()
        self.setup_ui()
        self.setup_shortcuts()

        if camera_widget.stream_thread:
            camera_widget.stream_thread.frame_ready.connect(self.update_frame)

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        # Top control bar
        self.control_bar = QFrame()
        self.control_bar.setStyleSheet("""
            QFrame { background-color: rgba(0,0,0,180); border: none; }
            QPushButton {
                background-color: rgba(255,255,255,50);
                border: 1px solid rgba(255,255,255,100);
                color: white; padding: 8px 16px;
                border-radius: 4px; font-size: 12px;
            }
            QPushButton:hover { background-color: rgba(255,255,255,80); }
            QLabel { color: white; font-size: 14px; font-weight: bold; }
        """)
        self.control_bar.setFixedHeight(60)
        self.control_bar.hide()

        ctrl = QHBoxLayout(self.control_bar)
        ctrl.setContentsMargins(20, 10, 20, 10)

        self.camera_name_label = QLabel(self.camera_widget.camera_info.get('name', 'Camera'))
        ctrl.addWidget(self.camera_name_label)
        ctrl.addStretch()

        self.record_button = QPushButton("\u23fa Record")
        self.record_button.clicked.connect(self.toggle_recording)
        ctrl.addWidget(self.record_button)

        self.snapshot_button = QPushButton("\U0001f4f7 Snapshot")
        self.snapshot_button.clicked.connect(self.take_snapshot)
        ctrl.addWidget(self.snapshot_button)

        self.close_button = QPushButton("\u2715 Close")
        self.close_button.clicked.connect(self.close)
        ctrl.addWidget(self.close_button)

        layout.addWidget(self.control_bar)

        self.video_label = QLabel()
        self.video_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.video_label.setStyleSheet("background-color: black;")
        layout.addWidget(self.video_label)

        self.status_overlay = QLabel("Press ESC to exit | Move mouse to show controls")
        self.status_overlay.setStyleSheet(
            "QLabel { background-color: rgba(0,0,0,180); color: white; "
            "padding: 10px 20px; font-size: 12px; }")
        self.status_overlay.setFixedHeight(40)
        layout.addWidget(self.status_overlay)

        self.setMouseTracking(True)
        self.control_timer = QTimer(self)
        self.control_timer.setSingleShot(True)
        self.control_timer.timeout.connect(self.hide_controls)

    def setup_shortcuts(self):
        QShortcut(QKeySequence(Qt.Key.Key_Escape), self, activated=self.close)
        QShortcut(QKeySequence(Qt.Key.Key_F11), self, activated=self.close)
        QShortcut(QKeySequence(Qt.Key.Key_Space), self, activated=self.take_snapshot)
        QShortcut(QKeySequence(Qt.Key.Key_R), self, activated=self.toggle_recording)

    # ── Controls visibility ────────────────────────────────
    def mouseMoveEvent(self, event):
        self.show_controls()
        super().mouseMoveEvent(event)

    def show_controls(self):
        self.control_bar.show()
        self.control_timer.start(3000)

    def hide_controls(self):
        self.control_bar.hide()

    # ── Frame rendering ────────────────────────────────────
    def update_frame(self, frame):
        try:
            if frame is None or frame.size == 0:
                return
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            screen = self.size()
            h, w, ch = rgb.shape
            aspect = w / h
            screen_aspect = screen.width() / screen.height()

            if aspect > screen_aspect:
                nw = screen.width()
                nh = max(int(nw / aspect), 1)
            else:
                nh = screen.height()
                nw = max(int(nh * aspect), 1)

            resized = cv2.resize(rgb, (nw, nh))
            bytes_per_line = ch * nw
            img = QImage(resized.data, nw, nh, bytes_per_line, QImage.Format.Format_RGB888)
            self.video_label.setPixmap(QPixmap.fromImage(img))
        except Exception as e:
            logger.error(f"Fullscreen display error: {e}")

    # ── Recording ──────────────────────────────────────────
    def toggle_recording(self):
        cw = self.camera_widget
        cw.toggle_recording()
        self._recording = cw.recording_manager.is_recording(cw.camera_id)
        if self._recording:
            self.record_button.setText("\u23f9 Stop")
            self.record_button.setStyleSheet("background-color: rgba(255,0,0,100);")
            self.status_overlay.setText("Recording... | Press R to stop | ESC to exit")
        else:
            self.record_button.setText("\u23fa Record")
            self.record_button.setStyleSheet("")
            self.status_overlay.setText("Recording stopped | Press ESC to exit")

    def take_snapshot(self):
        cw = self.camera_widget
        if cw.current_frame is not None:
            from .snapshot_manager import SnapshotManager
            sm = SnapshotManager()
            sm.take_snapshot(cw.current_frame, cw.camera_info.get('name', 'Camera'))
            self.status_overlay.setText("Snapshot saved! | ESC to exit")
            QTimer.singleShot(2000,
                lambda: self.status_overlay.setText("Press ESC to exit | Move mouse to show controls"))

    # ── Cleanup ────────────────────────────────────────────
    def closeEvent(self, event):
        if self.camera_widget.stream_thread:
            try:
                self.camera_widget.stream_thread.frame_ready.disconnect(self.update_frame)
            except RuntimeError:
                pass
        self.closed.emit()
        event.accept()
