# 🛡️ Perimeter Intrusion Detection System using Virtual Tripwire  

An intelligent **security surveillance system** that automates the detection of unauthorized entries using **Computer Vision** and **Deep Learning**.  
This project allows users to draw a virtual boundary (tripwire) on live or recorded video, and it automatically detects and alerts when any person or object crosses it — in real time.  

---

## 🚀 Features

- 🧠 Real-time object detection using **MobileNet-SSD**  single shot detector --> identification
- 🎯 Virtual boundary (polygon) drawing with mouse input  
- 🚨 Instant intrusion alerts with red marking  
- 📸 Automatic snapshot and event log saving  
- 📁 Local storage for logs and captured images  
- ⚙️ Modular, object-oriented design for easy customization  
- 🔄 Ready for integration with **YOLO**, **Deep SORT** advanced object tracking algorithm, or web platforms  

---

## 🧩 System Architecture

**Main Modules:**
- **`main.py`** → Runs the complete intrusion detection process  
- **`centroid_tracker.py`** → Tracks objects and maintains IDs using centroid-based logic  
- **`models/`** → Contains the pre-trained **MobileNetSSD** model (`.prototxt` & `.caffemodel`)  
- **`snapshots/`** → Stores intrusion snapshots and logs  
- **`videos/`** → Includes test videos for simulation  
- **`alerts_log.txt`** → Keeps a detailed log of intrusion events  

---

## ⚙️ Installation & Setup

1. **Clone this repository** (or download ZIP):
   ```bash
   git clone https://github.com/your-username/Perimeter_Intrusion_System.git
MACRO_3RD_SEM/
│
├── perimeter_intrusion_system/
│   ├── models/
│   │   ├── MobileNetSSD_deploy.caffemodel
│   │   └── MobileNetSSD_deploy.prototxt
│   ├── videos/
│   │   ├── test_video.mp4
│   │   └── realistic_test_video.mp4
│   ├── snapshots/
│   ├── centroid_tracker.py
│   ├── main.py
│   ├── requirements.txt
│   └── alerts_log.txt
│
└── README.md
