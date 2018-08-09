import numpy as np


class ManualController:
    def __init__(self, actuate_motors, quad_identifier, target_pose, update_rate, time_scaling, log):
        self.log = log
        self.quad_identifier = quad_identifier
        self.actuate_motors = actuate_motors
        self.update_rate = update_rate
        self.time_scaling = time_scaling
        self.time = 0
        self.position_target = target_pose[0:3]
        self.orientation_target = target_pose[3:6]
        self.run = True
        self.MOTOR_LIMITS = [4000, 9000]
        self.throttle = [0, 0, 0, 0]  # m1, m2, m3, m4

    def update(self):
        self.log.info("CONTROLLER UPDATE")
        m1 = self.throttle[0]
        m2 = self.throttle[1]
        m3 = self.throttle[2]
        m4 = self.throttle[3]
        m = np.clip([m1, m2, m3, m4], self.MOTOR_LIMITS[0], self.MOTOR_LIMITS[1])
        self.actuate_motors(self.quad_identifier, m)

    def update_throttle(self, throttle):
        self.throttle = throttle
