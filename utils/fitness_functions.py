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

    # requirements_fit = fitness_requirements_are_satisfied(requirements_matrix, morphology)
    # proportion_above_min, proportion_under_max = fitness_min_and_max_shifts_threshold(5, 15, morphology, amount_workers)

    fit_groups = fitness_packed_schedule(morphology, amount_workers, amount_shifts)

    return (fit_groups)**3


def fitness_requirements_are_satisfied(requirements_matrix, morphology):
    """
    Compares an individual with the requirements_matrix to make sure there is no missing or exceeding staff
    """
    filled_slots = morphology.sum(axis=0)
    empty_slots = abs(requirements_matrix - filled_slots).astype(int)
    # sum_required_slots = requirements_matrix.sum()

    a, b = requirements_matrix.shape

    # sum_empty_slots = empty_slots.sum() # count missing and exceeding ones
    # sum_empty_slots = ((empty_slots > 0) * empty_slots).sum() # just count the missing ones

    # return min(1, 0.1*sum_required_slots / sum_empty_slots)
    # return max(1e-100, (-1/sum_required_slots)* sum_empty_slots + 1)

    return 1 - empty_slots.astype(bool).sum()/(a*b)


def fitness_respect_availability(morphology, availability_matrix, amount_workers, amount_shifts):
    """
    Computes the proportion of workers*shifts that work at the time they are available

    Matrix difference_new:
    0 = available and works // not available and doesn't work
    1 = available and doesn't work
    -1 = not available and works
    """

    new_sum_workers = morphology.sum(axis=1).astype(int)
    difference_new = availability_matrix - new_sum_workers

    # print(difference_new)

    for fila in range(difference_new.shape[0]):
        for column in range(difference_new.shape[1]):
            if difference_new[fila, column] >= 0:
                difference_new[fila, column] = 1
            else:
                difference_new[fila, column] = 0

    mark = difference_new.sum() / (amount_workers * amount_shifts)
    return mark


def fitness_min_and_max_shifts_threshold(min_threshold, max_threshold, morphology, amount_workers):
    count_workers_above_min_threshold = 0
    count_workers_under_max_threshold = 0

    for worker_i in range(amount_workers):
        worked_shifts = morphology[worker_i].sum()

        if worked_shifts > min_threshold:
            count_workers_above_min_threshold += 1
        if worked_shifts < max_threshold:
            count_workers_under_max_threshold += 1

    return count_workers_above_min_threshold / amount_workers, count_workers_under_max_threshold / amount_workers


def fitness_packed_schedule(morphology,amount_workers, amount_shifts):

    workers_match_condition = 0
    for worker_i in range(amount_workers):
        worked_shifts = morphology[worker_i].sum(axis=0)

        groups_in_schedule = count_groups_of_ones(worked_shifts)
        max_possible_groups = amount_shifts // 2 + amount_shifts % 2
        max_allowed_groups = 4

        y = (-1)/(max_possible_groups - max_allowed_groups) * groups_in_schedule - max_possible_groups * (-1)/(max_possible_groups - max_allowed_groups)

        if min(1, y) > 0.9:
            workers_match_condition += 1

    return workers_match_condition / amount_workers


def count_groups_of_ones(sample_array):
    """
    Count of groups of consecutive 1s in a vector
    sample_array = [0 0 0 1 1 0 1 1 1 0 1 0 1 1 0 1 1] ----> 5
    :param sample_array: numpy array
    :return:
    """
    count_starting_ones = 0
    currently_zero = True

    for i in range(len(sample_array)):
        current_value = sample_array[i]

        if currently_zero and current_value == 1:
            count_starting_ones += 1
            currently_zero = False
        else:
            if current_value == 0:
                currently_zero = True

    return count_starting_ones
