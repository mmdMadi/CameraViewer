import cv2
import os
import time
import logging
import numpy as np
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                               QPushButton, QFrame, QMenu, QMessageBox)
from PySide6.QtCore import Qt, QTimer, Signal, QThread
from PySide6.QtGui import QPixmap, QImage, QAction

logger = logging.getLogger("CCTV_Viewer")


class CameraStreamThread(QThread):
    frame_ready = Signal(np.ndarray)
    error_occurred = Signal(str)

    def __init__(self, url, fps=30, low_latency=True, camera_info=None):
        super().__init__()
        self.url = url
        self.fps = max(1, min(fps, 60))
        self.frame_delay = int(1000 / self.fps)
        self.low_latency = low_latency
        self.camera_info = camera_info or {}
        self.running = False
        self.cap = None

    def run(self):
        self.running = True
        logger.info(f"Starting stream: {self.url} (FPS={self.fps}, low_latency={self.low_latency})")

        try:
            try:
                camera_index = int(self.url)
                self.cap = cv2.VideoCapture(camera_index)
            except (ValueError, TypeError):
                self.cap = cv2.VideoCapture(self.url)

            from .stream_optimizer import StreamOptimizer, NetworkStreamOptimizer
            optimizer = StreamOptimizer()
            optimizer.optimize_capture_properties(self.cap, self.url, self.low_latency)
            self._apply_resolution_settings()

            if isinstance(self.url, str):
                url_lower = self.url.lower()
                if 'rtsp://' in url_lower:
                    NetworkStreamOptimizer.apply_opencv_optimizations(self.cap, 'rtsp')
                elif 'http://' in url_lower:
                    NetworkStreamOptimizer.apply_opencv_optimizations(self.cap, 'http')

            self.cap.set(cv2.CAP_PROP_FPS, self.fps)

            if not self.cap.isOpened():
                logger.error(f"Failed to open stream: {self.url}")
                self.error_occurred.emit(f"Failed to open stream: {self.url}")
                return

            ret, test_frame = self.cap.read()
            if not ret:
                logger.error(f"Cannot read first frame: {self.url}")
                self.error_occurred.emit("Cannot read from stream - check URL/format")
                return

            logger.info(f"Connected to {self.url} ({test_frame.shape[1]}x{test_frame.shape[0]})")

            consecutive_failures = 0
            last_frame_time = 0

            while self.running:
                current_time = int(time.time() * 1000)
                ret, frame = self.cap.read()

                if ret and frame is not None:
                    if current_time - last_frame_time >= self.frame_delay:
                        self.frame_ready.emit(frame)
                        last_frame_time = current_time
                        consecutive_failures = 0

                    # Drain buffer for network streams
                    if isinstance(self.url, str):
                        url_lower = self.url.lower()
                        if 'rtsp://' in url_lower or 'http://' in url_lower:
                            for _ in range(2):
                                if not self.cap.grab():
                                    break
                else:
                    consecutive_failures += 1
                    if consecutive_failures > 10:
                        msg = "No frames received" if consecutive_failures <= 11 else "Stream ended"
                        self.error_occurred.emit(msg)
                        break

                self.msleep(1)

        except Exception as e:
            self.error_occurred.emit(f"Stream error: {e}")
        finally:
            if self.cap:
                self.cap.release()

    def _apply_resolution_settings(self):
        resolution = self.camera_info.get('resolution', 'Auto (Camera Default)')
        resolutions = {
            "1920x1080 (Full HD)": (1920, 1080),
            "1280x720 (HD)": (1280, 720),
            "640x480 (VGA)": (640, 480),
            "320x240 (QVGA)": (320, 240),
        }
        size = resolutions.get(resolution)
        if size and self.cap:
            self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, size[0])
            self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, size[1])

    def stop(self):
        self.running = False
        self.wait(5000)  # 5s timeout to avoid hanging


