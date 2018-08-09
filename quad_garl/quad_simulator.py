#!/usr/bin/env python3
import signal
import sys
from typing import Any, List, Tuple

from quad_garl import gui, quad_controller, quadcopter


class Quadcopter:
    def signal_handler(self, signal, frame):
        """ Catch Ctrl+C to stop threads """
        self.run = False
        self.log('Stopping')
        self.stop_threads()
        sys.exit(0)

    def __init__(self, log, target_pose):
        signal.signal(signal.SIGINT, self.signal_handler)

        # Constants
        self.TIME_SCALING = 1.0
        self.QUAD_DYNAMICS_UPDATE = 0.002  # seconds
        self.CONTROLLER_DYNAMICS_UPDATE = 0.005  # seconds
        self.run = True
        self.position_target = target_pose[0:3]
        self.orientation_target = target_pose[3:6]
        self.quad_id = "q1"

        # Logging
        self.log = log

        # Define the quadcopters
        self.log("Create quadcopter definition")
        self.QUADCOPTER = \
            {'q1': {'position': [1, 0, 4], 'orientation': [0, 0, 0], 'L': 0.3, 'r': 0.1, 'prop_size': [10, 4.5],
                    'weight': 1.2}}

        # Make objects for quadcopter, gui and controller
        self.log("Create objects for quad, gui and controller")
        self.gui = gui.GUI(quads=self.QUADCOPTER, log=self.log)
        self.quad = quadcopter.Quadcopter(self.QUADCOPTER, dt=self.QUAD_DYNAMICS_UPDATE,
                                          time_scaling=self.TIME_SCALING, log=self.log)
        self.controller = quad_controller.ManualController(actuate_motors=self.quad.set_motor_speeds,
                                                           quad_identifier=self.quad_id,
                                                           target_pose=target_pose,
                                                           update_rate=self.CONTROLLER_DYNAMICS_UPDATE,
                                                           time_scaling=self.TIME_SCALING,
                                                           log=self.log)

    def get_quad_state(self) -> Tuple[Any, Any]:
        self.log("Get quad state")
        return self.quad.get_position(self.quad_id), self.quad.get_orientation(self.quad_id)

    def set_quad_state(self, position: List, orientation: List):
        self.log("Set quad state")
        self.quad.set_position(self.quad_id, position)
        self.quad.set_orientation(self.quad_id, orientation)
        self.gui.update()

    def apply_throttle(self, throttle: List):
        self.controller.update_throttle(throttle=throttle)
        self.controller.update()
        self.quad.update()
        self.gui.update()
