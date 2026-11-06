"""
Stream optimization utilities for reducing latency and improving performance.
"""

import cv2
import time
import logging
from PySide6.QtCore import QObject, Signal

logger = logging.getLogger("CCTV_Viewer")


class StreamOptimizer(QObject):
    performance_update = Signal(dict)

    def __init__(self):
        super().__init__()
        self.frame_times = []
        self.last_frame_time = 0
        self.frame_count = 0
        self.dropped_frames = 0

    def optimize_capture_properties(self, cap, url, low_latency_mode=True):
        if not cap or not cap.isOpened():
            return False

        try:
            if low_latency_mode:
                cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
                url_str = str(url) if url is not None else ""

                if 'rtsp://' in url_str.lower():
                    cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('H', '2', '6', '4'))
                    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
                    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
                elif 'http://' in url_str.lower():
                    cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'))
                    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
                    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
                elif _is_usb_camera(url):
                    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
                    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
                    cap.set(cv2.CAP_PROP_FPS, 30)
            else:
                cap.set(cv2.CAP_PROP_BUFFERSIZE, 3)
                cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
                cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

            return True

        except Exception as e:
            logger.error(f"Error optimizing capture: {e}")
            return False

    def should_drop_frame(self, target_fps=30):
        current_time = time.time()

        if self.last_frame_time == 0:
            self.last_frame_time = current_time
            return False

        if (current_time - self.last_frame_time) < (1.0 / target_fps):
            self.dropped_frames += 1
            return True

        self.last_frame_time = current_time
        self.frame_count += 1
        self.frame_times.append(current_time)
        if len(self.frame_times) > 100:
            self.frame_times.pop(0)
        return False

    def get_performance_metrics(self):
        if len(self.frame_times) < 2:
            return {
                'fps': 0,
                'latency_ms': 0,
                'dropped_frames': self.dropped_frames,
                'total_frames': self.frame_count,
                'buffer_health': 'Unknown',
            }

        time_span = self.frame_times[-1] - self.frame_times[0]
        actual_fps = len(self.frame_times) / time_span if time_span > 0 else 0
        avg_interval = time_span / (len(self.frame_times) - 1)
        latency_ms = avg_interval * 1000

        if latency_ms < 100:
            health = 'Good'
        elif latency_ms < 500:
            health = 'High'
        else:
            health = 'Critical'

        return {
            'fps': round(actual_fps, 1),
            'latency_ms': round(latency_ms, 1),
            'dropped_frames': self.dropped_frames,
            'total_frames': self.frame_count,
            'buffer_health': health,
        }

    def reset_metrics(self):
        self.frame_times.clear()
        self.last_frame_time = 0
        self.frame_count = 0
        self.dropped_frames = 0


def _is_usb_camera(url):
    """Check if the URL looks like a USB camera index."""
    if isinstance(url, int):
        return True
    if isinstance(url, str):
        try:
            int(url)
            return True
        except ValueError:
            pass
    return False


class NetworkStreamOptimizer:
    @staticmethod
    def get_rtsp_options():
        return {
            'rtsp_transport': 'tcp',
            'max_delay': '100000',
            'reorder_queue_size': '1',
            'buffer_size': '1024000',
        }

    @staticmethod
    def get_http_options():
        return {
            'timeout': '5000000',
            'reconnect': '1',
            'reconnect_streamed': '1',
            'reconnect_delay_max': '2',
        }

    @staticmethod
    def apply_opencv_optimizations(cap, stream_type='rtsp'):
        if not cap or not cap.isOpened():
            return False
        try:
            if stream_type == 'rtsp':
                cap.set(cv2.CAP_PROP_OPEN_TIMEOUT_MSEC, 5000)
                cap.set(cv2.CAP_PROP_READ_TIMEOUT_MSEC, 5000)
            elif stream_type == 'http':
                cap.set(cv2.CAP_PROP_OPEN_TIMEOUT_MSEC, 3000)
                cap.set(cv2.CAP_PROP_READ_TIMEOUT_MSEC, 3000)
            cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
            return True
        except Exception as e:
            logger.error(f"Error applying OpenCV optimizations: {e}")
            return False
