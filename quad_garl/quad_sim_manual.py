#!/usr/bin/env python3
import signal
import sys

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

# Define the quadcopters
QUADCOPTER = {
    'q1': {'position': [1, 0, 4], 'orientation': [0, 0, 0], 'L': 0.3, 'r': 0.1, 'prop_size': [10, 4.5], 'weight': 1.2}}

# Make objects for quadcopter, gui and controller
quad = quadcopter.Quadcopter(QUADCOPTER)
gui_object = gui.GUI(quads=QUADCOPTER)
ctrl = controller_manual.ManualController(get_state=quad.get_position, get_time=quad.get_time,
                                          actuate_motors=quad.set_motor_speeds, quad_identifier='q1')

# Start threads
quad.start_thread(dt=QUAD_DYNAMICS_UPDATE, time_scaling=TIME_SCALING)
ctrl.start_thread(update_rate=CONTROLLER_DYNAMICS_UPDATE, time_scaling=TIME_SCALING)

# Update the GUI
throttle = [3000, 3000, 3000, 3000]
while (run == True):
    throttle = list(map(lambda x: x + 50, throttle))
    ctrl.update_throttle(throttle=throttle)
    gui_object.quads['q1']['position'] = quad.get_position('q1')
    gui_object.quads['q1']['orientation'] = quad.get_orientation('q1')
    # gui_object.update()
quad.stop_thread()
ctrl.stop_thread()
