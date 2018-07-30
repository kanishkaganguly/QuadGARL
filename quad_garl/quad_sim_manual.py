#!/usr/bin/env python3
import logging
import signal
import sys

import numpy as np

from quad_garl.genetic_algorithm import GeneticAlgorithm
from quad_garl.reinforcement_learning import ReinforcementLearning

sys.path.append("../")
from quad_garl import controller_manual, gui, quadcopter

# Constants
TIME_SCALING = 1.0
QUAD_DYNAMICS_UPDATE = 0.002  # seconds
CONTROLLER_DYNAMICS_UPDATE = 0.005  # seconds
run = True


# Catch Ctrl+C to stop threads
def signal_handler(signal, frame):
    global run
    run = False
    print('Stopping')
    sys.exit(0)


signal.signal(signal.SIGINT, signal_handler)

# Logging
log = logging.getLogger("quad-logger")
logging.basicConfig(filename='test.log', level=logging.DEBUG)

# Define the quadcopters
log.info("Create quadcopter definition")
QUADCOPTER = \
    {'q1': {'position': [1, 0, 4], 'orientation': [0, 0, 0], 'L': 0.3, 'r': 0.1, 'prop_size': [10, 4.5], 'weight': 1.2}}

# Make objects for quadcopter, gui and controller
log.info("Create objects for quad, gui and controller")
quad = quadcopter.Quadcopter(QUADCOPTER)
gui_object = gui.GUI(quads=QUADCOPTER)
ctrl = controller_manual.ManualController(get_state=quad.get_position, get_time=quad.get_time,
                                          actuate_motors=quad.set_motor_speeds, quad_identifier='q1')

# Start threads
log.info("Start worker threads for quad and controller")
quad.start_thread(dt=QUAD_DYNAMICS_UPDATE, time_scaling=TIME_SCALING)
ctrl.start_thread(update_rate=CONTROLLER_DYNAMICS_UPDATE, time_scaling=TIME_SCALING)

# Set up RL and GA framework
log.info("Initialize RL and GA frameworks")
rl = ReinforcementLearning()
ga = GeneticAlgorithm()

throttle = [3000, 3000, 3000, 3000]
target_state = [2, 2, 2, 0, 0, 0]
i = 0
while run:
    log.info("Iteration: {}".format(i))

    # Get quad state
    log.info("Get quad state")
    old_quad_state = np.array([quad.get_position('q1'), quad.get_orientation('q1')]).flatten()
    rl.update_tensor_data(_tensor=rl.input_tensor, _data=old_quad_state)

    # Predict throttle from state
    log.info("Predict throttle from state")
    y_pred = rl.model(rl.input_tensor)
    throttle = list(map(lambda x: x * 1000, y_pred.data.numpy()))

    # Set throttle
    log.info("Apply throttle to quad: {}".format(throttle))
    ctrl.update_throttle(throttle=throttle)

    # Get new quad state
    log.info("Get new state")
    new_quad_state = np.array([quad.get_position('q1'), quad.get_orientation('q1')]).flatten()

    # Get reward
    rl.update_reward(curr_state=new_quad_state, target_state=target_state)

    # GUI update
    log.info("Update GUI")
    gui_object.quads['q1']['position'] = quad.get_position('q1')
    gui_object.quads['q1']['orientation'] = quad.get_orientation('q1')
    gui_object.update()

    i += 1
    if i > 100:
        run = False
        break

quad.stop_thread()
ctrl.stop_thread()
