import numpy as np
from utils.mutation_functions import find_spots_to_volunteer_for

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

    amount_workers, amount_shifts, availability_matrix, requirements_matrix = problem_parameters

    fit_groups = fitness_packed_schedule(morphology, amount_workers, amount_shifts)
    #
    # min_threshold = 7
    # max_threshold = 15
    # fit_min, fit_max = fitness_min_and_max_shifts_threshold(min_threshold, max_threshold, morphology, amount_workers)

    fit_volunteer = fitness_volunteer_spots(morphology,problem_parameters)

    return (0.95*fit_groups+0.05*fit_volunteer)**5


def fitness_min_and_max_shifts_threshold(min_threshold, max_threshold, morphology, amount_workers):
    count_workers_above_min_threshold = 0
    count_workers_under_max_threshold = 0

    for worker_i in range(amount_workers):
        worked_shifts = morphology[worker_i].sum()

        if worked_shifts >= min_threshold:
            count_workers_above_min_threshold += 1
        if worked_shifts <= max_threshold:
            count_workers_under_max_threshold += 1

    return count_workers_above_min_threshold / amount_workers, count_workers_under_max_threshold / amount_workers


def fitness_packed_schedule(morphology, amount_workers, amount_shifts):

    workers_match_condition = 0
    for worker_i in range(amount_workers):
        worked_shifts = morphology[worker_i]

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


def fitness_volunteer_spots(morphology,problem_parameters):
    return 1 - len(find_spots_to_volunteer_for(morphology,problem_parameters)) / 570
