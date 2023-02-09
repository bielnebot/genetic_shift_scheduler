from population_creation import generate_population, Population
from crossover_functions import crossover


def run_evolution(population_size, amount_iterations, mutation_rate):

    population = generate_population(population_size)

    for iteration in range(amount_iterations):
        # Calculate fitness
        population.fitness()

        # print(f"{population}\n{population.fitness_values}")
        # print(f"iteration {iteration}   average fitness: {np.mean(population.fitness_values)}    max fitness: {np.max(population.fitness_values)}\n")

        # The new population
        new_population = Population()
        for _ in range(population_size):
            # Selection
            parent_1, parent_2 = population.choose_parents()
            # print(f"Parents are: {parent_1} and {parent_2}")
            # Reproduction
            offspring = crossover(parent_1, parent_2)
            offspring.mutate(mutation_rate)
            # print(f"Offspring is {offspring}")
            new_population.add_individual(offspring)

        population = new_population

    return population


if __name__ == "__main__":
    run_evolution(population_size=5,
                  amount_iterations=3,
                  mutation_rate=0.01)