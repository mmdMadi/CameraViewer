import cv2
import os
import datetime
import logging
from PySide6.QtCore import QObject, Signal

logger = logging.getLogger("CCTV_Viewer")

_FORMATS = {
    "JPG": (cv2.IMWRITE_JPEG_QUALITY, 95, ".jpg"),
    "PNG": (cv2.IMWRITE_PNG_COMPRESSION, 3, ".png"),
    "BMP": (None, None, ".bmp"),
}


class SnapshotManager(QObject):
    snapshot_saved = Signal(str)
    error_occurred = Signal(str)

    def __init__(self):
        super().__init__()

    def take_snapshot(self, frame, camera_name, output_dir=None, fmt="JPG"):
        try:
            if frame is None or frame.size == 0:
                self.error_occurred.emit("No frame available for snapshot")
                return None

            if output_dir is None:
                output_dir = "snapshots"
            os.makedirs(output_dir, exist_ok=True)

            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            safe_name = "".join(c for c in camera_name if c.isalnum() or c in (' ', '-', '_')).rstrip()
            _, _, ext = _FORMATS.get(fmt, (None, None, ".jpg"))
            filename = os.path.join(output_dir, f"{safe_name}_{timestamp}{ext}")

            # Apply format-specific encoding
            codec_info = _FORMATS.get(fmt)
            if codec_info and codec_info[0] is not None:
                param = codec_info[0]
                value = codec_info[1]
                success = cv2.imwrite(filename, frame, [param, value])
            else:
                success = cv2.imwrite(filename, frame)

            if success:
                logger.info(f"Snapshot saved: {filename}")
                self.snapshot_saved.emit(filename)
                return filename
            else:
                self.error_occurred.emit("Failed to save snapshot")
                return None

        except Exception as e:
            logger.error(f"Snapshot error: {e}")
            self.error_occurred.emit(f"Snapshot error: {e}")
            return None
