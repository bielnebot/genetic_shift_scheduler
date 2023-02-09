import numpy as np


def choose_parents(population, fitness):
    """

    :param population: list of instances of the class Individual
    :param fitness: list of numeric values representing the fitness of each individual
    :return: two instances of the class Individual
    """

    fitness_array = np.array(fitness)
    normalized_fitness = fitness_array / sum(fitness_array)
    cumulative_fitness = np.cumsum(normalized_fitness)

    # Parent 1
    threshold = np.random.rand()
    elem_index = np.where(cumulative_fitness > threshold)

    parent_1_index = elem_index[0][0]

    # Parent 2
    threshold = np.random.rand()
    elem_index = np.where(cumulative_fitness > threshold)
    parent_2_index = elem_index[0][0]

    # Make sure parent 1 and parent 2 are different
    while parent_1_index == parent_2_index:
        threshold = np.random.rand()
        elem_index = np.where(cumulative_fitness > threshold)
        parent_2_index = elem_index[0][0]

    return population[parent_1_index], population[parent_2_index]