# Project J.A.R.V.I.S (Gesture Interface V3)

> "I am not controlling a computer. The computer understands my intent."

A production-grade, sci-fi inspired hand gesture interface featuring physics-based cursors, intent prediction, and cinematic HUD visuals.

## Features
-   **Physics Cursor**: Momentum, friction, and "weight" for stable, jitter-free control.
-   **Intent Engine**: Confidence-based gesture detection (no accidental clicks).
-   **Cinematic HUD**: Real-time holographic overlay with finger trails and dynamic reticles.
-   **OneEuro Smoothing**: Professional-grade jitter reduction.

## Setup
1.  **Install Requirements**:
    ```bash
    pip install -r requirements.txt
    ```
    *(Ensure you have `mediapipe`, `opencv-python`, `numpy`, `pyautogui`)*

2.  **Download Model**:
    Ensure `hand_landmarker.task` is in the root directory.

3.  **Run**:
    ```bash
    python main_v3.py
    ```

## Controls
-   **Move**: Raise your hand. The cursor follows your **Index Finger** with physics.
-   **Left Click**: Pinch **Thumb + Index**.
    -   *Visual*: The HUD Reticle will shrink and turn Orange (Pending) -> Red (Click).
-   **Quit**: Press **'Q'**.

## Architecture (For Developers)
-   `core/`: System loop and State management.
-   `perception/`: MediaPipe wrapper + OneEuroFilter.
-   `intent/`: Gesture State Machine (Confidence Buckets).
-   `control/`: Physics Engine (Mass/Friction).
-   `ui/`: OpenCV Drawing (HUD).

---
*Senior HCI Engineering Project*




🚀 Welcome to APEX HUB
💡 Here you’ll find -

✅ Advanced Ethical Hacking Guides
✅ Penetration Testing Methods
✅ Viral Methods 
✅ Unique Premium Tools
✅ Premium Courses for Free

💯 legal content, purely for educational and research purposes.

📲 Join the private channel to access all Content -

https://t.me/join_apex_hub
https://t.me/join_apex_hub

⚡ Learn. Apply. Grow. Stay Ahead