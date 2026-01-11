
import cv2
import numpy as np
from collections import deque
from gesture_v3 import config

class CinematicHUD:
    """
    UI Layer.
    Renders "Iron Man" style overlay.
    """
    def __init__(self):
        # Trail history
        self.trail = deque(maxlen=20)
        self.pulse_phase = 0.0

    def draw(self, img, hand_landmarks, state, confidence):
        """
        Draw the HUD.
        :param img: Canvas
        :param hand_landmarks: MediaPipe landmarks
        :param state: Current Intent State
        :param confidence: Gesture Confidence (0-1)
        """
        if not hand_landmarks:
            self.trail.clear()
            return
            
        h, w, _ = img.shape
        
        # Center of palm (approx)
        idx_base = hand_landmarks[5] # Index MCP
        pinky_base = hand_landmarks[17] # Pinky MCP
        wrist = hand_landmarks[0]
        
        cx = int((idx_base.x + pinky_base.x + wrist.x) / 3 * w)
        cy = int((idx_base.y + pinky_base.y + wrist.y) / 3 * h)
        
        # Update Trail
        self.trail.appendleft((cx, cy))
        
        # 1. Draw Trail (Light Writer Effect)
        for i in range(1, len(self.trail)):
            thickness = int(np.sqrt(20 / i) * 2)
            cv2.line(img, self.trail[i-1], self.trail[i], config.COLOR_IDLE, thickness)

        # 2. Draw Reticle (Rotating Circles)
        self.pulse_phase += 0.1
        radius = int(40 + np.sin(self.pulse_phase) * 5)
        
        color = config.COLOR_IDLE
        if state == "MOVE":
             color = config.COLOR_MOVE
             radius = 20
        elif state == "CLICK_LEFT":
             color = config.COLOR_CLICK
             radius = 35
             cv2.circle(img, (cx, cy), radius, color, 3)
        elif state == "CLICK_RIGHT":
             color = config.COLOR_RIGHT_CLICK
             radius = 35
             cv2.putText(img, "R", (cx-10, cy+10), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)
        elif state == "DRAG_ACTIVE":
             color = config.COLOR_DRAG_ACTIVE
             radius = 35
             cv2.circle(img, (cx, cy), radius, color, 4) 
             # Lock icon
             cv2.rectangle(img, (cx-10, cy-10), (cx+10, cy+10), color, -1)
        elif state == "FIST":
             color = (0, 165, 255) # Orange
             radius = 30
             cv2.putText(img, "TOGGLE", (cx-25, cy-40), cv2.FONT_HERSHEY_PLAIN, 1, color, 1)

        elif state == "SCROLL":
             color = config.COLOR_SCROLL
             radius = 45
             # Draw arrows
             cv2.arrowedLine(img, (cx, cy - 20), (cx, cy - 60), color, 2)
             cv2.arrowedLine(img, (cx, cy + 20), (cx, cy + 60), color, 2)

        # Main Arc
        cv2.ellipse(img, (cx, cy), (radius, radius), 
                    self.pulse_phase * 50, 0, 270, color, 2)
        
        # Inner Tech Geometry (Decorations)
        if state == "CLICK_PENDING":
             # Draw bar indicating confidence
             bar_len = int(confidence * 100)
             cv2.line(img, (cx - 50, cy + 60), (cx - 50 + bar_len, cy + 60), color, 4)

        # 3. Text Label
        cv2.putText(img, f"STATUS: {state}", (cx + 50, cy - 50), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (200, 200, 200), 1)
