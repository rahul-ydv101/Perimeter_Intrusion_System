#!/usr/bin/env python3
"""
Alternative setup using OpenCV's built-in DNN models for easier installation.
This uses models that are easier to download and set up.
"""

import cv2
import urllib.request
import os

def download_opencv_dnn_models():
    """Download alternative DNN models that work with OpenCV."""
    
    print("Setting up alternative DNN models...")
    
    # Create models directory
    os.makedirs("models", exist_ok=True)
    
    # URLs for alternative models that are easier to download
    models = [
        {
            "url": "https://raw.githubusercontent.com/opencv/opencv/master/samples/dnn/face_detector/opencv_face_detector.pbtxt",
            "filename": "models/opencv_face_detector.pbtxt",
            "description": "OpenCV Face Detector Config"
        },
        {
            "url": "https://raw.githubusercontent.com/opencv/opencv_3rdparty/dnn_samples_face_detector_20170830/opencv_face_detector_uint8.pb",
            "filename": "models/opencv_face_detector_uint8.pb",
            "description": "OpenCV Face Detector Weights"
        }
    ]
    
    success_count = 0
    
    for model in models:
        try:
            print(f"Downloading {model['description']}...")
            urllib.request.urlretrieve(model["url"], model["filename"])
            print(f"✓ {model['description']} downloaded")
            success_count += 1
        except Exception as e:
            print(f"✗ Failed to download {model['description']}: {e}")
    
    return success_count == len(models)

def create_simple_detector():
    """Create a simple person detector using OpenCV's built-in models."""
    
    detector_code = '''
import cv2
import numpy as np
from centroid_tracker import CentroidTracker

class SimplePersonDetector:
    """Simple person detector using OpenCV's built-in models."""
    
    def __init__(self):
        # Use OpenCV's built-in HOG descriptor for person detection
        self.hog = cv2.HOGDescriptor()
        self.hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())
        self.tracker = CentroidTracker()
    
    def detect_people(self, frame):
        """Detect people in the frame using HOG descriptor."""
        # Resize frame for faster processing
        frame_resized = cv2.resize(frame, (640, 480))
        
        # Detect people
        boxes, weights = self.hog.detectMultiScale(
            frame_resized, 
            winStride=(8, 8),
            padding=(32, 32),
            scale=1.05,
            hitThreshold=0.0,
            finalThreshold=2.0,
            useMeanshiftGrouping=False
        )
        
        # Filter detections by weight (confidence)
        detections = []
        for i, (x, y, w, h) in enumerate(boxes):
            if weights[i] > 0.5:  # Confidence threshold
                # Scale back to original frame size
                scale_x = frame.shape[1] / 640
                scale_y = frame.shape[0] / 480
                x = int(x * scale_x)
                y = int(y * scale_y)
                w = int(w * scale_x)
                h = int(h * scale_y)
                detections.append((x, y, x + w, y + h))
        
        return detections

# Usage example:
# detector = SimplePersonDetector()
# boxes = detector.detect_people(frame)
'''
    
    with open("simple_detector.py", "w") as f:
        f.write(detector_code)
    
    print("✓ Created simple_detector.py")

def main():
    """Set up alternative detection system."""
    print("=" * 60)
    print("Alternative Setup for Real Person Detection")
    print("=" * 60)
    
    print("This setup uses OpenCV's built-in HOG descriptor for person detection.")
    print("It doesn't require downloading large model files!")
    print()
    
    # Create the simple detector
    create_simple_detector()
    
    print("✓ Alternative setup complete!")
    print()
    print("To use the real system with this alternative detector:")
    print("1. The simple_detector.py file has been created")
    print("2. You can now modify main.py to use this detector")
    print("3. Or run: python simple_detector.py (if it has a main function)")
    print()
    print("This detector will detect real people in your video!")

if __name__ == "__main__":
    main()
