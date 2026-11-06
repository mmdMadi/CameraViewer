import uuid
import logging
from PySide6.QtCore import QObject, Signal


class CameraManager(QObject):
    camera_added = Signal(str, dict)
    camera_removed = Signal(str)
    camera_updated = Signal(str, dict)

    def __init__(self):
        super().__init__()
        self.cameras = {}
        self.camera_widgets = {}

    # ── CRUD ───────────────────────────────────────────────
    def add_camera(self, camera_info, camera_id=None):
        camera_id = camera_id or str(uuid.uuid4())
        self.cameras[camera_id] = camera_info
        self.camera_added.emit(camera_id, camera_info)
        return camera_id

    def remove_camera(self, camera_id):
        if camera_id in self.cameras:
            del self.cameras[camera_id]
            self.camera_removed.emit(camera_id)

    def update_camera(self, camera_id, camera_info):
        if camera_id in self.cameras:
            self.cameras[camera_id] = camera_info
            self.camera_updated.emit(camera_id, camera_info)

    def get_camera(self, camera_id):
        return self.cameras.get(camera_id)

    def get_all_cameras(self):
        """Return list of dicts with both id and info for persistence."""
        result = []
        for cam_id, info in self.cameras.items():
            entry = dict(info)
            entry["id"] = cam_id
            result.append(entry)
        return result

    # ── Widget registry ────────────────────────────────────
    def register_widget(self, camera_id, widget):
        self.camera_widgets[camera_id] = widget

    def unregister_widget(self, camera_id):
        self.camera_widgets.pop(camera_id, None)

    # ── Bulk controls ──────────────────────────────────────
    def start_all(self):
        for widget in self.camera_widgets.values():
            if not widget.is_streaming:
                widget.start_stream()

    def stop_all(self):
        for widget in self.camera_widgets.values():
            if widget.is_streaming:
                widget.stop_stream()

    def is_streaming(self, camera_id):
        w = self.camera_widgets.get(camera_id)
        return w is not None and w.is_streaming
