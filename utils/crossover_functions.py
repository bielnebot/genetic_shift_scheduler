import numpy as np
from utils.population_creation import Individual


def crossover(parent_1, parent_2):
    """
    Creates a new individual by combining parent 1 and parent 2
    :param parent_1: instances of the class Individual
    :param parent_2: instances of the class Individual
    :return: instances of the class Individual
    """
    amount_shifts = parent_1.amount_shifts
    amount_workers = parent_1.amount_workers
    amount_activities = parent_1.amount_activities

    new_morphology = np.zeros((amount_workers,amount_activities,amount_shifts))

    for i in range(amount_shifts):
        if i % 2 == 0:
            new_morphology[:,:,i] = parent_1.morphology[:,:,i]
        elif i % 2 == 1:
            new_morphology[:,:,i] = parent_2.morphology[:,:,i]

    return Individual(parent_1.problem_parameters, new_morphology)
