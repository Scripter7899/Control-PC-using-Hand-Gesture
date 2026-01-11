
import time
import math
from gesture_v3 import config

class GestureClassifier:
    """
    Intent Engine.
    Uses confidence buckets to determine gesture state.
    States:
    - IDLE: No hand or erratic movement
    - HOVER: Hand detected, cursor moving
    - CLICK_PENDING: Pinch detected, accumulating confidence
    - CLICK: Pinch confirmed
    - DRAG: Pinch held + movement (Future)
    """
    def __init__(self):
        self.state = "IDLE"
        self.pinch_confidence = 0.0
        self.last_update = time.time()
        
        # Tip Indices
        self.THUMB_TIP = 4
        self.INDEX_TIP = 8

    def process(self, landmarks):
        """
        Analyze landmarks to determine intent.
        :param landmarks: Normalized Landmark list
        :return: (State, MetaDataDict)
        """
        if not landmarks:
            self.state = "IDLE"
            self.pinch_confidence = 0.0
            return self.state, {}

        # 1. Calc Click Pinch (Thumb + Index)
        thumb = landmarks[4]
        index = landmarks[8]
        dist_click = math.hypot(thumb.x - index.x, thumb.y - index.y)

        # 2. Calc Right Click Pinch (Thumb + Middle)
        middle = landmarks[12]
        dist_right = math.hypot(thumb.x - middle.x, thumb.y - middle.y)
        
        # 3. Velocity Gate (Prevent click while moving fast)
        wrist = landmarks[0]
        curr_time = time.time()
        dt = curr_time - self.last_update
        self.last_update = curr_time
        
        velocity = 0.0
        if hasattr(self, 'prev_wrist'):
            dx = wrist.x - self.prev_wrist.x
            dy = wrist.y - self.prev_wrist.y
            dist_move = math.hypot(dx, dy)
            if dt > 0:
                velocity = dist_move / dt # Units per second
        
        self.prev_wrist = wrist
        
        # 4. Confidence Accumulation
        # Only accumulate if pinch is close AND hand is stable (velocity < 2.0 approx)
        is_stable = velocity < 2.0 
        
        # We need separate confidence for Right Click to be robust, 
        # but for simplicity let's use a "Pinch Type" flag if single confidence is high?
        # Better: Priority check.

        # CLICK LOGIC
        if dist_click < config.PINCH_THRESHOLD_NORM and is_stable:
             self.pinch_confidence += config.CONFIDENCE_GROWTH
             self.pinch_type = "LEFT"
        elif dist_right < config.PINCH_THRESHOLD_NORM and is_stable:
             self.pinch_confidence += config.CONFIDENCE_GROWTH
             self.pinch_type = "RIGHT"
        else:
             self.pinch_confidence -= config.CONFIDENCE_DECAY
            
        # Clamp confidence
        self.pinch_confidence = max(0.0, min(1.0, self.pinch_confidence))

        # --- V6 GESTURE CLASSIFICATION ---
        
        # 1. Basic Finger States (Up/Down)
        # Compare Tip Y to PIP Y (Proximal Interphalangeal) is better for curling check than MCP
        # Actually MCP is safer for general "Up/Down".
        
        fingers_up = [False] * 5
        
        # Thumb: Compare Tip x to IP x (Use relative to wrist to determine side?)
        # Simple heuristic: Thumb Tip distance to Pinky Base > Threshold?
        # Let's stick to simple y-check for 4 fingers, and specialized for thumb.
        
        # Index (8), Middle (12), Ring (16), Pinky (20)
        # Compare Tip Y to Pip Y (6, 10, 14, 18)
        for i, tip_idx in enumerate([8, 12, 16, 20]):
            pip_idx = tip_idx - 2
            fingers_up[i+1] = landmarks[tip_idx].y < landmarks[pip_idx].y 
            
        # Thumb (4): Check distance to index MCP(5)? Or just "Out"?
        # If thumb tip is far from index mcp, it's open.
        thumb_tip = landmarks[4]
        index_mcp = landmarks[5]
        thumb_out = math.hypot(thumb_tip.x - index_mcp.x, thumb_tip.y - index_mcp.y) > 0.05
        fingers_up[0] = thumb_out
        
        # 2. Key Gestures
        
        # A. FIST (All closed)
        # Strict: All 4 fingers down. Thumb can be whatever (usually close)
        is_fist = not any(fingers_up[1:]) # Index, Mid, Ring, Pinky DOWN
        
        # B. OPEN PALM (All open)
        is_palm = all(fingers_up)
        
        # C. PEACE (Scroll)
        is_peace = fingers_up[1] and fingers_up[2] and not fingers_up[3] and not fingers_up[4] # I, M UP. R, P DOWN.
        
        # D. PINCHES
        # Index Pinch
        dist_index = math.hypot(landmarks[4].x - landmarks[8].x, landmarks[4].y - landmarks[8].y)
        is_pinch_index = dist_index < config.PINCH_THRESHOLD_NORM
        
        # Middle Pinch
        dist_middle = math.hypot(landmarks[4].x - landmarks[12].x, landmarks[4].y - landmarks[12].y)
        is_pinch_middle = dist_middle < config.PINCH_THRESHOLD_NORM
        
        # 3. State Determination
        
        # Priority: PINCH > SCROLL > FIST > PALM > IDLE
        
        if is_pinch_index:
            self.state = "CLICK_LEFT"
            self.pinch_confidence = 1.0 # Instant
        elif is_pinch_middle:
            self.state = "CLICK_RIGHT"
        elif is_peace:
            self.state = "SCROLL"
        elif is_fist:
            self.state = "FIST"
        elif is_palm:
            self.state = "MOVE"
        else:
            self.state = "IDLE" # Ambiguous / Transition

        return self.state, {
            "confidence": 1.0,
            "pinch_dist": dist_index
        }
