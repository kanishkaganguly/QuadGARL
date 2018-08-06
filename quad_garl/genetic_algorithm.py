import math

import numpy as np


class GeneticAlgorithm:
    def __init__(self, log, chromosome_size, generations, population_size, selection_percent):
        # Logging
        self.log = log

        self._chromosome_size = chromosome_size
        self._generations = generations
        self._population_size = population_size
        self._selection_percent = selection_percent
        self._population = np.zeros(shape=(self._population_size, self._chromosome_size))
        self._fitness = np.zeros(self._population_size).flatten()
        self._num_chromosomes_to_select = math.ceil(self._selection_percent * self._population_size)

    @property
    def population(self) -> np.array:
        return self._population

    def initialize_population(self):
        self._population = np.random.rand(self._population_size, self._chromosome_size)
        self._fitness = np.random.rand(self._population_size).flatten()

    def select(self):
        population_with_fitness = list(zip(self.population, self._fitness))
        sorted_population_with_fitness = (sorted(population_with_fitness, key=lambda t: t[1])[::-1])[
                                         :self._num_chromosomes_to_select]

    def update_fitness_value(self, fitness_value: float, idx_to_update: int):
        self._fitness[idx_to_update] = fitness_value

    def crossover(self):
        return

    def mutate(self):
        return

# if __name__ == '__main__':
#     ga = GeneticAlgorithm(log=None, chromosome_size=10, generations=10, population_size=20, selection_percent=0.3)
#     ga.initialize_population()
#     ga.select()
