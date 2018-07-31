#!/usr/bin/env python3
import signal
import sys
from typing import List

import numpy as np

from quad_garl import gui, quad_controller, quadcopter


class Quadcopter():
    def signal_handler(self, signal, frame):
        """ Catch Ctrl+C to stop threads """
        self.run = False
        self.log.info('Stopping')
        self.stop_threads()
        sys.exit(0)

    def __init__(self, log):
        signal.signal(signal.SIGINT, self.signal_handler)

        # Constants
        self.TIME_SCALING = 1.0
        self.QUAD_DYNAMICS_UPDATE = 0.002  # seconds
        self.CONTROLLER_DYNAMICS_UPDATE = 0.005  # seconds
        self.run = True

        # Logging
        self.log = log

        # Define the quadcopters
        self.log.info("Create quadcopter definition")
        self.QUADCOPTER = \
            {'q1': {'position': [1, 0, 4], 'orientation': [0, 0, 0], 'L': 0.3, 'r': 0.1, 'prop_size': [10, 4.5],
                    'weight': 1.2}}

        # Make objects for quadcopter, gui and controller
        self.log.info("Create objects for quad, gui and controller")
        self.quad = quadcopter.Quadcopter(self.QUADCOPTER)
        self.gui = gui.GUI(quads=self.QUADCOPTER)
        self.controller = quad_controller.ManualController(get_state=self.quad.get_position,
                                                           get_time=self.quad.get_time,
                                                           actuate_motors=self.quad.set_motor_speeds,
                                                           quad_identifier='q1')

    def start_threads(self):
        # Start threads
        self.log.info("Start worker threads for quad and controller")
        self.quad.start_thread(dt=self.QUAD_DYNAMICS_UPDATE, time_scaling=self.TIME_SCALING)
        self.controller.start_thread(update_rate=self.CONTROLLER_DYNAMICS_UPDATE, time_scaling=self.TIME_SCALING)

    def stop_threads(self):
        # Start threads
        self.log.info("Stop worker threads for quad and controller")
        self.quad.stop_thread()
        self.controller.stop_thread()

    def get_quad_state(self) -> np.array:
        self.log.info("Get quad state")
        return np.array([self.quad.get_position('q1'), self.quad.get_orientation('q1')]).flatten()

    def set_quad_state(self, state: np.array):
        self.log.info("Set quad state")
        self.gui.quads['q1']['position'] = state[0:2]
        self.gui.quads['q1']['orientation'] = state[3:5]
        self.gui.update()

    def apply_throttle(self, throttle: List):
        self.controller.update_throttle(throttle=throttle)
