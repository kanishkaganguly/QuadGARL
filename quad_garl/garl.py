# Logging
import logging

from quad_garl.genetic_algorithm import GeneticAlgorithm
from quad_garl.quad_simulator import Quadcopter
from quad_garl.reinforcement_learning import ReinforcementLearning

log = logging.getLogger("quad-logger")
logging.basicConfig(filename='test.log', level=logging.DEBUG)

# Variables
chromosome_size = 10  # type:int
generations = 10  # type:int
population_size = 20  # type:int
selection_percent = 0.3  # type:float

# Set up RL, GA, Quad framework
log.info("Initialize RL and GA frameworks")
quad_sim = Quadcopter(log)
ga = GeneticAlgorithm(log, chromosome_size, generations, population_size, selection_percent)
rl = ReinforcementLearning(log)

target_state = [2, 2, 2, 0, 0, 0]

i = 0
while i < 500:
    # Get initial state
    old_state = quad_sim.get_quad_state()

    # Create population
    ga.initialize_population()

    #

    i += 1
