import numpy as np
from utils.fitness_functions import compute_fitness
from utils.mating_pool_functions import choose_parents
from utils.mutation_functions import mutation


def generate_sample(problem_parameters):
    """
    Returns a random morphology of an individual of the population
    """
    amount_workers, amount_activities, amount_shifts, _, _ = problem_parameters

    solution_matrix = np.zeros((amount_shifts, amount_workers, amount_activities))
    is_working = np.random.randint(low=0, high=2, size=(amount_shifts * amount_workers))
    where_is_working = np.random.randint(low=0, high=amount_activities, size=(amount_shifts * amount_workers))

    iteration_count = 0
    for shift_i in range(amount_shifts):
        for worker_i in range(amount_workers):
            solution_matrix[shift_i, worker_i, where_is_working[iteration_count]] = is_working[iteration_count]
            iteration_count += 1

    return solution_matrix


class Individual:
    def __init__(self, problem_parameters, morphology=None):
        if morphology is None:
            self.morphology = generate_sample(problem_parameters)
        else:
            self.morphology = morphology
        self.amount_workers = problem_parameters[0]
        self.amount_activities = problem_parameters[1]
        self.amount_shifts = problem_parameters[2]
        self.availability_matrix = problem_parameters[3]
        self.requirements_matrix = problem_parameters[4]
        self.problem_parameters = problem_parameters

    def fitness(self):
        return compute_fitness(self.morphology, self.problem_parameters)

    def mutate(self, mutation_rate):
        self.morphology = mutation(self.morphology,
                                   mutation_rate,
                                   (self.amount_workers, self.amount_activities, self.amount_shifts))

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

    def fitness(self,):
        for individual in self.population_individuals:
            self.fitness_values.append(individual.fitness())

    def choose_parents(self):
        parent_1, parent_2 = choose_parents(self.population_individuals, self.fitness_values)
        return parent_1, parent_2

    def __str__(self):
        return f"{[str(individual) for individual in self.population_individuals]}"


def generate_population(size, problem_parameters):
    random_population = Population()
    for _ in range(size):
        current_individual = Individual(problem_parameters)
        random_population.add_individual(current_individual)

    return random_population


if __name__ == "__main__":
    pop = generate_population(3)
    for i in pop.population_individuals:
        print(i)