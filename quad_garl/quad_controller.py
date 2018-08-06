import numpy as np

from quad_garl.quad_utils import wrap_angle


class ManualController:
    def __init__(self, get_state, get_time, actuate_motors, quad_identifier, target, update_rate, time_scaling):
        self.get_state = get_state
        self.quad_identifier = quad_identifier
        self.actuate_motors = actuate_motors
        self.get_time = get_time
        self.update_rate = update_rate
        self.time_scaling = time_scaling
        self.time = 0
        self.thread_object = None
        self.target = target
        self.yaw_target = 0.0
        self.run = True
        self.MOTOR_LIMITS = [4000, 9000]
        self.throttle = [0, 0, 0, 0]  # m1, m2, m3, m4

    def update(self):
        print("CONTROLLER UPDATE")
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
        self.yaw_target = wrap_angle(target)
