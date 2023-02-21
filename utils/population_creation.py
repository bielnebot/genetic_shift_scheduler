import numpy as np
from utils.fitness_functions import compute_fitness
from utils.mating_pool_functions import choose_parents
from utils.mutation_functions import mutation


def generate_sample(problem_parameters):
    """
    Returns a random morphology of an individual of the population
    """
    amount_workers, amount_shifts, availability_matrix, requirements_matrix = problem_parameters

    solution_matrix = np.zeros((amount_workers, amount_shifts))

    # Access shifts in a random order
    randomly_ordered_shifts = np.arange(amount_shifts)
    np.random.shuffle(randomly_ordered_shifts)

    # Map workers to amount of available shifts
    # worker_to_amount_availability = {i:availability_matrix[i].sum() for i in range(amount_workers)}

    for shift_i in randomly_ordered_shifts:
        available_workers = availability_matrix[:, shift_i].astype(int)
        num_available_workers = int(available_workers.sum())

        num_required_workers = int(requirements_matrix[:, shift_i].sum())

        for i in range(min(num_required_workers, num_available_workers)):
            # print(f"choose from: {available_workers}")
            index_free_workers = np.where(available_workers > 0.5)[0]

            # Option 1: start assigning from the least available worker (due to non stochastic selection, all members are the same)
            # local_worker_to_amount_availability = {i: worker_to_amount_availability[i] for i in index_free_workers}
            # new_worker_index = min(local_worker_to_amount_availability, key=local_worker_to_amount_availability.get)
            # print(f"indexs available: {index_free_workers}")

            # Option 2: assign randomly
            new_worker_index = np.random.choice(index_free_workers)
            # print(f"{new_worker_index} was selected")

            solution_matrix[new_worker_index, shift_i] = 1

            available_workers[new_worker_index] = 0
            num_available_workers = int(available_workers.sum())

    return solution_matrix


class Individual:
    def __init__(self, problem_parameters, morphology=None):
        if morphology is None:
            self.morphology = generate_sample(problem_parameters)
        else:
            self.morphology = morphology
        self.amount_workers = problem_parameters[0]
        self.amount_shifts = problem_parameters[1]
        self.availability_matrix = problem_parameters[2]
        self.requirements_matrix = problem_parameters[3]
        self.problem_parameters = problem_parameters

    def fitness(self):
        return compute_fitness(self.morphology, self.problem_parameters)

    def mutate(self, mutation_rate):
        self.morphology = mutation(self.morphology,
                                   mutation_rate,
                                   self.problem_parameters)

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

    def fittest_individual(self):
        best_score = 0
        best_individual = None
        for individual in self.population_individuals:
            if individual.fitness() > best_score:
                best_individual = individual
                best_score = individual.fitness()

        return best_individual, best_score

    def __str__(self):
        return f"{[str(individual) for individual in self.population_individuals]}"


def generate_population(size, problem_parameters):
    random_population = Population()
    for _ in range(size):
        current_individual = Individual(problem_parameters)
        random_population.add_individual(current_individual)

    return random_population


if __name__ == "__main__":
    ...
