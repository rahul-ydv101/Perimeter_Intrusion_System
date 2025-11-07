#!/usr/bin/env python3
"""
Perimeter Intrusion Detection System using Virtual Tripwire
Author: Rahul Yadav (GPT-5 Fixed Version)

Detects objects entering a polygonal perimeter drawn by the user.
When intrusion occurs, saves snapshot + logs the event.
"""

import cv2
import numpy as np
import argparse
import os
import time
from centroid_tracker import CentroidTracker

# ============ PARAMETERS ============
CONFIDENCE_THRESHOLD = 0.3
SKIP_FRAMES = 1
DEBOUNCE_FRAMES = 1

# ====================================

class PerimeterIntrusionSystem:
    def __init__(self, video_source):
        self.video_source = video_source
        self.vs = cv2.VideoCapture(video_source)
        self.tracker = CentroidTracker()
        self.polygon = []
        self.drawing = False
        self.frame_count = 0
        self.alert_count = 0
        self.log_file = "alerts_log.txt"
        os.makedirs("snapshots", exist_ok=True)
        self.load_mobilenet_ssd()
        self.state_change_frames = {}  # object_id -> frames since last state change

    def load_mobilenet_ssd(self):
        print("[INFO] Loading MobileNet-SSD model...")
        base_dir = os.path.dirname(os.path.abspath(__file__))
        prototxt_path = os.path.join(base_dir, "models", "MobileNetSSD_deploy.prototxt")
        caffemodel_path = os.path.join(base_dir, "models", "MobileNetSSD_deploy.caffemodel")
        self.net = cv2.dnn.readNetFromCaffe(prototxt_path, caffemodel_path)
        self.CLASSES = ["background", "aeroplane", "bicycle", "bird", "boat",
                        "bottle", "bus", "car", "cat", "chair", "cow", "diningtable",
                        "dog", "horse", "motorbike", "person", "pottedplant", "sheep",
                        "sofa", "train", "tvmonitor"]
        print("[INFO] Model loaded successfully.")

    # Polygon drawing
    def draw_perimeter(self, event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            self.drawing = True
            self.polygon.append((x, y))
        elif event == cv2.EVENT_MOUSEMOVE and self.drawing:
            pass
        elif event == cv2.EVENT_LBUTTONUP:
            self.drawing = False

    def detect_objects(self, frame):
        (h, w) = frame.shape[:2]
        blob = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)), 0.007843,
                                     (300, 300), 127.5)
        self.net.setInput(blob)
        detections = self.net.forward()

        rects = []
        for i in np.arange(0, detections.shape[2]):
            confidence = detections[0, 0, i, 2]
            if confidence > CONFIDENCE_THRESHOLD:
                idx = int(detections[0, 0, i, 1])
                if self.CLASSES[idx] != "person":
                    continue
                box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
                (startX, startY, endX, endY) = box.astype("int")
                rects.append((startX, startY, endX, endY))
        return rects

    def check_perimeter_intrusion(self, point):
        if len(self.polygon) < 3:
            return False
        pt = (int(point[0]), int(point[1]))  # Ensure tuple of ints
        result = cv2.pointPolygonTest(np.array(self.polygon, np.int32), pt, False)
        return result >= 0  # True if inside or on boundary

    def log_alert(self, object_id, timestamp):
        with open(self.log_file, "a") as f:
            f.write(f"[ALERT] Object {object_id} ENTERED perimeter at {timestamp}\n")
        print(f"[ALERT] Object {object_id} ENTERED perimeter at {timestamp}")

    def save_alert_snapshot(self, frame, object_id):
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        filename = f"snapshots/intrusion_obj_{object_id}_{timestamp}.jpg"
        cv2.imwrite(filename, frame)
        print(f"[SNAPSHOT] Saved: {filename}")

    def process_frame(self, frame):
        self.frame_count += 1
        if self.frame_count % SKIP_FRAMES != 0:
            return frame

        rects = self.detect_objects(frame)
        objects = self.tracker.update(rects)
        states = self.tracker.get_states()

        # Show perimeter warning if not set
        if len(self.polygon) < 3:
            cv2.putText(frame, 'PERIMETER NOT SET!', (30, 80), cv2.FONT_HERSHEY_SIMPLEX, 2.0, (0,0,255), 6, cv2.LINE_AA)
            return frame

        # Store rects by index for drawing (approximate matching)
        rects_by_index = {}
        if len(rects) > 0:
            for idx, rect in enumerate(rects):
                if idx < len(list(objects.keys())):
                    obj_id = list(objects.keys())[idx]
                    rects_by_index[obj_id] = rect

        for (object_id, centroid) in objects.items():
            is_inside = self.check_perimeter_intrusion(centroid)
            old_state = states.get(object_id, "OUTSIDE")
            new_state = "INSIDE" if is_inside else "OUTSIDE"
            self.tracker.update_state(object_id, new_state)

            # Track state change frame counts for debounce
            if object_id not in self.state_change_frames:
                self.state_change_frames[object_id] = 0
            
            # Check if state changed
            state_changed = (old_state != new_state)
            
            if state_changed:
                self.state_change_frames[object_id] = 0  # Reset on state change
            else:
                self.state_change_frames[object_id] += 1  # Increment if same state

            # Debug line (leave visible)
            print(f"Object {object_id}: old={old_state}, new={new_state}, point={centroid}, frames_since_change={self.state_change_frames[object_id]}")

            # Alert and snapshot when person enters perimeter
            # Trigger when state changes from OUTSIDE to INSIDE
            if state_changed and new_state == "INSIDE":
                timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
                self.alert_count += 1
                self.log_alert(object_id, timestamp)
                self.save_alert_snapshot(frame, object_id)

            # Draw bounding box - use stored rect or draw around centroid
            color = (0, 255, 0) if new_state == "OUTSIDE" else (0, 0, 255)
            if object_id in rects_by_index:
                (startX, startY, endX, endY) = rects_by_index[object_id]
                cv2.rectangle(frame, (startX, startY), (endX, endY), color, 4)
            else:
                # Fallback: draw box around centroid
                box_size = 80
                cv2.rectangle(frame, 
                            (centroid[0] - box_size, centroid[1] - box_size),
                            (centroid[0] + box_size, centroid[1] + box_size), 
                            color, 4)

            # Draw circle for centroid, larger
            cv2.circle(frame, tuple(centroid), 10, color, -1)

            # Draw ID and big state label
            cv2.putText(frame, f"ID {object_id}", (centroid[0] - 10, centroid[1] - 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.9, color, 2)
            state_text = new_state
            text_color = (0,255,0) if new_state=="OUTSIDE" else (0,0,255)
            cv2.putText(frame, state_text, (centroid[0] - 10, centroid[1] + 40), 
                        cv2.FONT_HERSHEY_SIMPLEX, 1.1, text_color, 5)

        if len(self.polygon) >= 3:
            cv2.polylines(frame, [np.array(self.polygon, np.int32)], True, (255, 255, 0), 5)

        cv2.putText(frame, f"Alerts: {self.alert_count}", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        return frame

    def run(self):
        cv2.namedWindow("Perimeter Intrusion System")
        cv2.setMouseCallback("Perimeter Intrusion System", self.draw_perimeter)

        # Try to open the video/camera source, fail gracefully
        if not self.vs.isOpened():
            print("[ERROR] Could not open video source!")
            print("Tip: Try running with a video file, e.g. python main.py --video videos/test_video.mp4")
            blank = np.zeros((380, 640, 3), np.uint8)
            cv2.putText(blank, "VIDEO SOURCE ERROR", (40, 140), cv2.FONT_HERSHEY_SIMPLEX, 1.3, (0, 0, 255), 2)
            cv2.putText(blank, "Check webcam or use: python main.py --video filename.mp4", (10, 200), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)
            cv2.imshow("Perimeter Intrusion System", blank)
            cv2.waitKey(3000)
            cv2.destroyAllWindows()
            return

        print("============================================================")
        print("Perimeter Intrusion Detection System")
        print("============================================================")
        print("Left-click to draw polygon perimeter. Press 'd' for done, 'r' to reset, 'q' to quit.\n")

        background_frame = None
        try:
            while True:
                ret, frame = self.vs.read()
                if not ret:
                    break
                display = frame.copy()
                background_frame = frame.copy()

                if len(self.polygon) > 1:
                    cv2.polylines(display, [np.array(self.polygon, np.int32)], True, (255, 0, 0), 2)
                # Large, clear yellow instructions
                cv2.rectangle(display, (0,0),(display.shape[1],55),(0,0,0),-1)
                cv2.putText(display, "Draw perimeter: left-click = add point | d = done | r = reset | q = quit", (12, 40),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.93, (0, 255, 255), 3, cv2.LINE_AA)
                cv2.imshow("Perimeter Intrusion System", display)
                key = cv2.waitKey(1) & 0xFF
                if key == ord('d'):
                    print("[INFO] Perimeter defined. Saving background image and starting detection...")
                    if background_frame is not None:
                        cv2.imwrite("background.jpg", background_frame)
                        print("[INFO] Background image saved as background.jpg")
                    break
                elif key == ord('r'):
                    print("[INFO] Resetting perimeter definition.")
                    self.polygon = []
                elif key == ord('q') or cv2.getWindowProperty("Perimeter Intrusion System", cv2.WND_PROP_VISIBLE) < 1:
                    print("[INFO] Quit during perimeter definition.")
                    self.vs.release()
                    cv2.destroyAllWindows()
                    return
            # Detection mode banner
            detection_mode_banner = True
            while True:
                ret, frame = self.vs.read()
                if not ret:
                    break
                frame = self.process_frame(frame)
                if detection_mode_banner:
                    cv2.rectangle(frame,(0,0),(frame.shape[1],48),(0,0,0),-1)
                    cv2.putText(frame, "DETECTION MODE: Press q to quit", (12,36), 
                        cv2.FONT_HERSHEY_SIMPLEX, 1.03, (0,255,0), 3, cv2.LINE_AA)
                    detection_mode_banner = False
                cv2.imshow("Perimeter Intrusion System", frame)
                k = cv2.waitKey(1) & 0xFF
                if k == ord('q') or cv2.getWindowProperty("Perimeter Intrusion System", cv2.WND_PROP_VISIBLE) < 1:
                    break
        finally:
            print(f"\nTotal alerts: {self.alert_count}")
            print(f"Alerts logged to: {self.log_file}")
            print("Snapshots saved to: snapshots/ directory")
            self.vs.release()
            cv2.destroyAllWindows()

# ================= MAIN ==================
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--video", type=str, default="0", help="Path to video file or 0 for webcam")
    args = parser.parse_args()

    video_source = 0 if args.video == "0" else args.video
    system = PerimeterIntrusionSystem(video_source)
    system.run()
