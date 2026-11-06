import math
from PySide6.QtWidgets import (QWidget, QGridLayout, QScrollArea,
                               QVBoxLayout, QLabel, QPushButton)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont

from .camera_widget import CameraWidget


class CameraGrid(QWidget):
    def __init__(self, camera_manager, main_window=None):
        super().__init__()
        self.camera_manager = camera_manager
        self.main_window = main_window
        self.camera_widgets = {}

        self.setup_ui()

        self.camera_manager.camera_added.connect(self.add_camera_widget)
        self.camera_manager.camera_removed.connect(self.remove_camera_widget)

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)

        self.grid_widget = QWidget()
        self.grid_layout = QGridLayout(self.grid_widget)
        self.grid_layout.setSpacing(5)

        self.scroll_area.setWidget(self.grid_widget)
        layout.addWidget(self.scroll_area)

        self.show_empty_state()

    # ── Empty state ────────────────────────────────────────
    def show_empty_state(self):
        if self.camera_widgets:
            return
        empty_widget = QWidget()
        empty_layout = QVBoxLayout(empty_widget)
        empty_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        empty_label = QLabel("No cameras added yet")
        empty_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        font = QFont()
        font.setPointSize(16)
        font.setBold(True)
        empty_label.setFont(font)
        empty_label.setStyleSheet("color: #888888;")

        add_button = QPushButton("Add Your First Camera")
        add_button.setMinimumSize(200, 40)
        if self.main_window:
            add_button.clicked.connect(self.main_window.add_camera)

        empty_layout.addWidget(empty_label)
        empty_layout.addWidget(add_button)

        self.clear_grid()
        self.grid_layout.addWidget(empty_widget, 0, 0)

    # ── Grid helpers ───────────────────────────────────────
    def clear_grid(self):
        while self.grid_layout.count():
            item = self.grid_layout.takeAt(0)
            widget = item.widget()
            if widget:
                if isinstance(widget, CameraWidget):
                    # keep alive in dict, just remove from layout
                    continue
                widget.deleteLater()

    def add_camera_widget(self, camera_id, camera_info):
        if camera_id not in self.camera_widgets:
            widget = CameraWidget(camera_id, camera_info, self.camera_manager)
            self.camera_widgets[camera_id] = widget
            self.camera_manager.register_widget(camera_id, widget)
            self.refresh_grid()

    def remove_camera_widget(self, camera_id):
        widget = self.camera_widgets.pop(camera_id, None)
        if widget:
            self.camera_manager.unregister_widget(camera_id)
            widget.stop_stream()
            widget.deleteLater()
            self.refresh_grid()

    def refresh_grid(self):
        if not self.camera_widgets:
            self.clear_grid()
            self.show_empty_state()
            return

        self.clear_grid()

        columns = self._get_grid_columns()
        widgets = list(self.camera_widgets.values())

        for idx, cam_widget in enumerate(widgets):
            row = idx // columns
            col = idx % columns
            self.grid_layout.addWidget(cam_widget, row, col)

        # stretch last row / last column so widgets expand
        last_row = (len(widgets) - 1) // columns
        self.grid_layout.setRowStretch(last_row + 1, 1)
        self.grid_layout.setColumnStretch(columns, 1)

    def _get_grid_columns(self):
        if self.main_window:
            return self.main_window.settings_manager.get_grid_columns()
        return 3

    def set_grid_columns(self, columns):
        self.refresh_grid()
