import cv2
import time
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import config
import numpy as np

class HandTracker:
    def __init__(self, mode=False, max_hands=config.MAX_NUM_HANDS, 
                 detection_con=config.MIN_DETECTION_CONFIDENCE, 
                 track_con=config.MIN_TRACKING_CONFIDENCE):
        
        base_options = python.BaseOptions(model_asset_path=config.MODEL_PATH)
        # Use VIDEO mode for smooth tracking
        options = vision.HandLandmarkerOptions(
            base_options=base_options,
            num_hands=max_hands,
            min_hand_detection_confidence=detection_con,
            min_hand_presence_confidence=detection_con,
            min_tracking_confidence=track_con,
            running_mode=vision.RunningMode.VIDEO)
        
        self.landmarker = vision.HandLandmarker.create_from_options(options)
        self.results = None
        
        # Standard MediaPipe Hand Connections
        self.HAND_CONNECTIONS = [
            (0, 1), (1, 2), (2, 3), (3, 4),       # Thumb
            (0, 5), (5, 6), (6, 7), (7, 8),       # Index
            (5, 9), (9, 10), (10, 11), (11, 12),  # Middle (Note: 0-9 usually not drawn in favor of 5-9) -- actually MP standard is 0-9 too.
            (9, 13), (13, 14), (14, 15), (15, 16),# Ring
            (13, 17), (17, 18), (18, 19), (19, 20),# Pinky
            (0, 17) # Palm Base
        ]
        # Some visualizations add horizontal knuckles (5,9), (9,13), (13,17)
        self.HAND_CONNECTIONS += [(5,9), (9,13), (13,17)]

    def find_hands(self, img, draw=True):
        # Convert BGR to RGB for MediaPipe
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
        
        # Timestamp in ms (required for VIDEO mode)
        timestamp = int(time.time() * 1000)
        
        try:
            self.results = self.landmarker.detect_for_video(mp_image, timestamp)
        except Exception as e:
            print(f"Tracking Logic Error: {e}")
            self.results = None
        
        if self.results and self.results.hand_landmarks:
            for hand_lms in self.results.hand_landmarks:
                if draw:
                    self.draw_landmarks(img, hand_lms)
        return img

    def draw_landmarks(self, img, landmarks):
        h, w, c = img.shape
        # Convert NormalizedLandmark (x,y,z) to pixel coordinates
        points = []
        for lm in landmarks:
            # MediaPipe Tasks: .x, .y, .z (normalized 0-1)
            cx, cy = int(lm.x * w), int(lm.y * h)
            points.append((cx, cy))
        
        # Draw connections
        for p1, p2 in self.HAND_CONNECTIONS:
            if p1 < len(points) and p2 < len(points):
                cv2.line(img, points[p1], points[p2], config.COLOR_HAND_LINES, config.UI_THICKNESS)
        
        # Draw points
        for cx, cy in points:
             cv2.circle(img, (cx, cy), 5, config.COLOR_HAND_POINTS, cv2.FILLED)

    def get_landmark_list(self, img):
        lm_list = []
        if self.results and self.results.hand_landmarks:
            # V1: Single hand support
            my_hand = self.results.hand_landmarks[0]
            h, w, c = img.shape
            for id, lm in enumerate(my_hand):
                cx, cy = int(lm.x * w), int(lm.y * h)
                lm_list.append([id, cx, cy])
        return lm_list

if __name__ == "__main__":
    # Test stub
    cap = cv2.VideoCapture(config.CAMERA_ID)
    tracker = HandTracker()
    while True:
        success, img = cap.read()
        if not success:
            break
        img = tracker.find_hands(img)
        lm_list = tracker.get_landmark_list(img)
        if len(lm_list) != 0:
            print(lm_list[8]) # Tip of index finger

        cv2.imshow("Hand Tracker Test", img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()
