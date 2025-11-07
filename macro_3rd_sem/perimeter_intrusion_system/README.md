# Perimeter Intrusion Detection System using Virtual Tripwire

A complete Python-based computer vision system that detects intrusions in video streams using OpenCV and MobileNet-SSD. The system allows users to define a virtual perimeter (polygon) and detects when persons or objects enter or exit that defined area.

## 🎯 Features

- **Real-time Object Detection**: Uses MobileNet-SSD for efficient person detection
- **Virtual Tripwire**: Define custom perimeter polygons by clicking points
- **Object Tracking**: Centroid-based tracking with unique ID assignment
- **Intrusion Detection**: Automatic detection of objects entering/exiting perimeter
- **Visual Alerts**: Color-coded bounding boxes (green=outside, red=inside)
- **Snapshot Capture**: Automatic saving of intrusion snapshots
- **Comprehensive Logging**: Console alerts and log file generation
- **Multiple Input Sources**: Support for video files and webcam

## 🏗️ Project Structure

```
perimeter_intrusion_system/
├── main.py                          # Main application file
├── centroid_tracker.py              # Object tracking implementation
├── models/
│   ├── MobileNetSSD_deploy.prototxt # Neural network architecture
│   ├── MobileNetSSD_deploy.caffemodel # Pre-trained weights
│   └── download_models.py           # Script to download model files
├── videos/
│   └── input_video.mp4              # Sample input video (add your own)
├── snapshots/                       # Directory for intrusion snapshots
├── README.md                        # This file
└── requirements.txt                 # Python dependencies
```

## 🚀 Quick Start

### 1. Installation

Clone or download this project, then install dependencies:

```bash
cd perimeter_intrusion_system
pip install -r requirements.txt
```

### 2. Download Model Files

The MobileNet-SSD model files are required for object detection. Download them using:

```bash
python models/download_models.py
```

**Note**: If the automatic download fails, manually download from:
- [MobileNetSSD_deploy.prototxt](https://github.com/chuanqi305/MobileNet-SSD/blob/master/MobileNetSSD_deploy.prototxt)
- [MobileNetSSD_deploy.caffemodel](https://github.com/chuanqi305/MobileNet-SSD/raw/master/MobileNetSSD_deploy.caffemodel)

Place both files in the `models/` directory.

### 3. Add Your Video

Place your video file in the `videos/` directory, or use your webcam.

### 4. Run the System

```bash
# Using a video file
python main.py --video videos/your_video.mp4

# Using webcam
python main.py --video 0

# Using default video (videos/input_video.mp4)
python main.py
```

## 🎮 Usage Instructions

### 1. Define Perimeter
- When the system starts, click points on the video to define your perimeter polygon
- The perimeter will be drawn as a blue polygon with numbered points
- Press `d` when you're done defining the perimeter
- Press `r` to reset and start over

### 2. Monitor Intrusions
- The system will automatically detect persons in the video
- Green bounding boxes indicate objects outside the perimeter
- Red bounding boxes indicate objects inside the perimeter
- Object IDs are displayed above each bounding box
- Centroids are marked with colored circles

### 3. Controls
- `d`: Finish defining perimeter
- `r`: Reset perimeter points
- `q`: Quit the application

### 4. Outputs
- **Console Alerts**: Real-time intrusion notifications
- **Snapshots**: Saved in `snapshots/` directory with timestamps
- **Log File**: `alerts_log.txt` with all intrusion events

## 📊 Example Output

### Console Output
```
✓ Model loaded successfully
✓ Video source opened successfully
Added point: (100, 150)
Added point: (300, 150)
Added point: (300, 300)
Added point: (100, 300)
✓ Perimeter defined with 4 points
Starting intrusion detection...
[ALERT] Object 1 ENTERED perimeter at 2025-01-14 10:30:15
✓ Snapshot saved: snapshots/intrusion_obj_1_20250114_103015.jpg
[ALERT] Object 1 EXITED perimeter at 2025-01-14 10:30:45
```

### Visual Interface
- Blue polygon showing the defined perimeter
- Green/red bounding boxes around detected objects
- Object IDs displayed above each box
- Timestamp in bottom-left corner
- Status information in bottom-right corner

## ⚙️ Configuration

### Key Parameters (in main.py)

```python
CONFIDENCE_THRESHOLD = 0.5    # Minimum confidence for detection
SKIP_FRAMES = 3               # Process every nth frame
DEBOUNCE_FRAMES = 2           # Frames to wait before confirming state change
PERSON_CLASS_ID = 15          # COCO dataset class ID for person
```

### Tracker Parameters (in centroid_tracker.py)

```python
max_disappeared = 50          # Max frames object can be missing
max_distance = 50             # Max distance to associate objects
```

## 🔧 Dependencies

- **opencv-python**: Computer vision library
- **numpy**: Numerical computing
- **imutils**: OpenCV convenience functions
- **scipy**: Scientific computing (for distance calculations)
- **playsound**: Audio alerts (optional)

## 🎥 Supported Input Sources

- **Video Files**: MP4, AVI, MOV, etc.
- **Webcam**: Real-time camera input (index 0)
- **Network Streams**: RTSP, HTTP streams (with proper URL)

## 📈 Performance Optimization

- **Frame Skipping**: Processes every 3rd frame by default
- **Confidence Filtering**: Only detects high-confidence objects
- **Debouncing**: Prevents flickering alerts
- **Efficient Tracking**: Centroid-based tracking reduces computational load

## 🐛 Troubleshooting

### Common Issues

1. **Model Loading Error**
   ```
   ✗ Error loading model: [Errno 2] No such file or directory
   ```
   **Solution**: Download the model files using `python models/download_models.py`

2. **Video Not Found**
   ```
   ✗ Error: Could not open video source: videos/input_video.mp4
   ```
   **Solution**: Ensure your video file exists in the `videos/` directory

3. **Webcam Access Denied**
   ```
   ✗ Error: Could not open video source: 0
   ```
   **Solution**: Check camera permissions or try a different camera index

4. **Low Detection Accuracy**
   **Solutions**: 
   - Adjust `CONFIDENCE_THRESHOLD` (lower = more detections)
   - Ensure good lighting and clear view
   - Use higher resolution videos

### Performance Issues

- **Slow Processing**: Increase `SKIP_FRAMES` value
- **Memory Usage**: Process smaller video segments
- **CPU Usage**: Lower video resolution or use GPU acceleration

## 🔮 Future Enhancements

- **Advanced Tracking**: YOLOv8 + Deep SORT integration
- **Multiple Perimeters**: Support for multiple detection zones
- **Real-time Alerts**: Email/SMS notifications via Twilio
- **GUI Interface**: User-friendly graphical interface
- **Database Integration**: Store logs in SQLite/PostgreSQL
- **Multi-camera Support**: Simultaneous multiple video streams
- **Object Classification**: Detect vehicles, animals, etc.
- **Motion Analysis**: Background subtraction for better detection
- **Cloud Integration**: Upload alerts to cloud services
- **Mobile App**: Remote monitoring via mobile application

## 📝 License

This project is open source and available under the MIT License.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues for bugs and feature requests.

## 📞 Support

For support, please open an issue in the project repository or contact the development team.

---

**Note**: This system is designed for educational and research purposes. For production use in security applications, additional testing and validation are recommended.
