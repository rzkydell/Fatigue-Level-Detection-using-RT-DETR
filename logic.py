import time
from config import CLASS_MEDIUM

class FatigueStateMachine:
    def __init__(self, force_duration=2.0):
        self.current_state = "Inisialisasi..."
        self.state_time = time.time()
        self.force_medium = False
        self.force_start = None
        self.force_duration = force_duration

    def update(self, smoothed_class, class_order, order_to_name):
        if not smoothed_class or smoothed_class not in class_order:
            return self.current_state

        detected_order = class_order[smoothed_class]
        now = time.time()

        if self.current_state not in class_order:
            self.current_state = smoothed_class
            self.state_time = now
            return self.current_state

        current_order = class_order.get(self.current_state, 1)

        # A. Lompatan 1 -> 3 (Force lewat 2)
        if (current_order == 1 and detected_order == 3) or self.force_medium:
            if not self.force_medium:
                self.force_medium = True
                self.force_start = now
                self.current_state = order_to_name.get(2, CLASS_MEDIUM)

            if now - self.force_start >= self.force_duration:
                self.current_state = order_to_name.get(3, smoothed_class)
                self.force_medium = False
                self.state_time = now
            else:
                self.current_state = order_to_name.get(2, CLASS_MEDIUM)

        # B. Transisi 1 -> 2 (Delay 0.5s)
        elif current_order == 1 and detected_order == 2:
            if now - self.state_time >= 0.5:
                self.current_state = smoothed_class
                self.state_time = now

        # C. Transisi 2 -> 3 (Max 4s)
        elif current_order == 2 and detected_order == 3:
            if now - self.state_time <= 4.0:
                self.current_state = smoothed_class
                self.state_time = now

        # D. Transisi Turun
        elif detected_order < current_order:
            self.current_state = smoothed_class
            self.state_time = now
            self.force_medium = False

        return self.current_state