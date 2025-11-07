#!/usr/bin/env python3
"""
Download the real MobileNet-SSD model files for the Perimeter Intrusion Detection System.
"""

import urllib.request
import os
import sys

def download_file(url, filename, description):
    """Download a file with progress bar."""
    try:
        print(f"Downloading {description}...")
        print(f"URL: {url}")
        
        def show_progress(block_num, block_size, total_size):
            downloaded = block_num * block_size
            if total_size > 0:
                percent = min(100, (downloaded * 100) / total_size)
                sys.stdout.write(f"\rProgress: {percent:.1f}%")
                sys.stdout.flush()
        
        urllib.request.urlretrieve(url, filename, show_progress)
        print(f"\n✓ {description} downloaded successfully")
        
        # Check file size
        file_size = os.path.getsize(filename)
        print(f"File size: {file_size / (1024*1024):.1f} MB")
        
        return True
    except Exception as e:
        print(f"\n✗ Failed to download {description}: {e}")
        return False

def main():
    """Download the model files."""
    print("=" * 60)
    print("MobileNet-SSD Model Downloader")
    print("=" * 60)
    
    # Create models directory
    os.makedirs("models", exist_ok=True)
    
    # Alternative URLs for the model files
    urls = [
        {
            "url": "https://github.com/chuanqi305/MobileNet-SSD/raw/master/MobileNetSSD_deploy.caffemodel",
            "filename": "models/MobileNetSSD_deploy.caffemodel",
            "description": "MobileNet-SSD Caffe Model"
        }
    ]
    
    print("Attempting to download MobileNet-SSD model files...")
    print("Note: The prototxt file is already created.")
    print()
    
    success_count = 0
    
    for item in urls:
        if download_file(item["url"], item["filename"], item["description"]):
            success_count += 1
        print()
    
    print("=" * 60)
    if success_count == len(urls):
        print("🎉 All model files downloaded successfully!")
        print("You can now run the real system with:")
        print("python main.py --video videos/test_video.mp4")
    else:
        print("❌ Some files failed to download.")
        print()
        print("Manual download instructions:")
        print("1. Go to: https://github.com/chuanqi305/MobileNet-SSD")
        print("2. Download 'MobileNetSSD_deploy.caffemodel' (about 23MB)")
        print("3. Place it in the models/ directory")
        print("4. The prototxt file is already created")
    
    print("=" * 60)

if __name__ == "__main__":
    main()
