import pyautogui
import numpy as np
import config

class MouseController:
    def __init__(self):
        self.screen_width, self.screen_height = pyautogui.size()
        self.prev_x, self.prev_y = 0, 0
        self.curr_x, self.curr_y = 0, 0
    
    def move_mouse(self, x, y):
        """
        Moves the mouse to (x, y) with smoothing and clamping.
        x, y: Normalized coordinates (0.0 to 1.0) or raw pixels? 
              Let's accept raw pixels from the camera frame and map them to screen.
        """
        
        # 1. Map Camera Coordinates to Screen Coordinates
        # Use config.SCREEN_MARGIN to create a "active area" in the camera frame
        # x is from 0 to config.FRAME_WIDTH
        # y is from 0 to config.FRAME_HEIGHT
        
        # Linear Interpolation: np.interp(v, [min_in, max_in], [min_out, max_out])
        
        screen_x = np.interp(x, 
                             [config.SCREEN_MARGIN, config.FRAME_WIDTH - config.SCREEN_MARGIN], 
                             [0, self.screen_width])
        
        screen_y = np.interp(y, 
                             [config.SCREEN_MARGIN, config.FRAME_HEIGHT - config.SCREEN_MARGIN], 
                             [0, self.screen_height])

        # 2. Clamp values to be safe
        screen_x = max(0, min(screen_x, self.screen_width - 1))
        screen_y = max(0, min(screen_y, self.screen_height - 1))

        # 3. Dynamic Smoothing
        # Calculate distance to target
        dist = np.hypot(screen_x - self.prev_x, screen_y - self.prev_y)
        
        # Map distance to smoothing factor
        # Large distance (fast move) -> Low Smoothing (Responsive) -> e.g., 2
        # Small distance (slow move) -> High Smoothing (Stable) -> e.g., 15
        
        # Normalize distance relative to threshold (0 to 1)
        speed_factor = min(dist / config.SMOOTHING_SPEED_THRESHOLD, 1.0)
        
        # Invert: High speed = Low smoothing value
        # smooth_val = MAX - (MAX - MIN) * speed_factor
        current_smooth = config.MAX_SMOOTHING - (config.MAX_SMOOTHING - config.MIN_SMOOTHING) * speed_factor
        
        # Apply Smoothing
        self.curr_x = self.prev_x + (screen_x - self.prev_x) / current_smooth
        self.curr_y = self.prev_y + (screen_y - self.prev_y) / current_smooth

        # 4. Move Mouse
        try:
            pyautogui.moveTo(self.curr_x, self.curr_y)
            self.prev_x, self.prev_y = self.curr_x, self.curr_y
        except pyautogui.FailSafeException:
            pass # Handle PyAutoGUI failsafe if it triggers (corner of screen)

    def click(self):
        """
        Performs a left click.
        """
        pyautogui.click()

    def right_click(self):
        """
        Performs a right click.
        """
        pyautogui.rightClick()
    
    def scroll(self, steps):
        """
        Scrolls the screen.
        steps: +ve for UP, -ve for DOWN (PyAutoGUI convention might differ on OS)
        PyAutoGUI: positive clicks = scroll UP
        """
        # Limit scroll speed for safety
        if steps > 0:
            pyautogui.scroll(int(config.SCROLL_SPEED))
        else:
            pyautogui.scroll(int(-config.SCROLL_SPEED))
