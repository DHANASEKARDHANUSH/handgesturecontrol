# handgesturecontrol
A Python project that lets you control your computer using just your hand gestures via webcam.  
The project uses *MediaPipe* for real-time hand tracking and *PyAutoGUI* for mouse and window control.  

## ✨ Features
- 🖱 *Move Cursor* → Extend index finger and move it around to control the mouse pointer.  
- 👆 *Left Click* → Pinch *index + thumb* together.  
- ✌ *Right Click* → Extend middle finger and pinch with thumb.  
- ✊ *Minimize Window* → Make a fist (all fingers closed).  
- 🤘 *Taskbar Navigation* → Extend pinky finger to highlight windows on the taskbar.  
- 👍 *Switch Windows* → Extend thumb to outline the next taskbar window (repeat to move further).  
- ✌ *Open Window* → Show peace sign to open the currently highlighted taskbar window.  

## 🛠 Tech Stack
- [Python](https://www.python.org/)  
- [MediaPipe](https://developers.google.com/mediapipe) (hand tracking & landmarks)  
- [OpenCV](https://opencv.org/) (video capture & image processing)  
- [PyAutoGUI](https://pyautogui.readthedocs.io/) (mouse & keyboard automation)  

## 🚀 How It Works
1. Captures video frames from webcam.  
2. Detects hand landmarks using *MediaPipe Hands*.  
3. Maps finger positions to screen coordinates.  
4. Smooths cursor movement with linear interpolation (to reduce jitter).  
5. Recognizes gestures → triggers corresponding OS actions.  

## 📷 Demo
(Add screenshots or GIFs later of you using it!)  

## 📦 Installation
1. Clone this repo:
   ```bash
   git clone https://github.com/DHANASEKARDHANUSH/handgesturecontrol.git
   cd handgesturecontrol