import cv2

# Camera Settings
CAMERA_ID = 0  # Default webcam
FRAME_WIDTH = 640
FRAME_HEIGHT = 480
FPS_TARGET = 30
MODEL_PATH = 'hand_landmarker.task'

# Hand Tracking Settings
MIN_DETECTION_CONFIDENCE = 0.7
MIN_TRACKING_CONFIDENCE = 0.5
MAX_NUM_HANDS = 1  # Version 1 restricted to single hand

# Smoothening
# Dynamic Smoothing: Low smoothing for fast moves, High smoothing for slow precision
SMOOTHING_FACTOR = 7  # Baseline (Legacy, kept for reference)
SMOOTHING_LPF = 0.5   # Low Pass Filter Alpha (0.0 - 1.0, lower = smoother)
# Dynamic Ranges
MIN_SMOOTHING = 2.0   # Fast movement (Responsive)
MAX_SMOOTHING = 15.0  # Slow movement (Very Smooth)
SMOOTHING_SPEED_THRESHOLD = 150 # Pixel distance to trigger max responsiveness

# Gesture Thresholds
CLICK_DISTANCE_THRESHOLD = 60  # Increased further to improve Left Click detection
CLICK_HOLD_TIME = 0.2  # Reduced for faster clicking
PAUSE_HOLD_TIME = 1.0 # Seconds to hold fist to pause (optional, or immediate)
GESTURE_TIMEOUT = 0.2 # Time to wait before resetting gesture state

# Version 2 Settings
SCROLL_SPEED = 30 # px per scroll event (approx)
GESTURE_COOLDOWN = 0.5 # Seconds between clicks (Debounce)
DOUBLE_CLICK_DISTANCE = 40 # Max distance for pinch

# Safety
SCREEN_MARGIN = 0 # Full camera frame used for control
FAILSAFE_FPS = 10 # Minimum FPS before pausing for safety

# Visuals
COLOR_HAND_POINTS = (0, 255, 0)
COLOR_HAND_LINES = (0, 255, 0)
COLOR_ACTIVE = (0, 255, 0) # Green
COLOR_SCROLL = (255, 255, 0) # Cyan/Yellowish
COLOR_PAUSED = (0, 0, 255) # Red
COLOR_TEXT = (255, 255, 255)
UI_FONT = cv2.FONT_HERSHEY_SIMPLEX
UI_FONT_SCALE = 1
UI_THICKNESS = 2
