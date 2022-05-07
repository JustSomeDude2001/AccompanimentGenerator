import random

from Environment import Environment
from Individual import Individual


class Population:
    # Only constructor needs size of population and size of individual in chords
    def __init__(self, size, individual_size):
        self.individuals = []
        for i in range(size):
            self.individuals.append(Individual(type='random', size=individual_size))

    # Pruning population is removing the population with lower fitness until a target population size reached
    def prune(self, environment: Environment, target_size):
        individuals_sorted = []
        for individual in self.individuals:
            individuals_sorted.append((environment.get_fitness(individual), individual))

        individuals_sorted.sort(key=lambda a: a[0], reverse=True)
        while len(individuals_sorted) > target_size:
            individuals_sorted.pop()

        self.individuals = [individual[1] for individual in individuals_sorted]

    # This method increases population by splicing until a target size reached.
    def populate_offspring(self, target_size, splicing_method):
        for i in range(target_size - len(self.individuals)):
            parent_a = random.choice(self.individuals)
            parent_b = random.choice(self.individuals)
            self.individuals.append(Individual(type="splice", splicing_method=splicing_method,
                                               parent_a=parent_a,
                                               parent_b=parent_b))

    def populate_outsiders(self):
        pass

    def mutate(self, magnitude: int):
        for i in range(len(self.individuals)):
            self.individuals[i].mutate(magnitude)



