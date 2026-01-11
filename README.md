# Hand Gesture Control System V1

A software-only solution to control your PC mouse using hand gestures via a webcam. Built with Python, OpenCV, and MediaPipe.

## Features (Version 2)
-   **Multi-Mode Interaction**:
    -   **MOVE MODE**: Standard cursor control.
    -   **SCROLL MODE**: Intuitive hand-movement scrolling.
    -   **PAUSED MODE**: Safety state.
-   **Expanded Gestures**:
    -   **Right Click**: Thumb + Middle Pinch.
    -   **Left Click**: Thumb + Index Pinch.
-   **Advanced Safety**:
    -   **Global Kill Switch ('Q')**.
    -   **Auto-Pause**: Activates on hand loss or low FPS.
    -   **Cooldowns**: Prevents accidental double-clicks.
-   **Visual Dashboard**:
    -   Real-time Mode, FPS, and Gesture display.

## Prerequisites
-   Python 3.8+
-   Webcam
-   MediaPipe Model (`hand_landmarker.task`)

## Setup Instructions

1.  **Clone/Download** this repository.
2.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

3.  **Download Model**:
    The system requires the `hand_landmarker.task` model file. [Download Link](https://storage.googleapis.com/mediapipe-models/hand_landmarker/hand_landmarker/float16/1/hand_landmarker.task) or use:
    ```powershell
    Invoke-WebRequest -Uri https://storage.googleapis.com/mediapipe-models/hand_landmarker/hand_landmarker/float16/1/hand_landmarker.task -OutFile hand_landmarker.task
    ```

4.  **Run the System**:
    ```bash
    python main.py
    ```

## ✋ Gesture Guide (Detailed Patterns)

### 1. **MOVE CURSOR**
*   **Pattern**: Raise **Index Finger** ONLY. Keep other fingers curled.
*   **Action**: The mouse cursor follows your index fingertip.
*   **Tips**: Keep your hand steady. Move within your camera's field of view.

### 2. **LEFT CLICK**
*   **Pattern**: Pinch your **Thumb** and **Index Finger** together.
*   **Action**: Triggers a Left Click.
*   **Requirement**:
    *   Fingers must touch (distance < 40px).
    *   Hold for **0.25 seconds** (prevents accidental clicks).

### 3. **RIGHT CLICK**
*   **Pattern**: Pinch your **Thumb** and **Middle Finger** together.
*   **Action**: Triggers a Right Click (Context Menu).
*   **Requirement**: Hold for **0.25 seconds**.

### 4. **SCROLL MODE**
*   **Pattern**: Raise **Index** + **Middle Fingers** (Peace Sign / Victory Sign).
*   **Action**: Enters SCROLL MODE.
    *   Move Hand **UP** -> Scroll Page UP.
    *   Move Hand **DOWN** -> Scroll Page DOWN.
*   **Exit**: Lower your middle finger to return to cursor control.

### 5. **PAUSE / SAFETY**
*   **Pattern**: Make a **Closed Fist**.
*   **Action**: Pauses all system control immediately.
*   **Visual**: Screen border turns RED, Text says "PAUSED".

### 6. **QUIT**
*   **Pattern**: Press **'Q'** on your keyboard.
*   **Action**: Safery shutdown of the application.

## Configuration
Tweak `config.py`:
-   `SCROLL_SPEED`: Adjust scroll sensitivity.
-   `GESTURE_COOLDOWN`: Time between clicks.
-   `SMOOTHING_FACTOR`: Cursor stability.

## Version 3 Roadmap (Future)
-   **Voice Control**: "Computer, open browser".
-   **Keyboard Input**: Air-typing interface.
-   **Custom Gestures**: ML Training for user-defined signaling.


---
*Created for Portfolio Demonstration*




🚀 Curated by APEX HUB
💡 Here you’ll find -

✅ Advanced Ethical Hacking Guides
✅ Penetration Testing Methods
✅ Viral Methods 
✅ Unique Premium Tools
✅ Premium Courses for Free

💯 legal content, purely for educational and research purposes.

📲 Join the private channel to access all Content -

https://t.me/join_apex_hub

⚡ Learn. Apply. Grow. Stay Ahead
