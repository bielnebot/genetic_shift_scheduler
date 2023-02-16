import numpy as np
from utils.fitness_functions import compute_fitness
from utils.mating_pool_functions import choose_parents
from utils.mutation_functions import mutation


def generate_sample_old(problem_parameters):
    """
    Returns a random morphology of an individual of the population
    """
    amount_workers, amount_activities, amount_shifts, availability_matrix, _ = problem_parameters

    solution_matrix = np.zeros((amount_workers,amount_activities,amount_shifts))
    is_working = np.random.randint(low=0, high=2, size=(amount_workers,amount_shifts))
    # is_working = np.ones((amount_workers, amount_shifts))
    is_working = np.multiply(is_working, availability_matrix)
    where_is_working = np.random.randint(low=0, high=amount_activities, size=(amount_workers,amount_shifts))

    for shift_i in range(amount_shifts):
        for worker_i in range(amount_workers):
            solution_matrix[worker_i, where_is_working[worker_i, shift_i], shift_i] = is_working[worker_i, shift_i]

    return solution_matrix


def generate_sample(problem_parameters):
    """
    Returns a random morphology of an individual of the population
    """
    amount_workers, amount_activities, amount_shifts, availability_matrix, requirements_matrix = problem_parameters

    solution_matrix = np.zeros((amount_workers, amount_activities, amount_shifts))

    # Access shifts and activities in a random order
    randomly_ordered_shifts = np.arange(amount_shifts)
    np.random.shuffle(randomly_ordered_shifts)

    randomly_ordered_activities = np.arange(amount_activities)
    np.random.shuffle(randomly_ordered_activities)

    for shift_i in randomly_ordered_shifts:
        available_workers = availability_matrix[:, shift_i].astype(int)
        num_available_workers = int(available_workers.sum())
        for activity_i in randomly_ordered_activities:
            # print(f"\nshift = {shift_i} activity = {activity_i}")
            num_required_workers = int(requirements_matrix[activity_i, shift_i])
            # print(f"{num_required_workers} required and {num_available_workers}  available")
            if num_available_workers > 0:
                for i in range(min(num_required_workers, num_available_workers)):
                    # print(f"choose from: {available_workers}")
                    index_free_workers = np.where(available_workers > 0.5)[0]
                    # print(f"indexs available: {index_free_workers}")
                    new_worker_index = np.random.choice(index_free_workers)
                    # print(f"{new_worker_index} was selected")

                    solution_matrix[new_worker_index, activity_i, shift_i] = 1

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
        self.fitness_values = []
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
    pop = generate_population(3)
    for i in pop.population_individuals:
        print(i)