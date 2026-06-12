# Virtual Mouse & Virtual Painter 🖱️🎨

A Python-based computer vision project that uses hand gesture recognition to control your computer as a virtual mouse and create digital paintings using hand movements. Built with OpenCV and MediaPipe for real-time hand tracking.

## Features ✨

### Virtual Mouse Mode
- **Hand Tracking**: Real-time detection and tracking of hand landmarks using MediaPipe
- **Gesture Controls**: 
  - 1 finger (index): Move mouse cursor
  - 2 fingers: Double-click
  - 3 fingers: Copy command
  - 4 fingers: Paste command
  - 5 fingers: Text selection mode
- **Smooth Movement**: Interpolation and smoothing for natural cursor movement
- **Volume Control**: Adjust system volume using finger distance

### Virtual Painter Mode
- **Drawing Canvas**: Create digital paintings using hand gestures
- **Color Selection**: Multiple colors available via header overlays
- **Brush Control**: Adjustable brush thickness and color
- **Finger Gestures**: 
  - Index + Middle fingers up: Drawing mode
  - Other finger combinations: Color/tool selection

### Integrated Control
- **Easy Switching**: Press 'S' to switch to Painter, 'E' to return to Mouse, 'Q' to quit
- **Seamless Transition**: Smooth switching between modes without restarting

## Requirements 📋

- Python 3.7+
- OpenCV (`opencv-python`)
- MediaPipe (`mediapipe`)
- AutoPy (`autopy`)
- PyAutoGUI (`pyautogui`)
- Keyboard (`keyboard`)
- NumPy (`numpy`)

## Installation 🛠️

1. **Clone the repository**:
```bash
git clone https://github.com/yoyo2-hub/Virtual_Mouse-Virtual_Painter.git
cd Virtual_Mouse-Virtual_Painter
```

2. **Install dependencies**:
```bash
pip install -r requirements.txt
```

Or install packages individually:
```bash
pip install opencv-python mediapipe autopy pyautogui keyboard numpy
```

## Usage 🚀

### Start the Application
```bash
python main.py
```

The application starts in **Virtual Mouse mode** by default.

### Controls

| Key | Action |
|-----|--------|
| `S` | Switch to Virtual Painter mode |
| `E` | Switch back to Virtual Mouse mode |
| `Q` | Quit the application |

### Virtual Mouse Gestures

| Fingers Up | Action |
|-----------|--------|
| 1 (Index) | Move mouse cursor |
| 2 (Index + Middle) | Double-click or volume control |
| 3+ | Copy, Paste, or Text Selection |

### Virtual Painter Gestures

| Gesture | Action |
|---------|--------|
| Index + Middle up | Draw on canvas |
| Thumb up | Select color/tool |
| All fingers | Reset/Clear |

## Project Structure 📁

```
Virtual_Mouse-Virtual_Painter/
├── main.py                      # Main entry point - mode switcher
├── AiVirtualMouseProject.py    # Virtual Mouse implementation
├── painter.py                   # Virtual Painter implementation
├── volume.py                    # Volume control module
├── HandTrackingModule.py        # Hand detection & tracking utility
├── Header/                      # Color palette & tool overlays
└── README.md
```

## Key Components 🔧

### HandTrackingModule.py
Custom hand detection class using MediaPipe that provides:
- `findHands()`: Detect and draw hand landmarks
- `findPosition()`: Get coordinates of hand joints
- `fingersUp()`: Determine which fingers are extended
- `findDistance()`: Calculate distance between two finger points

### AiVirtualMouseProject.py
Virtual mouse controller with:
- Real-time cursor movement tracking
- Gesture-based mouse actions (click, drag, select)
- Multi-mode operation based on finger counts
- Screen boundary management and smoothing

### painter.py
Digital painting application featuring:
- Real-time canvas drawing
- Color palette selection
- Brush thickness adjustment
- Header overlays for tool selection

### volume.py
Standalone volume control module using:
- Finger distance measurement
- System volume adjustment
- Visual feedback for volume levels

## How It Works 🎯

1. **Hand Detection**: Webcam captures video frames
2. **Landmark Recognition**: MediaPipe identifies 21 hand landmarks in real-time
3. **Gesture Analysis**: Finger positions determine the current gesture/action
4. **Action Execution**: Commands sent to control mouse or draw on canvas
5. **Visual Feedback**: Real-time display of hand tracking and current mode

## Tips for Best Results 💡

- Ensure good lighting in your environment
- Keep your hand within the camera frame
- Move smoothly for better tracking accuracy
- Hold gestures steady for 0.5 seconds to register actions
- Test different hand distances for optimal volume control
- Use a webcam with at least 30 FPS for smooth performance

## Author 👨‍💻

**yoyo2-hub** - [GitHub Profile](https://github.com/yoyo2-hub)

**Enjoy controlling your computer with hand gestures! 🙌**
