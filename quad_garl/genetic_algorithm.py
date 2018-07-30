import numpy as np


class GeneticAlgorithm:
    def __init__(self, chromosome_size, generations, population_size):
        self.chromosome_size = chromosome_size
        self.generations = generations
        self.population_size = population_size
        self.population = np.zeros(shape=(self.population_size, self.chromosome_size))

    def initialize_population(self):
        self.population = np.random.rand(self.population_size, self.chromosome_size)
        print(self.population)

    def evaluate(self):
        return

    def select(self):
        return

    def crossover(self):
        return

    def mutate(self):
        return


if __name__ == '__main__':
    ga = GeneticAlgorithm(chromosome_size=10, generations=10, population_size=20)
    ga.initialize_population()
