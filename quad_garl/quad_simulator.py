#!/usr/bin/env python3
import signal
import sys
from typing import List

import numpy as np

from quad_garl import gui, quad_controller, quadcopter


class Quadcopter:
    def signal_handler(self, signal, frame):
        """ Catch Ctrl+C to stop threads """
        self.run = False
        self.log.info('Stopping')
        self.stop_threads()
        sys.exit(0)

    def __init__(self, log, target):
        signal.signal(signal.SIGINT, self.signal_handler)

        # Constants
        self.TIME_SCALING = 1.0
        self.QUAD_DYNAMICS_UPDATE = 0.002  # seconds
        self.CONTROLLER_DYNAMICS_UPDATE = 0.005  # seconds
        self.run = True
        self.target = target[0:3]
        self.yaw_target = target[-1]
        self.quad_id = "q1"

        # Logging
        self.log = log

        # Define the quadcopters
        self.log.info("Create quadcopter definition")
        self.QUADCOPTER = \
            {'q1': {'position': [1, 0, 4], 'orientation': [0, 0, 0], 'L': 0.3, 'r': 0.1, 'prop_size': [10, 4.5],
                    'weight': 1.2}}

        # Make objects for quadcopter, gui and controller
        self.log.info("Create objects for quad, gui and controller")
        self.gui = gui.GUI(quads=self.QUADCOPTER)
        self.quad = quadcopter.Quadcopter(self.QUADCOPTER, dt=self.QUAD_DYNAMICS_UPDATE, time_scaling=self.TIME_SCALING)
        self.controller = quad_controller.ManualController(actuate_motors=self.quad.set_motor_speeds,
                                                           quad_identifier=self.quad_id,
                                                           target=self.target,
                                                           update_rate=self.CONTROLLER_DYNAMICS_UPDATE,
                                                           time_scaling=self.TIME_SCALING)

    def get_quad_state(self) -> np.array:
        self.log.info("Get quad state")
        return np.array([self.quad.get_position('q1'), self.quad.get_orientation('q1')]).flatten()

    def apply_throttle(self, throttle: List):
        # Set throttle
        self.controller.update_throttle(throttle=throttle)
        # Apply throttle
        self.controller.update()
        # Get new state
        self.quad.update()
        # Display new state
        self.gui.update()
