
import cv2
import time
from gesture_v3 import config
from gesture_v3.perception.tracker import HandTracker

class SystemController:
    """
    Core Application Loop (V3)
    Orchestrates: Camera -> Tracker -> Smoother -> Intent -> Physics -> UI -> Display
    """
    def __init__(self):
        self.running = True
        self.cap = cv2.VideoCapture(0)
        
        # Setup Camera
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
        self.cap.set(cv2.CAP_PROP_FPS, config.TARGET_FPS)
        
        # Modules
        self.tracker = HandTracker()
        self.start_time = time.time()
        
    def run(self):
        print(f"[{config.APP_NAME}] System Initialized. Press 'Q' to Quit.")
        
        # Initialize Subsystems
        from gesture_v3.perception.smoothing import OneEuroFilter
        from gesture_v3.intent.classifier import GestureClassifier
        from gesture_v3.control.mouse_physics import PhysicsCursor
        from gesture_v3.ui.hud import CinematicHUD

        smoother = OneEuroFilter(time.time(), [0.5, 0.5], min_cutoff=config.ONE_EURO_MIN_CUTOFF, beta=config.ONE_EURO_BETA)
        classifier = GestureClassifier()
        cursor = PhysicsCursor()
        hud = CinematicHUD()
        
        last_time = time.time()

        while self.running:
            # Time Delta
            current_time = time.time()
            dt = current_time - last_time
            last_time = current_time
            
            success, img = self.cap.read()
            if not success:
               continue

            # 1. Flip & Color correction
            img = cv2.flip(img, 1) # Mirror view
            img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            
            # 2. Perception (Tracking)
            frame_timestamp_ms = (current_time - self.start_time) * 1000
            
            # Safety Check: Low FPS
            fps = 1/dt if dt > 0 else 0
            if fps < config.FAILSAFE_FPS and (current_time - self.start_time) > 2.0:
                 cv2.putText(img, "SAFETY PAUSE: LOW FPS", (config.WINDOW_WIDTH//2 - 150, config.WINDOW_HEIGHT//2), 
                             cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                 cv2.imshow(config.APP_NAME, img)
                 key = cv2.waitKey(1)
                 if key == ord('q'): self.running = False
                 continue

            detection_result = self.tracker.process(img_rgb, frame_timestamp_ms)
            
            hand_landmarks = None
            delta_x, delta_y = 0.0, 0.0
            state = "IDLE"
            confidence = 0.0
            
            if detection_result.hand_landmarks:
                hand_landmarks = detection_result.hand_landmarks[0]
                
                # --- V6 RELATIVE TRACKING ---
                # Use Index MCP (5) as the anchor for movement (stable part of palm)
                raw_point = hand_landmarks[5] 
                norm_x, norm_y = raw_point.x, raw_point.y
                
                # 3. Smoothing
                filtered_pos = smoother(current_time, [norm_x, norm_y])
                curr_x, curr_y = filtered_pos[0], filtered_pos[1]
                
                # Calculate Delta
                if hasattr(self, 'prev_hand_x'):
                    delta_x = curr_x - self.prev_hand_x
                    delta_y = curr_y - self.prev_hand_y
                
                self.prev_hand_x = curr_x
                self.prev_hand_y = curr_y
                
                # 4. Intent Classification
                state, meta = classifier.process(hand_landmarks)
                # Store raw state because we might override it for HUD
                raw_state = state 
                confidence = meta.get("confidence", 0.0)
                
                # --- V6 STATE MACHINE ---
                current_time_loop = time.time()
                
                # Globals
                if not hasattr(self, 'drag_active'): self.drag_active = False
                if not hasattr(self, 'last_toggle_time'): self.last_toggle_time = 0
                if not hasattr(self, 'last_click_time'): self.last_click_time = 0
                
                # 1. DRAG TOGGLE LOGIC (FIST)
                if state == "FIST":
                    if (current_time_loop - self.last_toggle_time) > config.DRAG_TOGGLE_COOLDOWN:
                        self.drag_active = not self.drag_active # Toggle
                        self.last_toggle_time = current_time_loop
                        
                        if self.drag_active:
                            import pyautogui
                            pyautogui.mouseDown() # PICK
                        else:
                            import pyautogui
                            pyautogui.mouseUp()   # DROP
                            
                # 2. EXECUTE ACTIONS BASED ON STATE & TOGGLE
                
                # A. DRAG MODE (Active)
                if self.drag_active:
                    state = "DRAG_ACTIVE" # Override classifier state for HUD
                    
                    # Allow movement if not performing another exclusive action
                    if raw_state == "MOVE" or raw_state == "IDLE" or raw_state == "FIST":
                         cursor.update_relative(delta_x, delta_y, dt)
                
                # B. NORMAL MODE (Not Dragging)
                else:
                    if state == "MOVE":
                        cursor.update_relative(delta_x, delta_y, dt)
                        
                    elif state == "CLICK_LEFT":
                        if (current_time_loop - self.last_click_time) > config.CLICK_COOLDOWN:
                             import pyautogui
                             pyautogui.click()
                             self.last_click_time = current_time_loop
                             cv2.circle(img, (int(norm_x*config.WINDOW_WIDTH), int(norm_y*config.WINDOW_HEIGHT)), 50, config.COLOR_CLICK, 4)
                             
                    elif state == "CLICK_RIGHT":
                        if (current_time_loop - self.last_click_time) > config.CLICK_COOLDOWN: 
                             import pyautogui
                             pyautogui.rightClick()
                             self.last_click_time = current_time_loop
                             
                    elif state == "SCROLL":
                        if hasattr(self, 'last_scroll_y'):
                             dy = norm_y - self.last_scroll_y
                             if abs(dy) > 0.005: 
                                 import pyautogui
                                 scroll_amount = int(-dy * config.SCROLL_SPEED * 100)
                                 pyautogui.scroll(scroll_amount)
                        self.last_scroll_y = norm_y
                    else:
                        if hasattr(self, 'last_scroll_y'): del self.last_scroll_y

                # 5. UI Layer
                hud.draw(img, hand_landmarks, state, confidence)
                
            else:
                # HAND LOST SAFETY
                if hasattr(self, 'drag_active') and self.drag_active:
                    import pyautogui
                    pyautogui.mouseUp()
                    self.drag_active = False
                    print("Hand lost. Safety Drop.")
                
                # Reset Delta Reference
                if hasattr(self, 'prev_hand_x'): 
                    del self.prev_hand_x
                    del self.prev_hand_y
                
                classifier.process(None)
                hud.draw(img, None, "IDLE", 0.0)
            
            # Physics call handles internally now (update_relative called above)


            # 7. System Info
            fps = 1/dt if dt > 0 else 0
            cv2.putText(img, f"J.A.R.V.I.S  |  FPS: {int(fps)}", (20, 30), cv2.FONT_HERSHEY_PLAIN, 1, (200, 255, 200), 1)

            # 8. Display
            cv2.imshow(config.APP_NAME, img)

            # 9. Inputs
            key = cv2.waitKey(1)
            if key == ord('q'):
                self.running = False

        self.cap.release()
        cv2.destroyAllWindows()