class CameraWidget(QFrame):
    def __init__(self, camera_id, camera_info, camera_manager):
        super().__init__()
        self.camera_id = camera_id
        self.camera_info = camera_info
        self.camera_manager = camera_manager
        self.stream_thread = None
        self.is_streaming = False
        self.current_frame = None
        self.performance_timer = QTimer()
        self.performance_timer.timeout.connect(self.update_performance_stats)

        from .recording_manager import RecordingManager
        from .snapshot_manager import SnapshotManager
        from .stream_optimizer import StreamOptimizer
        self.recording_manager = RecordingManager()
        self.snapshot_manager = SnapshotManager()
        self.stream_optimizer = StreamOptimizer()

        self.setFrameStyle(QFrame.Shape.Box)
        self.setLineWidth(2)
        self.setMinimumSize(320, 240)
        self.setMaximumSize(640, 480)

        self.setup_ui()
        self.setup_context_menu()

    # ── UI ─────────────────────────────────────────────────
    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(5, 5, 5, 5)

        header_layout = QHBoxLayout()

        self.name_label = QLabel(self.camera_info.get('name', 'Camera'))
        self.name_label.setStyleSheet("font-weight: bold; font-size: 12px;")
        header_layout.addWidget(self.name_label)

        header_layout.addStretch()

        self.start_stop_button = QPushButton("\u25b6")
        self.start_stop_button.setMaximumSize(30, 25)
        self.start_stop_button.setToolTip("Start stream")
        self.start_stop_button.clicked.connect(self.toggle_stream)
        header_layout.addWidget(self.start_stop_button)

        self.record_button = QPushButton("\u23fa")
        self.record_button.setMaximumSize(30, 25)
        self.record_button.setToolTip("Start/Stop recording")
        self.record_button.clicked.connect(self.toggle_recording)
        self.record_button.setEnabled(False)
        header_layout.addWidget(self.record_button)

        self.snapshot_button = QPushButton("\U0001f4f7")
        self.snapshot_button.setMaximumSize(30, 25)
        self.snapshot_button.setToolTip("Take snapshot")
        self.snapshot_button.clicked.connect(self.take_snapshot)
        self.snapshot_button.setEnabled(False)
        header_layout.addWidget(self.snapshot_button)

        layout.addLayout(header_layout)

        self.video_label = QLabel()
        self.video_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.video_label.setStyleSheet(
            "QLabel { background-color: #000000; border: 1px solid #666666; "
            "color: #ffffff; cursor: pointer; }")
        self.video_label.setText("Camera Offline\n\nDouble-click to fullscreen")
        self.video_label.setMinimumSize(300, 200)
        self.video_label.mouseDoubleClickEvent = self.open_fullscreen
        layout.addWidget(self.video_label)

        self.status_label = QLabel("Disconnected")
        self.status_label.setStyleSheet("font-size: 10px; color: #888888;")
        layout.addWidget(self.status_label)

        self.performance_label = QLabel("")
        self.performance_label.setStyleSheet("font-size: 9px; color: #666666;")
        self.performance_label.hide()
        layout.addWidget(self.performance_label)

    # ── Context menu ───────────────────────────────────────
    def setup_context_menu(self):
        self.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.customContextMenuRequested.connect(self.show_context_menu)

    def show_context_menu(self, position):
        menu = QMenu(self)

        menu.addAction(QAction("Edit Camera", self, triggered=self.edit_camera))
        menu.addAction(QAction("Remove Camera", self, triggered=self.remove_camera))
        menu.addSeparator()

        if self.is_streaming:
            menu.addAction(QAction("Stop Stream", self, triggered=self.stop_stream))
            menu.addAction(QAction("Fullscreen View", self, triggered=self.open_fullscreen))
            menu.addSeparator()

            if self.recording_manager.is_recording(self.camera_id):
                menu.addAction(QAction("Stop Recording", self, triggered=self.toggle_recording))
            else:
                menu.addAction(QAction("Start Recording", self, triggered=self.toggle_recording))

            menu.addAction(QAction("Take Snapshot", self, triggered=self.take_snapshot))
        else:
            menu.addAction(QAction("Start Stream", self, triggered=self.start_stream))

        menu.exec(self.mapToGlobal(position))

    # ── Stream control ─────────────────────────────────────
    def toggle_stream(self):
        if self.is_streaming:
            self.stop_stream()
        else:
            self.start_stream()

    def start_stream(self):
        if self.is_streaming:
            return

        url = self.camera_info.get('url', '')
        if not url:
            self.status_label.setText("No URL configured")
            return

        self.video_label.clear()
        self.video_label.setText("Connecting...")

        fps = self.camera_info.get('fps', 30)
        mode = self.camera_info.get('mode', 'Low Latency (Minimal delay)')
        low_latency = 'Low Latency' in mode

        self.stream_thread = CameraStreamThread(url, fps, low_latency, self.camera_info)
        self.stream_thread.frame_ready.connect(self.update_frame)
        self.stream_thread.error_occurred.connect(self.handle_stream_error)
        self.stream_thread.start()

        self.is_streaming = True
        self.start_stop_button.setText("\u23f9")
        self.start_stop_button.setToolTip("Stop stream")
        self.record_button.setEnabled(True)
        self.snapshot_button.setEnabled(True)
        self.status_label.setText("Connecting...")

        self.stream_optimizer.reset_metrics()
        self.performance_timer.start(2000)

    def stop_stream(self):
        if not self.is_streaming:
            return

        if self.stream_thread:
            self.stream_thread.stop()
            self.stream_thread = None

        if self.recording_manager.is_recording(self.camera_id):
            self.recording_manager.stop_recording(self.camera_id)
            self.record_button.setText("\u23fa")
            self.record_button.setStyleSheet("")

        self.is_streaming = False
        self.start_stop_button.setText("\u25b6")
        self.start_stop_button.setToolTip("Start stream")
        self.record_button.setEnabled(False)
        self.snapshot_button.setEnabled(False)
        self.status_label.setText("Disconnected")

        self.performance_timer.stop()
        self.performance_label.hide()

        self.video_label.clear()
        self.video_label.setText("Camera Offline\n\nDouble-click to fullscreen")

    # ── Frame handling ─────────────────────────────────────
    def update_frame(self, frame):
        try:
            if frame is None or frame.size == 0:
                self.handle_stream_error("Received empty frame")
                return

            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            widget_size = self.video_label.size()
            if widget_size.width() <= 0 or widget_size.height() <= 0:
                return

            h, w, ch = rgb_frame.shape
            aspect_ratio = w / h
            widget_aspect = widget_size.width() / widget_size.height()

            if aspect_ratio > widget_aspect:
                new_width = widget_size.width() - 10
                new_height = max(int(new_width / aspect_ratio), 75)
            else:
                new_height = widget_size.height() - 10
                new_width = max(int(new_height * aspect_ratio), 100)

            resized = cv2.resize(rgb_frame, (new_width, new_height))
            bytes_per_line = ch * new_width
            qt_image = QImage(resized.data, new_width, new_height,
                              bytes_per_line, QImage.Format.Format_RGB888)
            pixmap = QPixmap.fromImage(qt_image)
            self.video_label.setPixmap(pixmap)

            self.current_frame = frame.copy()

            if self.recording_manager.is_recording(self.camera_id):
                self.recording_manager.add_frame(self.camera_id, frame)

            if not self.stream_optimizer.should_drop_frame(self.camera_info.get('fps', 30)):
                self.status_label.setText("Connected - Streaming")

        except Exception as e:
            self.handle_stream_error(f"Display error: {e}")

    def handle_stream_error(self, error_message):
        logger.warning(f"Stream error [{self.camera_info.get('name', '?')}]: {error_message}")
        self.status_label.setText(f"Error: {error_message}")
        self.stop_stream()

    # ── Recording / Snapshot ───────────────────────────────
    def toggle_recording(self):
        if not self.is_streaming:
            return

        if self.recording_manager.is_recording(self.camera_id):
            self.recording_manager.stop_recording(self.camera_id)
            self.record_button.setText("\u23fa")
            self.record_button.setStyleSheet("")
            self.status_label.setText("Recording stopped")
        else:
            camera_name = self.camera_info.get('name', 'Camera')
            fps = self.camera_info.get('fps', 30)
            recorder = self.recording_manager.start_recording(self.camera_id, camera_name, fps)
            if recorder:
                self.record_button.setText("\u23f9")
                self.record_button.setStyleSheet("background-color: rgba(255, 0, 0, 100);")
                self.status_label.setText("Recording...")

    def take_snapshot(self):
        if not self.is_streaming or self.current_frame is None:
            return

        camera_name = self.camera_info.get('name', 'Camera')
        filename = self.snapshot_manager.take_snapshot(self.current_frame, camera_name)
        if filename:
            self.status_label.setText(f"Snapshot: {os.path.basename(filename)}")

    # ── Fullscreen ─────────────────────────────────────────
    def open_fullscreen(self, event=None):
        if not self.is_streaming:
            return
        from .fullscreen_viewer import FullscreenViewer
        self._fullscreen_viewer = FullscreenViewer(self)
        self._fullscreen_viewer.show()

    # ── Edit / Remove ──────────────────────────────────────
    def edit_camera(self):
        from .add_camera_dialog import AddCameraDialog
        dialog = AddCameraDialog(self, self.camera_info)
        if dialog.exec():
            updated = dialog.get_camera_info()
            self.camera_manager.update_camera(self.camera_id, updated)
            self.camera_info = updated
            self.name_label.setText(updated.get('name', 'Camera'))
            # save to disk
            main_win = self.window()
            if hasattr(main_win, 'save_cameras'):
                main_win.save_cameras()

    def remove_camera(self):
        reply = QMessageBox.question(
            self, "Remove Camera",
            f"Remove '{self.camera_info.get('name', 'Camera')}'?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            self.stop_stream()
            self.camera_manager.remove_camera(self.camera_id)
            main_win = self.window()
            if hasattr(main_win, 'save_cameras'):
                main_win.save_cameras()

    # ── Performance ────────────────────────────────────────
    def update_performance_stats(self):
        if not self.is_streaming:
            return

        metrics = self.stream_optimizer.get_performance_metrics()
        target_fps = self.camera_info.get('fps', 30)
        actual_fps = metrics['fps']

        if abs(actual_fps - target_fps) > 5 or metrics.get('latency_ms', 0) > 200:
            buffer_health = metrics.get('buffer_health', 'Unknown')
            perf_text = f"FPS: {actual_fps} | Latency: {metrics.get('latency_ms', 0)}ms | {buffer_health}"
            self.performance_label.setText(perf_text)
            self.performance_label.show()

            if buffer_health == 'Critical':
                self.status_label.setText("Connected - High Latency!")
            elif buffer_health == 'High':
                self.status_label.setText("Connected - Buffering...")
        else:
            self.performance_label.hide()

    def closeEvent(self, event):
        self.stop_stream()
        event.accept()
