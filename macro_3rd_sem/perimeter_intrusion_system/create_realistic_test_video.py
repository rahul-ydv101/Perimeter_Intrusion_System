#!/usr/bin/env python3
"""
Create a more realistic test video that will trigger person detection.
"""

import cv2
import numpy as np
import os

def create_realistic_test_video():
    """Create a test video with more realistic person-like shapes."""
    
    # Video parameters
    width, height = 800, 600
    fps = 30
    duration = 15  # seconds
    total_frames = fps * duration
    
    # Create output directory
    os.makedirs("videos", exist_ok=True)
    
    # Define video writer
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter('videos/realistic_test_video.mp4', fourcc, fps, (width, height))
    
    print(f"Creating realistic test video: {total_frames} frames at {fps} FPS")
    
    for frame_num in range(total_frames):
        # Create blank frame with background
        frame = np.ones((height, width, 3), dtype=np.uint8) * 50  # Dark gray background
        
        # Add some texture to make it look more realistic
        for i in range(0, width, 100):
            cv2.line(frame, (i, 0), (i, height), (80, 80, 80), 1)
        for i in range(0, height, 100):
            cv2.line(frame, (0, i), (width, i), (80, 80, 80), 1)
        
        # Create more realistic person-like objects
        time_factor = frame_num / total_frames
        
        # Person 1: Walking from left to right with realistic proportions
        obj1_x = int(50 + (width - 200) * (time_factor % 1.0))
        obj1_y = height // 3
        
        # Draw person-like shape with head, body, arms, legs
        # Head (circle)
        cv2.circle(frame, (obj1_x + 20, obj1_y), 15, (220, 180, 140), -1)  # Skin color
        cv2.circle(frame, (obj1_x + 17, obj1_y - 3), 3, (0, 0, 0), -1)  # Left eye
        cv2.circle(frame, (obj1_x + 23, obj1_y - 3), 3, (0, 0, 0), -1)  # Right eye
        
        # Body (rectangle)
        cv2.rectangle(frame, (obj1_x + 10, obj1_y + 15), (obj1_x + 30, obj1_y + 70), (100, 150, 200), -1)  # Blue shirt
        
        # Arms (horizontal rectangles)
        cv2.rectangle(frame, (obj1_x, obj1_y + 25), (obj1_x + 10, obj1_y + 35), (220, 180, 140), -1)  # Left arm
        cv2.rectangle(frame, (obj1_x + 30, obj1_y + 25), (obj1_x + 40, obj1_y + 35), (220, 180, 140), -1)  # Right arm
        
        # Legs (vertical rectangles)
        cv2.rectangle(frame, (obj1_x + 12, obj1_y + 70), (obj1_x + 18, obj1_y + 110), (50, 50, 50), -1)  # Left leg
        cv2.rectangle(frame, (obj1_x + 22, obj1_y + 70), (obj1_x + 28, obj1_y + 110), (50, 50, 50), -1)  # Right leg
        
        # Person 2: Walking in a different pattern (appears later)
        if frame_num > 100:
            late_time = (frame_num - 100) / (total_frames - 100)
            obj2_x = int(width - 100 - (width - 250) * late_time)
            obj2_y = 2 * height // 3
            
            # Draw second person
            cv2.circle(frame, (obj2_x + 20, obj2_y), 15, (200, 160, 120), -1)  # Head
            cv2.circle(frame, (obj2_x + 17, obj2_y - 3), 3, (0, 0, 0), -1)  # Left eye
            cv2.circle(frame, (obj2_x + 23, obj2_y - 3), 3, (0, 0, 0), -1)  # Right eye
            cv2.rectangle(frame, (obj2_x + 10, obj2_y + 15), (obj2_x + 30, obj2_y + 70), (150, 100, 100), -1)  # Red shirt
            cv2.rectangle(frame, (obj2_x, obj2_y + 25), (obj2_x + 10, obj2_y + 35), (200, 160, 120), -1)  # Left arm
            cv2.rectangle(frame, (obj2_x + 30, obj2_y + 25), (obj2_x + 40, obj2_y + 35), (200, 160, 120), -1)  # Right arm
            cv2.rectangle(frame, (obj2_x + 12, obj2_y + 70), (obj2_x + 18, obj2_y + 110), (30, 30, 30), -1)  # Left leg
            cv2.rectangle(frame, (obj2_x + 22, obj2_y + 70), (obj2_x + 28, obj2_y + 110), (30, 30, 30), -1)  # Right leg
        
        # Person 3: Standing still in the center (for testing)
        if frame_num > 200:
            obj3_x = width // 2
            obj3_y = height // 2
            
            # Draw third person
            cv2.circle(frame, (obj3_x + 20, obj3_y), 15, (180, 140, 100), -1)  # Head
            cv2.circle(frame, (obj3_x + 17, obj3_y - 3), 3, (0, 0, 0), -1)  # Left eye
            cv2.circle(frame, (obj3_x + 23, obj3_y - 3), 3, (0, 0, 0), -1)  # Right eye
            cv2.rectangle(frame, (obj3_x + 10, obj3_y + 15), (obj3_x + 30, obj3_y + 70), (100, 200, 100), -1)  # Green shirt
            cv2.rectangle(frame, (obj3_x, obj3_y + 25), (obj3_x + 10, obj3_y + 35), (180, 140, 100), -1)  # Left arm
            cv2.rectangle(frame, (obj3_x + 30, obj3_y + 25), (obj3_x + 40, obj3_y + 35), (180, 140, 100), -1)  # Right arm
            cv2.rectangle(frame, (obj3_x + 12, obj3_y + 70), (obj3_x + 18, obj3_y + 110), (40, 40, 40), -1)  # Left leg
            cv2.rectangle(frame, (obj3_x + 22, obj3_y + 70), (obj3_x + 28, obj3_y + 110), (40, 40, 40), -1)  # Right leg
        
        # Add frame number and instructions
        cv2.putText(frame, f"Frame: {frame_num}/{total_frames}", 
                   (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        
        timestamp = f"Time: {frame_num/fps:.1f}s"
        cv2.putText(frame, timestamp, (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        
        cv2.putText(frame, "Realistic Test Video for Person Detection", 
                   (10, height - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
        
        # Write frame
        out.write(frame)
        
        # Show progress
        if frame_num % 50 == 0:
            progress = (frame_num / total_frames) * 100
            print(f"Progress: {progress:.1f}%")
    
    # Release video writer
    out.release()
    
    print("✓ Realistic test video created successfully!")
    print("File: videos/realistic_test_video.mp4")
    print("\nThis video contains person-like shapes that should trigger detection!")
    print("To test: python main.py --video videos/realistic_test_video.mp4")
    
    return True

if __name__ == "__main__":
    create_realistic_test_video()
