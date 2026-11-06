import cv2
import os
import shutil
import datetime
import logging
from PySide6.QtCore import QObject, QThread, Signal

logger = logging.getLogger("CCTV_Viewer")

# Minimum free disk space in MB before refusing to record
_MIN_DISK_MB = 500

# Supported formats -> fourcc + extension
_FORMATS = {
    "MP4": ("mp4v", "mp4"),
    "AVI": ("XVID", "avi"),
    "MOV": ("mp4v", "mov"),
    "MKV": ("mp4v", "mkv"),
}


class VideoRecorder(QThread):
    recording_started = Signal(str)
    recording_stopped = Signal()
    error_occurred = Signal(str)

    def __init__(self, camera_name, fps=30, output_dir="recordings", fmt="MP4"):
        super().__init__()
        self.camera_name = camera_name
        self.fps = fps
        self.output_dir = output_dir
        self.fmt = fmt
        self.recording = False
        self.frames_queue = []
        self.video_writer = None
        self.filename = ""

    def start_recording(self):
        if self.recording:
            return

        os.makedirs(self.output_dir, exist_ok=True)

        # Disk space check
        try:
            usage = shutil.disk_usage(self.output_dir)
            free_mb = usage.free // (1024 * 1024)
            if free_mb < _MIN_DISK_MB:
                self.error_occurred.emit(f"Low disk space ({free_mb} MB free). Need at least {_MIN_DISK_MB} MB.")
                return
        except OSError:
            pass  # proceed if check fails

        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_name = "".join(c for c in self.camera_name if c.isalnum() or c in (' ', '-', '_')).rstrip()
        _, ext = _FORMATS.get(self.fmt, ("mp4v", "mp4"))
        self.filename = os.path.join(self.output_dir, f"{safe_name}_{timestamp}.{ext}")

        self.recording = True
        self.start()

    def stop_recording(self):
        self.recording = False
        self.wait(5000)

    def add_frame(self, frame):
        if self.recording and frame is not None:
            self.frames_queue.append(frame.copy())

    def run(self):
        video_writer = None
        try:
            fourcc_str, _ = _FORMATS.get(self.fmt, ("mp4v", "mp4"))
            fourcc = cv2.VideoWriter_fourcc(*fourcc_str)
            frame_size = None

            self.recording_started.emit(self.filename)

            while self.recording or self.frames_queue:
                if self.frames_queue:
                    frame = self.frames_queue.pop(0)

                    if frame_size is None:
                        frame_size = (frame.shape[1], frame.shape[0])
                        video_writer = cv2.VideoWriter(self.filename, fourcc, self.fps, frame_size)

                    if video_writer and video_writer.isOpened():
                        video_writer.write(frame)
                else:
                    self.msleep(10)

        except Exception as e:
            logger.error(f"Recording error: {e}")
            self.error_occurred.emit(f"Recording error: {e}")
        finally:
            if video_writer:
                video_writer.release()
            self.recording_stopped.emit()


class RecordingManager(QObject):
    def __init__(self):
        super().__init__()
        self.active_recordings = {}

    def start_recording(self, camera_id, camera_name, fps=30, output_dir=None, fmt="MP4"):
        if camera_id in self.active_recordings:
            return None
        if output_dir is None:
            output_dir = "recordings"
        recorder = VideoRecorder(camera_name, fps, output_dir, fmt)
        self.active_recordings[camera_id] = recorder
        recorder.start_recording()
        return recorder

    def stop_recording(self, camera_id):
        recorder = self.active_recordings.pop(camera_id, None)
        if recorder:
            recorder.stop_recording()

    def add_frame(self, camera_id, frame):
        recorder = self.active_recordings.get(camera_id)
        if recorder:
            recorder.add_frame(frame)

    def is_recording(self, camera_id):
        return camera_id in self.active_recordings

    def stop_all_recordings(self):
        for cam_id in list(self.active_recordings.keys()):
            self.stop_recording(cam_id)
