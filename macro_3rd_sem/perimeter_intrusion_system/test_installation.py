#!/usr/bin/env python3
"""
Test script to verify the Perimeter Intrusion Detection System installation.
"""

import sys
import os
import cv2
import numpy as np

def test_imports():
    """Test if all required packages can be imported."""
    print("Testing package imports...")
    
    try:
        import cv2
        print("✓ OpenCV imported successfully")
    except ImportError as e:
        print(f"✗ OpenCV import failed: {e}")
        return False
    
    try:
        import numpy as np
        print("✓ NumPy imported successfully")
    except ImportError as e:
        print(f"✗ NumPy import failed: {e}")
        return False
    
    try:
        import scipy
        print("✓ SciPy imported successfully")
    except ImportError as e:
        print(f"✗ SciPy import failed: {e}")
        return False
    
    try:
        import imutils
        print("✓ imutils imported successfully")
    except ImportError as e:
        print(f"✗ imutils import failed: {e}")
        return False
    
    return True

def test_opencv_functionality():
    """Test OpenCV basic functionality."""
    print("\nTesting OpenCV functionality...")
    
    try:
        # Test basic image operations
        img = np.zeros((100, 100, 3), dtype=np.uint8)
        cv2.rectangle(img, (10, 10), (90, 90), (0, 255, 0), 2)
        print("✓ OpenCV image operations working")
        
        # Test DNN module
        if hasattr(cv2, 'dnn'):
            print("✓ OpenCV DNN module available")
        else:
            print("✗ OpenCV DNN module not available")
            return False
        
        return True
    except Exception as e:
        print(f"✗ OpenCV functionality test failed: {e}")
        return False

def test_model_files():
    """Test if model files exist."""
    print("\nTesting model files...")
    
    prototxt_path = "models/MobileNetSSD_deploy.prototxt"
    caffemodel_path = "models/MobileNetSSD_deploy.caffemodel"
    
    if os.path.exists(prototxt_path):
        print("✓ Prototxt file found")
    else:
        print("✗ Prototxt file not found")
        print("  Run: python models/download_models.py")
        return False
    
    if os.path.exists(caffemodel_path):
        # Check if it's a real model file (not placeholder)
        file_size = os.path.getsize(caffemodel_path)
        if file_size > 1000000:  # Should be ~23MB
            print("✓ Caffemodel file found and appears valid")
        else:
            print("✗ Caffemodel file appears to be a placeholder")
            print("  Run: python models/download_models.py")
            return False
    else:
        print("✗ Caffemodel file not found")
        print("  Run: python models/download_models.py")
        return False
    
    return True

def test_centroid_tracker():
    """Test the CentroidTracker class."""
    print("\nTesting CentroidTracker...")
    
    try:
        from centroid_tracker import CentroidTracker
        tracker = CentroidTracker()
        
        # Test with sample bounding boxes
        rects = [(100, 100, 200, 200), (300, 300, 400, 400)]
        objects, states = tracker.update(rects)
        
        print("✓ CentroidTracker working correctly")
        return True
    except Exception as e:
        print(f"✗ CentroidTracker test failed: {e}")
        return False

def test_directories():
    """Test if required directories exist."""
    print("\nTesting directory structure...")
    
    required_dirs = ["models", "videos", "snapshots"]
    
    for dir_name in required_dirs:
        if os.path.exists(dir_name):
            print(f"✓ {dir_name}/ directory exists")
        else:
            print(f"✗ {dir_name}/ directory missing")
            return False
    
    return True

def main():
    """Run all tests."""
    print("=" * 60)
    print("Perimeter Intrusion Detection System - Installation Test")
    print("=" * 60)
    
    tests = [
        ("Package Imports", test_imports),
        ("OpenCV Functionality", test_opencv_functionality),
        ("Model Files", test_model_files),
        ("CentroidTracker", test_centroid_tracker),
        ("Directory Structure", test_directories),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n--- {test_name} ---")
        if test_func():
            passed += 1
        else:
            print(f"✗ {test_name} failed")
    
    print("\n" + "=" * 60)
    print(f"Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! The system is ready to use.")
        print("\nNext steps:")
        print("1. Add a video file to the videos/ directory")
        print("2. Run: python main.py --video videos/your_video.mp4")
    else:
        print("❌ Some tests failed. Please fix the issues above.")
        print("\nCommon solutions:")
        print("- Install missing packages: pip install -r requirements.txt")
        print("- Download model files: python models/download_models.py")
        print("- Ensure all directories exist")
    
    print("=" * 60)

if __name__ == "__main__":
    main()
