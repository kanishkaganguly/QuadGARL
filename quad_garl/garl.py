import logging
import random
from typing import List

from quad_garl.garl_utils import GARLUtils
from quad_garl.genetic_algorithm import GeneticAlgorithm
from quad_garl.quad_simulator import Quadcopter
from quad_garl.reinforcement_learning import ReinforcementLearning

# Logging
log = logging.getLogger("quad-logger")
logging.basicConfig(filename='test.log', level=logging.DEBUG)

# Variables
chromosome_size = 10  # type:int
generations = 10  # type:int
population_size = 20  # type:int
selection_percent = 0.3  # type:float
target_state = [2, 2, 2, 0, 0, 3.14]  # type: List # x,y,z,r,p,y

# Set up RL, GA, Quad framework
log.info("Initialize RL and GA frameworks")
quad_sim = Quadcopter(log, target_state)
ga = GeneticAlgorithm(log, chromosome_size, generations, population_size, selection_percent)
rl = ReinforcementLearning(log)
utils = GARLUtils(genetic_algorithm=ga, reinforcement_learning=rl)

i = 0
while i < 10:
    print("Iteration {}".format(i))
    quad_sim.apply_throttle(throttle=random.sample(range(4000, 9000), 4))

    # # Create population
    # ga.initialize_population()
    #
    # # Evaluate current population
    # pop = ga.population
    # for each_population in pop:
    #     print(each_population)
    #     pass

    i += 1
    print()
