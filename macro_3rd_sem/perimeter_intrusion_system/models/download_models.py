#!/usr/bin/env python3
"""
Script to download MobileNet-SSD model files
"""

import urllib.request
import os

def download_file(url, filename):
    """Download a file from URL"""
    try:
        print(f"Downloading {filename}...")
        urllib.request.urlretrieve(url, filename)
        print(f"✓ {filename} downloaded successfully")
        return True
    except Exception as e:
        print(f"✗ Failed to download {filename}: {e}")
        return False

def main():
    """Download MobileNet-SSD model files"""
    
    # Create models directory if it doesn't exist
    os.makedirs("models", exist_ok=True)
    
    # URLs for the model files
    prototxt_url = "https://raw.githubusercontent.com/chuanqi305/MobileNet-SSD/master/MobileNetSSD_deploy.prototxt"
    caffemodel_url = "https://github.com/chuanqi305/MobileNet-SSD/raw/master/MobileNetSSD_deploy.caffemodel"
    
    # Download files
    prototxt_success = download_file(prototxt_url, "models/MobileNetSSD_deploy.prototxt")
    caffemodel_success = download_file(caffemodel_url, "models/MobileNetSSD_deploy.caffemodel")
    
    if prototxt_success and caffemodel_success:
        print("\n✓ All model files downloaded successfully!")
        print("You can now run the perimeter intrusion detection system.")
    else:
        print("\n✗ Some files failed to download.")
        print("Please download them manually from:")
        print("https://github.com/chuanqi305/MobileNet-SSD")

if __name__ == "__main__":