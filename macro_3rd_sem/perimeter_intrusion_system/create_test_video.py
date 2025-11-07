#!/usr/bin/env python3
"""
Create a simple test video for the Perimeter Intrusion Detection System.
This script generates a synthetic video with moving rectangles to test the system.
"""

import cv2
import numpy as np
import os

def create_test_video():
    """Create a test video with moving objects."""
    
    # Video parameters
    width, height = 800, 600
    fps = 30
    duration = 10  # seconds
    total_frames = fps * duration
    
    # Create output directory
    os.makedirs("videos", exist_ok=True)
    
    # Define video writer
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter('videos/test_video.mp4', fourcc, fps, (width, height))
    
    print(f"Creating test video: {total_frames} frames at {fps} FPS")
    
    for frame_num in range(total_frames):
        # Create blank frame
        frame = np.zeros((height, width, 3), dtype=np.uint8)
        
        # Add background pattern
        for i in range(0, width, 50):
            cv2.line(frame, (i, 0), (i, height), (20, 20, 20), 1)
        for i in range(0, height, 50):
            cv2.line(frame, (0, i), (width, i), (20, 20, 20), 1)
        
        # Create moving objects (simulating people)
        time_factor = frame_num / total_frames
        
        # Object 1: Moving from left to right
        obj1_x = int(50 + (width - 150) * time_factor)
        obj1_y = height // 3
        cv2.rectangle(frame, (obj1_x, obj1_y), (obj1_x + 40, obj1_y + 80), (0, 255, 0), -1)
        cv2.circle(frame, (obj1_x + 20, obj1_y + 20), 10, (255, 255, 255), -1)  # head
        
        # Object 2: Moving in a circular path
        center_x, center_y = width // 2, height // 2
        radius = 100
        angle = time_factor * 4 * np.pi
        obj2_x = int(center_x + radius * np.cos(angle))
        obj2_y = int(center_y + radius * np.sin(angle))
        cv2.rectangle(frame, (obj2_x, obj2_y), (obj2_x + 40, obj2_y + 80), (0, 0, 255), -1)
        cv2.circle(frame, (obj2_x + 20, obj2_y + 20), 10, (255, 255, 255), -1)  # head
        
        # Object 3: Moving from right to left (appears later)
        if frame_num > total_frames // 2:
            late_time = (frame_num - total_frames // 2) / (total_frames // 2)
            obj3_x = int(width - 50 - (width - 150) * late_time)
            obj3_y = 2 * height // 3
            cv2.rectangle(frame, (obj3_x, obj3_y), (obj3_x + 40, obj3_y + 80), (255, 0, 0), -1)
            cv2.circle(frame, (obj3_x + 20, obj3_y + 20), 10, (255, 255, 255), -1)  # head
        
        # Add frame number
        cv2.putText(frame, f"Frame: {frame_num}/{total_frames}", 
                   (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        
        # Add timestamp
        timestamp = f"Time: {frame_num/fps:.1f}s"
        cv2.putText(frame, timestamp, (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        
        # Add instructions
        cv2.putText(frame, "Test Video for Perimeter Intrusion Detection", 
                   (10, height - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
        
        # Write frame
        out.write(frame)
        
        # Show progress
        if frame_num % 30 == 0:
            progress = (frame_num / total_frames) * 100
            print(f"Progress: {progress:.1f}%")
    
    # Release video writer
    out.release()
    
    print("✓ Test video created successfully!")
    print("File: videos/test_video.mp4")
    print("\nTo test the system:")
    print("python main.py --video videos/test_video.mp4")
    
    return True

if __name__ == "__main__":
    create_test_video()
