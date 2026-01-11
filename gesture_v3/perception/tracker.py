
import mediapipe as mp
import numpy as np
import time
import os
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

# Relative import fix if needed, but config is in parent
try:
    from .. import config
except ImportError:
    import config

class HandTracker:
    """
    Wrapper for MediaPipe Hand Landmarker.
    Uses VIDEO mode for temporal consistency (internal smoothing).
    """
    def __init__(self, model_path="hand_landmarker.task"):
        self.model_path = model_path
        if not os.path.exists(self.model_path):
             # Try looking one level up if not found (development convenience)
             if os.path.exists("../" + model_path):
                 self.model_path = "../" + model_path
             else:
                 raise FileNotFoundError(f"Model not found at {model_path}")

        base_options = python.BaseOptions(model_asset_path=self.model_path)
        
        # VIDEO mode is critical for temporal consistency.
        # It requires timestamps to be passed in strictly increasing order.
        options = vision.HandLandmarkerOptions(
            base_options=base_options,
            running_mode=vision.RunningMode.VIDEO,
            num_hands=2, # Support 2 hands for Sci-Fi gestures
            min_hand_detection_confidence=0.5,
            min_hand_presence_confidence=0.5,
            min_tracking_confidence=0.5
        )
        self.landmarker = vision.HandLandmarker.create_from_options(options)

    def process(self, image_rgb, timestamp_ms):
        """
        Process a frame.
        :param image_rgb: OpenCV Image (RGB)
        :param timestamp_ms: Current timestamp in milliseconds (Must be increasing!)
        :return: Detection result
        """
        # Create MediaPipe Image
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=image_rgb)
        
        # Detect
        result = self.landmarker.detect_for_video(mp_image, int(timestamp_ms))
        
        return result
