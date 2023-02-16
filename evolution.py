import numpy as np
from utils.read_and_write_constraints import retrieve_constraints
from utils.population_creation import generate_population, Population
from utils.crossover_functions import crossover


def run_evolution(population_size, amount_iterations, mutation_rate):

    problem_parameters = retrieve_constraints()

    population = generate_population(population_size, problem_parameters)

    for iteration in range(amount_iterations):
        # Calculate fitness
        population.fitness()

        # print(f"{population}\n{population.fitness_values}")
        print(f"iteration {iteration}   average fitness: {np.mean(population.fitness_values)}    max fitness: {np.max(population.fitness_values)}\n")


        # The new population
        new_population = Population()
        for i in range(population_size):
            # Selection
            parent_1, parent_2 = population.choose_parents()
            # Reproduction
            offspring = crossover(parent_1, parent_2)
            offspring.mutate(mutation_rate)
            # print(f"Offspring is {offspring}")
            new_population.add_individual(offspring)

        population = new_population

    # print(population)
    return population, problem_parameters


if __name__ == "__main__":

    final_population = run_evolution(population_size=500,
                                     amount_iterations=100,
                                     mutation_rate=0.01)