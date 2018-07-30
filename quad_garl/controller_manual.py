import threading
import time

import numpy as np


class ManualController:
    def __init__(self, get_state, get_time, actuate_motors, quad_identifier):
        self.get_state = get_state
        self.quad_identifier = quad_identifier
        self.actuate_motors = actuate_motors
        self.get_time = get_time
        self.time = 0
        self.thread_object = None
        self.target = [0, 0, 0]
        self.yaw_target = 0.0
        self.run = True
        self.MOTOR_LIMITS = [4000, 9000]
        self.throttle = [0, 0, 0, 0]  # m1, m2, m3, m4

    def wrap_angle(self, val):
        return ((val + np.pi) % (2 * np.pi) - np.pi)

    def update(self):
        [dest_x, dest_y, dest_z] = self.target
        [x, y, z] = self.get_state(self.quad_identifier)
        m1 = self.throttle[0]
        m2 = self.throttle[1]
        m3 = self.throttle[2]
        m4 = self.throttle[3]
        m = np.clip([m1, m2, m3, m4], self.MOTOR_LIMITS[0], self.MOTOR_LIMITS[1])
        self.actuate_motors(self.quad_identifier, m)

    def update_throttle(self, throttle):
        self.throttle = throttle

    def update_target(self, target):
        self.target = target

    def update_yaw_target(self, target):
        self.yaw_target = self.wrap_angle(target)

    def thread_run(self, update_rate, time_scaling):
        update_rate = update_rate * time_scaling
        last_update = self.get_time()
        while self.run:
            time.sleep(0)
            self.time = self.get_time()
            if (self.time - last_update).total_seconds() > update_rate:
                self.update()
                last_update = self.time

    def start_thread(self, update_rate=0.005, time_scaling=1):
        self.thread_object = threading.Thread(target=self.thread_run, args=(update_rate, time_scaling))
        self.thread_object.start()

    def stop_thread(self):
        self.run = False
