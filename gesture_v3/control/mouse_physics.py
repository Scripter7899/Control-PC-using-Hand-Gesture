
import math
import pyautogui
import numpy as np
from gesture_v3 import config

pyautogui.FAILSAFE = False 

class PhysicsCursor:
    """
    Control Layer V6 (Air Mouse).
    Input: Relative Delta (dx, dy)
    Output: Relative Mouse Movement
    """
    def __init__(self):
        self.prev_dx = 0.0
        self.prev_dy = 0.0
        self.remainder_x = 0.0
        self.remainder_y = 0.0

    def update_relative(self, dx, dy, dt):
        """
        Process relative movement.
        """
        # 1. Dead Zone
        mag = math.hypot(dx, dy)
        if mag < config.DEAD_ZONE:
            return 
            
        # 2. Smoothing
        alpha = 1.0 - config.DELTA_SMOOTHING
        dx = alpha * dx + (1.0 - alpha) * self.prev_dx
        dy = alpha * dy + (1.0 - alpha) * self.prev_dy
        
        self.prev_dx = dx
        self.prev_dy = dy
        
        # 3. Acceleration
        gain = config.BASE_SENSITIVITY * (1.0 + config.ACCELERATION_FACTOR * mag)
        gain = min(gain, config.MAX_SENSITIVITY)
        
        move_x = dx * config.WINDOW_WIDTH * gain
        move_y = dy * config.WINDOW_HEIGHT * gain
        
        # Accumulate
        self.remainder_x += move_x
        self.remainder_y += move_y
        
        int_move_x = int(self.remainder_x)
        int_move_y = int(self.remainder_y)
        
        if int_move_x != 0 or int_move_y != 0:
            pyautogui.move(int_move_x, int_move_y, _pause=False)
            self.remainder_x -= int_move_x
            self.remainder_y -= int_move_y
