
"""
Centralized source of truth for all physics, UI, and logic constants.
"""
import math
import pyautogui

# --- SYSTEM ---
APP_NAME = "J.A.R.V.I.S Gesture Interface"
WINDOW_WIDTH, WINDOW_HEIGHT = pyautogui.size()
TARGET_FPS = 60

# --- PERCEPTION (OneEuroFilter) ---
# Low-jitter smoothing parameters
ONE_EURO_MIN_CUTOFF = 0.5   # Hz. Lower = more smoothing when slow
ONE_EURO_BETA = 4.0         # Reduced from 10.0 to 4.0 to reduce jitter/dancing
ONE_EURO_D_CUTOFF = 1.0     # Hz. Cutoff for derivative

# --- GESTURE CONFIG ---
# Confidence accumulation (0.0 to 1.0)
GESTURE_CONFIDENCE_THRESHOLD = 0.8  # Increased back to 0.8 (require more certainty)
CONFIDENCE_DECAY = 0.2             # Faster decay (forget partial pinches quickly)
CONFIDENCE_GROWTH = 0.15           # Slower growth (require sustained pinch)

# Pinch Thresholds (mm approx, relative to hand size)
PINCH_THRESHOLD_NORM = 0.07        # Increased to 0.07 (easier to trigger click)

# --- V6 RELATIVE PHYSICS (AIR MOUSE) ---
DEAD_ZONE = 0.002        # Anti-tremor: Movement below this is ignored
BASE_SENSITIVITY = 3.0   # Base speed
ACCELERATION_FACTOR = 20.0 # Gain for fast movements
MAX_SENSITIVITY = 12.0   # Cap
DELTA_SMOOTHING = 0.6    # Lag reduction

# --- GESTURES ---
# Pinch
PINCH_THRESHOLD_NORM = 0.06
CLICK_COOLDOWN = 0.4

# Scroll
SCROLL_SPEED = 20
SCROLL_DEADZONE = 0.05

# Drag (Toggle)
DRAG_TOGGLE_COOLDOWN = 1.0 # Prevent double-toggle
COLOR_DRAG_ACTIVE = (0, 255, 0) # Green (Locked)

# --- UI COLORS (BGR) ---
COLOR_IDLE = (255, 255, 0)      # Cyan
COLOR_MOVE = (255, 255, 255)    # White (Open Palm)
COLOR_CLICK = (0, 0, 255)       # Red
COLOR_RIGHT_CLICK = (255, 0, 0) # Blue
COLOR_SCROLL = (255, 0, 255)    # Magenta
COLOR_TEXT = (255, 255, 255)

# --- SAFETY ---
FAILSAFE_FPS = 15  # Minimum FPS to maintain active control
