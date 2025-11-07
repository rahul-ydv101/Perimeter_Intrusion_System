#!/usr/bin/env python3
"""
Demo mode for Perimeter Intrusion Detection System
This version works without the MobileNet-SSD model files by using simple rectangle detection.
"""

import cv2
import numpy as np
import argparse
import time
from datetime import datetime
from centroid_tracker import CentroidTracker

# Constants
SKIP_FRAMES = 3
DEBOUNCE_FRAMES = 2
COLOR_BLUE = (255, 0, 0)
COLOR_GREEN = (0, 255, 0)
COLOR_RED = (0, 0, 255)
COLOR_WHITE = (255, 255, 255)
COLOR_YELLOW = (0, 255, 255)

class DemoIntrusionDetector:
    """Demo version that works without model files."""
    
    def __init__(self, video_source):
        self.video_source = video_source
        self.cap = None
        self.tracker = CentroidTracker(max_disappeared=50, max_distance=50)
        self.perimeter_points = []
        self.perimeter_defined = False
        self.frame_count = 0
        self.alerts_log = []
        
    def mouse_callback(self, event, x, y, flags, param):
        """Mouse callback for defining perimeter polygon."""
        if event == cv2.EVENT_LBUTTONDOWN:
            self.perimeter_points.append((x, y))
            print(f"Added point: ({x}, {y})")
    
    def define_perimeter(self, frame):
        """Allow user to define the perimeter polygon."""
        cv2.namedWindow("Define Perimeter - Click points, press 'd' when done", cv2.WINDOW_NORMAL)
        cv2.setMouseCallback("Define Perimeter - Click points, press 'd' when done", self.mouse_callback)
        
        while True:
            display_frame = frame.copy()
            
            # Draw existing points and lines
            if len(self.perimeter_points) > 0:
                for i, point in enumerate(self.perimeter_points):
                    cv2.circle(display_frame, point, 5, COLOR_BLUE, -1)
                    cv2.putText(display_frame, f"{i+1}", 
                               (point[0] + 10, point[1] - 10), 
                               cv2.FONT_HERSHEY_SIMPLEX, 0.6, COLOR_WHITE, 2)
                
                if len(self.perimeter_points) > 1:
                    for i in range(len(self.perimeter_points) - 1):
                        cv2.line(display_frame, self.perimeter_points[i], 
                                self.perimeter_points[i+1], COLOR_BLUE, 2)
            
            # Add instructions
            cv2.putText(display_frame, "DEMO MODE - Click points to define perimeter", 
                       (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, COLOR_WHITE, 2)
            cv2.putText(display_frame, "Press 'd' when done, 'r' to reset", 
                       (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, COLOR_WHITE, 2)
            cv2.putText(display_frame, f"Points: {len(self.perimeter_points)}", 
                       (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.7, COLOR_WHITE, 2)
            
            cv2.imshow("Define Perimeter - Click points, press 'd' when done", display_frame)
            
            key = cv2.waitKey(1) & 0xFF
            
            if key == ord('d') and len(self.perimeter_points) >= 3:
                self.perimeter_defined = True
                cv2.destroyWindow("Define Perimeter - Click points, press 'd' when done")
                print(f"✓ Perimeter defined with {len(self.perimeter_points)} points")
                return True
            elif key == ord('r'):
                self.perimeter_points = []
                print("Reset perimeter points")
            elif key == ord('q'):
                cv2.destroyAllWindows()
                return False
        
        return False
    
    def detect_objects_demo(self, frame):
        """Demo object detection - creates moving rectangles."""
        boxes = []
        height, width = frame.shape[:2]
        
        # Create some demo objects that move across the frame
        time_factor = self.frame_count / 300.0  # Assuming 300 frame video
        
        # Object 1: Moving from left to right
        obj1_x = int(50 + (width - 150) * (time_factor % 1.0))
        obj1_y = height // 3
        boxes.append((obj1_x, obj1_y, obj1_x + 40, obj1_y + 80))
        
        # Object 2: Moving in circular pattern
        if self.frame_count > 50:  # Start after some frames
            center_x, center_y = width // 2, height // 2
            radius = 100
            angle = (self.frame_count - 50) * 0.1
            obj2_x = int(center_x + radius * np.cos(angle))
            obj2_y = int(center_y + radius * np.sin(angle))
            boxes.append((obj2_x, obj2_y, obj2_x + 40, obj2_y + 80))
        
        return boxes
    
    def check_perimeter_intrusion(self, centroid):
        """Check if centroid is inside perimeter."""
        if len(self.perimeter_points) < 3:
            return False
        
        polygon = np.array(self.perimeter_points, dtype=np.int32)
        result = cv2.pointPolygonTest(polygon, centroid, False)
        return result >= 0
    
    def draw_perimeter(self, frame):
        """Draw the perimeter polygon."""
        if len(self.perimeter_points) >= 3:
            overlay = frame.copy()
            polygon = np.array(self.perimeter_points, dtype=np.int32)
            
            cv2.fillPoly(overlay, [polygon], COLOR_BLUE)
            cv2.addWeighted(overlay, 0.3, frame, 0.7, 0, frame)
            
            cv2.polylines(frame, [polygon], True, COLOR_BLUE, 3)
            
            for i, point in enumerate(self.perimeter_points):
                cv2.circle(frame, point, 8, COLOR_YELLOW, -1)
                cv2.putText(frame, f"{i+1}", 
                           (point[0] + 12, point[1] - 12), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.6, COLOR_WHITE, 2)
        
        return frame
    
    def draw_objects(self, frame, objects, states):
        """Draw bounding boxes and centroids."""
        for (object_id, centroid) in objects.items():
            state = states.get(object_id, "OUTSIDE")
            color = COLOR_RED if state == "INSIDE" else COLOR_GREEN
            
            cv2.putText(frame, f"ID {object_id}", 
                       (centroid[0] - 10, centroid[1] - 10),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, COLOR_WHITE, 2)
            
            cv2.circle(frame, (centroid[0], centroid[1]), 4, color, -1)
        
        return frame
    
    def process_frame(self, frame):
        """Process frame for demo."""
        self.frame_count += 1
        
        if self.frame_count % SKIP_FRAMES == 0:
            boxes = self.detect_objects_demo(frame)
            objects, states = self.tracker.update(boxes)
            
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            for (object_id, centroid) in objects.items():
                is_inside = self.check_perimeter_intrusion(centroid)
                new_state = "INSIDE" if is_inside else "OUTSIDE"
                old_state = states.get(object_id, "OUTSIDE")
                
                self.tracker.update_state(object_id, new_state)
                frames_since_change = self.tracker.get_state_change_frames(object_id)
                
                if (old_state != new_state and frames_since_change >= DEBOUNCE_FRAMES):
                    if new_state == "INSIDE":
                        alert_msg = f"[ALERT] Object {object_id} ENTERED perimeter at {timestamp}"
                        print(alert_msg)
                        self.alerts_log.append(alert_msg)
                    else:
                        alert_msg = f"[ALERT] Object {object_id} EXITED perimeter at {timestamp}"
                        print(alert_msg)
                        self.alerts_log.append(alert_msg)
        
        objects, states = self.tracker.objects, self.tracker.object_states
        
        frame = self.draw_perimeter(frame)
        frame = self.draw_objects(frame, objects, states)
        
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cv2.putText(frame, f"DEMO MODE - {timestamp}", (10, frame.shape[0] - 20), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, COLOR_WHITE, 2)
        
        status_text = f"Objects: {len(objects)} | Perimeter: {'Defined' if self.perimeter_defined else 'Not Defined'}"
        cv2.putText(frame, status_text, (10, frame.shape[0] - 50), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, COLOR_WHITE, 2)
        
        return frame
    
    def run(self):
        """Main demo loop."""
        try:
            self.cap = cv2.VideoCapture(self.video_source)
            
            if not self.cap.isOpened():
                print(f"✗ Error: Could not open video source: {self.video_source}")
                return
            
            print("✓ Demo mode started")
            print("Instructions:")
            print("- Define perimeter by clicking points")
            print("- Press 'd' when done defining perimeter")
            print("- Press 'q' to quit")
            print("- Press 'r' to reset perimeter")
            
            ret, frame = self.cap.read()
            if not ret:
                print("✗ Error: Could not read first frame")
                return
            
            if not self.define_perimeter(frame):
                print("✗ Perimeter definition cancelled")
                return
            
            print("Starting demo intrusion detection...")
            
            while True:
                ret, frame = self.cap.read()
                if not ret:
                    print("End of video stream")
                    break
                
                processed_frame = self.process_frame(frame)
                cv2.imshow("DEMO: Perimeter Intrusion Detection", processed_frame)
                
                key = cv2.waitKey(30) & 0xFF  # Faster playback for demo
                if key == ord('q'):
                    print("Quitting demo...")
                    break
                elif key == ord('r'):
                    self.perimeter_points = []
                    self.perimeter_defined = False
                    print("Perimeter reset. Please redefine...")
                    if not self.define_perimeter(frame):
                        break
        
        except KeyboardInterrupt:
            print("\nDemo interrupted by user")
        
        except Exception as e:
            print(f"✗ Error during demo: {e}")
        
        finally:
            if self.cap:
                self.cap.release()
            cv2.destroyAllWindows()
            
            print(f"\n=== Demo Summary ===")
            print(f"Total alerts: {len(self.alerts_log)}")
            for alert in self.alerts_log:
                print(alert)

def main():
    """Main demo function."""
    parser = argparse.ArgumentParser(description="Demo Perimeter Intrusion Detection")
    parser.add_argument("--video", type=str, default="videos/test_video.mp4",
                       help="Path to video file")
    
    args = parser.parse_args()
    
    print("=" * 60)
    print("DEMO MODE: Perimeter Intrusion Detection System")
    print("=" * 60)
    print(f"Video source: {args.video}")
    print("This demo works without model files!")
    print("=" * 60)
    
    detector = DemoIntrusionDetector(args.video)
    detector.run()

if __name__ == "__main__":
    main()
