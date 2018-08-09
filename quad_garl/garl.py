from typing import List

from quad_garl import quad_utils
from quad_garl.garl_utils import GARLUtils
from quad_garl.genetic_algorithm import GeneticAlgorithm
from quad_garl.quad_simulator import Quadcopter
from quad_garl.reinforcement_learning import ReinforcementLearning


def main():
    # Variables
    chromosome_size = 10  # type:int
    generations = 10  # type:int
    population_size = 20  # type:int
    selection_percent = 0.3  # type:float
    target_pose = [2, 2, 2, 0, 0, 3.14]  # type: List # x,y,z,r,p,y

    # Logging
    log = quad_utils.quad_logger

    # Set up RL, GA, Quad framework
    log(log_data="Initialize RL and GA frameworks")
    quad_sim = Quadcopter(log, target_pose)
    ga = GeneticAlgorithm(log, chromosome_size, generations, population_size, selection_percent)
    rl = ReinforcementLearning(log)
    utils = GARLUtils(genetic_algorithm=ga, reinforcement_learning=rl)
    log(None)

    i = 0
    while i < 10:
        log("Iteration {}".format(i))

        # Create population
        ga.initialize_population()

        # Evaluate current population
        pop = ga.population
        for each_population in pop:
            print(each_population)
            pass

        i += 1
        log(None)


if __name__ == '__main__':
    main()
