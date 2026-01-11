import math
import config

class GestureRecognizer:
    def __init__(self):
        self.tip_ids = [4, 8, 12, 16, 20] # Thumb, Index, Middle, Ring, Pinky
    
    def detect_gesture(self, lm_list):
        """
        Analyzes the landmark list to determine the current gesture.
        Returns:
            gesture_name (str): "MOVE", "CLICK", "PAUSE", "NEUTRAL"
            info (dict): Additional info like distance or finger status
        """
        if len(lm_list) == 0:
            return "NEUTRAL", {}

        # 1. Determine which fingers are up
        fingers = []
        
        # Thumb (check x for left/right decision, but for simplicity here check relative to knuckle)
        # Using a simpler heuristic for general hand orientation:
        # Check if tip is to the left or right of knuckle might depend on hand (left/right).
        # For V1, assuming right hand or general "outwards" extension. 
        # Better: check x-coordinate relative to IP joint (id 3)
        if lm_list[self.tip_ids[0]][1] > lm_list[self.tip_ids[0] - 1][1]: # Assuming right hand facing camera? 
                                                                           # Actually, simpler is checking x for thumb.
                                                                           # Let's stick to standard vertical check for others, 
                                                                           # and a distance check for thumb-index click.
            # fingers.append(1) 
            pass # Thumb logic is complex due to rotation, will use distance for CLICK anyway.

        # 4 Fingers
        for id in range(1, 5):
            if lm_list[self.tip_ids[id]][2] < lm_list[self.tip_ids[id] - 2][2]: # y-coordinate (up is lower value in pixels)
                fingers.append(1)
            else:
                fingers.append(0)
        
        # Fingers array now has [Index, Middle, Ring, Pinky] status (1=Up, 0=Down)
        
        # 2. Logic Classification
        
        # --- DISTANCE CALCULATIONS (moved up for priority) ---
        
        # Distance: Thumb to Index (for Left Click)
        ind_x, ind_y = lm_list[8][1], lm_list[8][2]
        thumb_x, thumb_y = lm_list[4][1], lm_list[4][2]
        dist_idx = math.hypot(ind_x - thumb_x, ind_y - thumb_y)
        
        # Distance: Thumb to Middle (for Right Click)
        mid_x, mid_y = lm_list[12][1], lm_list[12][2]
        dist_mid = math.hypot(mid_x - thumb_x, mid_y - thumb_y)

        # --- PRIORITY GESTURES (Clicks) ---

        # LEFT CLICK: Pinch Thumb + Index (Primary interaction)
        if dist_idx < config.CLICK_DISTANCE_THRESHOLD:
             return "CLICK", {"distance": dist_idx}

        # RIGHT CLICK: Pinch Thumb + Middle
        if dist_mid < config.CLICK_DISTANCE_THRESHOLD:
             return "RIGHT_CLICK", {"distance": dist_mid}

        # --- STATE GESTURES ---

        # PAUSE: All fingers down (Fist)
        # Only trigger if NOT a click (handled above)
        if fingers == [0, 0, 0, 0]:
             return "PAUSE", {}

        # 4. Gesture Classification

        # SCROLL MODE: Index and Middle UP, others DOWN
        if fingers == [1, 1, 0, 0]:
            # To avoid confusion with specific pinch gestures, ensure thumb is somewhat away?
            # Or just accept [1,1,0,0] as Scroll mode trigger.
            return "SCROLL", {}

        # MOVE: Only Index Finger Up
        if fingers == [1, 0, 0, 0]:
            return "MOVE", {}
        
        # NEUTRAL
        return "NEUTRAL", {"distance_idx": dist_idx, "distance_mid": dist_mid}
