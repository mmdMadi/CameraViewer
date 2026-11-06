#!/usr/bin/env python3
"""
Simple camera test script to debug streaming issues
"""

import cv2
import sys

def test_camera(url):
    print(f"Testing camera URL: {url}")
    
    try:
        # Try to parse as integer for USB cameras
        try:
            camera_index = int(url)
            cap = cv2.VideoCapture(camera_index)
            print(f"Using USB camera index: {camera_index}")
        except ValueError:
            cap = cv2.VideoCapture(url)
            print(f"Using URL: {url}")
        
        if not cap.isOpened():
            print("ERROR: Could not open camera")
            return False
            
        print("Camera opened successfully")
        
        # Get camera properties
        width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
        height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
        fps = cap.get(cv2.CAP_PROP_FPS)
        
        print(f"Camera properties: {width}x{height} @ {fps} FPS")
        
        # Try to read a frame
        ret, frame = cap.read()
        if ret:
            print(f"Successfully read frame: {frame.shape}")
            print("Frame data type:", frame.dtype)
            print("Frame min/max values:", frame.min(), frame.max())
            
            # Try to save a test image
            cv2.imwrite("test_frame.jpg", frame)
            print("Saved test frame as test_frame.jpg")
            
        else:
            print("ERROR: Could not read frame")
            
        cap.release()
        return ret
        
    except Exception as e:
        print(f"ERROR: {e}")
        return False

if __name__ == "__main__":
    if len(sys.argv) > 1:
        url = sys.argv[1]
    else:
        url = input("Enter camera URL (or USB index like 0): ")
    
    test_camera(url)