import numpy as np


def compute_fitness(morphology, problem_parameters):
    """

    :param morphology:
    :param problem_parameters:
        amount_workers: int
        amount_activities: int
        amount_shifts: int
        availability_matrix: numpy array
        requirements_matrix numpy array
    :return: float
    """

    amount_workers, amount_activities, amount_shifts, availability_matrix, requirements_matrix = problem_parameters

    new_sum_workers = np.transpose(morphology.sum(axis=2))
    # print(new_sum_workers)
    difference_new = availability_matrix - new_sum_workers
    # print(difference_new)
    for fila in range(difference_new.shape[0]):
        for column in range(difference_new.shape[1]):
            if difference_new[fila, column] >= 0:
                difference_new[fila, column] = 1
            # elif difference_new[fila,column] == 1:
            #     difference_new[fila,column]=0.5
            else:
                difference_new[fila, column] = 0
    # print(difference_new)
    total = amount_workers * amount_shifts
    mark = sum(sum(difference_new)) / total
    mark = difference_new.sum() / total
    return mark
