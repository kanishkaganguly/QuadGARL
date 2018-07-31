import math
from typing import List

import numpy as np


class GeneticAlgorithm:
    def __init__(self, log, chromosome_size, generations, population_size, selection_percent):
        # Logging
        self.log = log

        self.chromosome_size = chromosome_size
        self.generations = generations
        self.population_size = population_size
        self.selection_percent = selection_percent
        self.population = np.zeros(shape=(self.population_size, self.chromosome_size))
        self.fitness = np.zeros(self.population_size).flatten()

    def initialize_population(self):
        self.population = np.random.rand(self.population_size, self.chromosome_size)
        self.fitness = np.random.rand(self.population_size).flatten()

    def select(self) -> List[np.array]:
        num_chromosomes_to_select = math.ceil(self.selection_percent * len(self.population))
        fitness_sorted = np.argsort(self.fitness)
        selected_chromosomes = []
        for idx_chromosome, sort_order in enumerate(fitness_sorted):
            if sort_order < num_chromosomes_to_select:
                selected_chromosomes.append(self.population[idx_chromosome])
        return selected_chromosomes

    def crossover(self):
        return

    def mutate(self):
        return


if __name__ == '__main__':
    ga = GeneticAlgorithm(log=None, chromosome_size=10, generations=10, population_size=20, selection_percent=0.3)
    ga.initialize_population()
    ga.select()
