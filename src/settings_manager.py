import json
import os
from PySide6.QtCore import QSettings

# Resolve config path relative to the project root (parent of src/)
_PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

class SettingsManager:
    def __init__(self):
        self.settings = QSettings("CCTV Solutions", "CCTV Viewer")
        self.config_file = os.path.join(_PROJECT_ROOT, "cameras_config.json")

    # ── Theme ──────────────────────────────────────────────
    def get_theme(self):
        return self.settings.value("appearance/theme", "light")

    def set_theme(self, theme):
        self.settings.setValue("appearance/theme", theme)

    # ── Grid ───────────────────────────────────────────────
    def get_grid_columns(self):
        return int(self.settings.value("display/grid_columns", 3))

    def set_grid_columns(self, columns):
        self.settings.setValue("display/grid_columns", columns)

    # ── Auto-start ─────────────────────────────────────────
    def get_auto_start(self):
        return self.settings.value("general/auto_start", True, type=bool)

    def set_auto_start(self, auto_start):
        self.settings.setValue("general/auto_start", auto_start)

    # ── Network ────────────────────────────────────────────
    def get_reconnect_interval(self):
        return int(self.settings.value("network/reconnect_interval", 5))

    def set_reconnect_interval(self, interval):
        self.settings.setValue("network/reconnect_interval", interval)

    def get_connection_timeout(self):
        return int(self.settings.value("network/connection_timeout", 10))

    def set_connection_timeout(self, timeout):
        self.settings.setValue("network/connection_timeout", timeout)

    def get_max_retries(self):
        return int(self.settings.value("network/max_retries", 3))

    # ── Paths ──────────────────────────────────────────────
    def get_recording_path(self):
        path = self.settings.value("paths/recording", "recordings")
        return self._resolve_path(path)

    def get_snapshot_path(self):
        path = self.settings.value("paths/snapshots", "snapshots")
        return self._resolve_path(path)

    @staticmethod
    def _resolve_path(path):
        if os.path.isabs(path):
            return path
        return os.path.join(_PROJECT_ROOT, path)

    # ── Cameras config ─────────────────────────────────────
    def get_cameras(self):
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, "r", encoding="utf-8") as f:
                    return json.load(f)
            except (json.JSONDecodeError, FileNotFoundError, OSError):
                return []
        return []

    def save_cameras(self, cameras):
        try:
            os.makedirs(os.path.dirname(self.config_file), exist_ok=True)
            with open(self.config_file, "w", encoding="utf-8") as f:
                json.dump(cameras, f, indent=2, ensure_ascii=False)
        except Exception as e:
            logging.getLogger("CCTV_Viewer").error(f"Error saving cameras: {e}")

    # ── Window geometry ────────────────────────────────────
    def get_window_geometry(self):
        return self.settings.value("window/geometry")

    def set_window_geometry(self, geometry):
        self.settings.setValue("window/geometry", geometry)

    def get_window_state(self):
        return self.settings.value("window/state")

    def set_window_state(self, state):
        self.settings.setValue("window/state", state)

    def get_window_maximized(self):
        return self.settings.value("window/maximized", False, type=bool)

    def set_window_maximized(self, maximized):
        self.settings.setValue("window/maximized", maximized)


import logging
