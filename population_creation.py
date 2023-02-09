from fitness_functions import compute_fitness
from mating_pool_functions import choose_parents
from mutation_functions import mutation


def generate_sample():
    """
    Returns a random morphology of an individual of the population
    """
    return ...


class Individual:
    def __init__(self, morphology=None):
        if morphology is None:
            self.morphology = generate_sample()
        else:
            self.morphology = morphology

    def fitness(self):
        return compute_fitness(self.morphology)

    def mutate(self, mutation_rate):
        self.morphology = mutation(self.morphology, mutation_rate)

    def __str__(self):
        return f"Individual: {self.morphology}"


class Population:
    def __init__(self, population_individuals=None):
        if population_individuals is None:
            self.population_individuals = []
        else:
            self.population_individuals = population_individuals
        self.fitness_values = []

    def add_individual(self, new_individual):
        self.population_individuals.append(new_individual)

    def __len__(self):
        return len(self.population_individuals)

    def fitness(self):
        for individual in self.population_individuals:
            self.fitness_values.append(individual.fitness())

    def choose_parents(self):
        parent_1, parent_2 = choose_parents(self.population_individuals, self.fitness_values)
        return parent_1, parent_2

    def __str__(self):
        return f"{[str(individual) for individual in self.population_individuals]}"


def generate_population(size):
    random_population = Population()
    for _ in range(size):
        current_individual = Individual()
        random_population.add_individual(current_individual)

    return random_population


if __name__ == "__main__":
    pop = generate_population(3)
    for i in pop.population_individuals:
        print(i)