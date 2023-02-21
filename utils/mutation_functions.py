import numpy as np
import random
import itertools


def mutation(initial_morphology, mutation_rate, problem_parameters):
    """

    :param initial_morphology: numpy array
    :param mutation_rate: float
    :param problem_size:
        amount_workers: int
        amount_shifts: int
    :return: new morphology
    """
    amount_workers, amount_shifts, availability_matrix, requirements_matrix = problem_parameters

    for _ in range(int(amount_workers/2)):
        if np.random.rand() < mutation_rate:
            if np.random.rand() < 0.5:
                # Exchange
                initial_morphology = mutation_exchange_shifts(initial_morphology, problem_parameters)
            else:
                # Volunteer
                initial_morphology = mutation_volunteer(initial_morphology, problem_parameters)

    return initial_morphology


def find_workers_that_could_volunteer(input_morphology, problem_parameters):

    amount_workers, amount_shifts, availability_matrix, requirements_matrix = problem_parameters

    current_occupation = input_morphology.sum(axis=1)
    total_availability = availability_matrix.sum(axis=1)

    # Workers with free shifts
    workers_with_free_shifts = np.where(total_availability - current_occupation > 0.5)[0]

    # Workers that work less shifts than the average
    min_threshold = 5                              # Useful when workers self organize
    min_threshold = np.mean(current_occupation)    # Useful when using max assignment to low available workers
    workers_that_work_less = np.where(current_occupation < min_threshold)[0]

    return list(set(workers_with_free_shifts).intersection(workers_that_work_less))


def find_spots_to_volunteer_for(input_morphology, problem_parameters):

    amount_workers, amount_shifts, availability_matrix, requirements_matrix = problem_parameters

    must_have_break_1 = [4, 5, 6, 7]
    must_have_break_2 = [16, 17, 18, 19]
    must_have_break_3 = [28, 29, 30, 31]
    must_have_break = [must_have_break_1, must_have_break_2, must_have_break_3]

    day_1 = [0, 11]  # 0 and 11 included
    day_2 = [12, 23]  # 12 and 23 included
    day_3 = [24, 35]
    days = [day_1, day_2, day_3]

    set_of_candidate_spots = []
    for worker_i in range(amount_workers):

        # Lunch break
        for break_i in must_have_break:
            if input_morphology[worker_i, break_i].sum() > (len(must_have_break_1) - 1):
                for break_shift in break_i:
                    set_of_candidate_spots.append((worker_i, break_shift))

        # Min work time in single day
        for day in days:
            today_shifts = input_morphology[worker_i, day[0]:day[1] + 1]
            if (today_shifts.sum() < 1.5) and (today_shifts.sum() > 0.5):  # (<--> != 1)
                set_of_candidate_spots.append((worker_i, day[0] + np.where(today_shifts > 0.5)[0][0]))

    return set_of_candidate_spots


def find_candidates_for_each_spot(morphology, set_of_candidate_spots, set_of_candidate_workers):

    potential_candidates_for_each_spot = []

    for candidate_spot in set_of_candidate_spots:
        worker_i, shift_i = candidate_spot
        local_candidates_of_spot = []

        for candidate_i in set_of_candidate_workers:
            if (morphology[candidate_i, shift_i] < 0.5) and (candidate_i != worker_i):
                local_candidates_of_spot.append(candidate_i)

        potential_candidates_for_each_spot.append(local_candidates_of_spot)

    return potential_candidates_for_each_spot


def mutation_volunteer(input_morphology,problem_parameters):

    amount_workers, amount_shifts, availability_matrix, _ = problem_parameters

    # Lunch, isolated shifts in a day, workers with high work load
    candidate_spots_to_be_replaced = find_spots_to_volunteer_for(input_morphology, problem_parameters)

    # workers with light work load that have free shifts
    candidate_workers_to_volunteer = find_workers_that_could_volunteer(input_morphology, problem_parameters)

    potential_candidates_for_each_spot = find_candidates_for_each_spot(input_morphology, candidate_spots_to_be_replaced, candidate_workers_to_volunteer)
    amount_of_potential_candidates_for_each_spot = [len(i) for i in potential_candidates_for_each_spot]

    # Choose random spot that has potential volunteers
    randomly_sorted_spot_indexes = np.arange(len(candidate_spots_to_be_replaced))
    np.random.shuffle(randomly_sorted_spot_indexes)
    spot_not_found = True
    for rand_spot_index in randomly_sorted_spot_indexes:
        amount_of_potential_candidates_for_that_spot = amount_of_potential_candidates_for_each_spot[rand_spot_index]
        if amount_of_potential_candidates_for_that_spot > 0.5:
            spot_not_found = False
            break

    if not spot_not_found:

        worker_1, shift_1 = candidate_spots_to_be_replaced[rand_spot_index]
        volunteer = np.random.choice(potential_candidates_for_each_spot[rand_spot_index])

        # Volunteering takes place
        input_morphology[worker_1, shift_1] = 0
        input_morphology[volunteer, shift_1] = 1

    return input_morphology


def mutation_exchange_shifts(input_morphology,problem_parameters):
    # Let workers exchange shifts

    amount_workers, amount_shifts, availability_matrix, _ = problem_parameters

    currently_worked_by_w1 = []
    currently_worked_by_w2 = []

    workers_with_free_shifts = list(np.where(availability_matrix.sum(axis=1) - input_morphology.sum(axis=1) > 0)[0])
    unchecked_combinations = list(itertools.combinations(workers_with_free_shifts, 2))

    while len(unchecked_combinations) > 0 and ((len(currently_worked_by_w1) == 0) or (len(currently_worked_by_w2) == 0)):
        worker_1, worker_2 = random.choice(unchecked_combinations)
        unchecked_combinations.remove((worker_1, worker_2))

        current_working_shifts_w1 = np.where(input_morphology[worker_1] > 0.5)[0]
        current_working_shifts_w2 = np.where(input_morphology[worker_2] > 0.5)[0]

        available_working_shifts_w1 = np.where(availability_matrix[worker_1] > 0.5)[0]
        available_working_shifts_w2 = np.where(availability_matrix[worker_2] > 0.5)[0]

        free_working_shifts_w1 = set(available_working_shifts_w1).difference(current_working_shifts_w1)
        free_working_shifts_w2 = set(available_working_shifts_w2).difference(current_working_shifts_w2)

        currently_worked_by_w1 = set(current_working_shifts_w1).intersection(free_working_shifts_w2)
        currently_worked_by_w2 = set(current_working_shifts_w2).intersection(free_working_shifts_w1)

    if (len(currently_worked_by_w1) == 0) or (len(currently_worked_by_w2) == 0):
        pass
    else:
        currently_worked_by_w1 = random.sample(list(currently_worked_by_w1), 1)[0]
        currently_worked_by_w2 = random.sample(list(currently_worked_by_w2), 1)[0]

        input_morphology[worker_1, currently_worked_by_w1] = 0
        input_morphology[worker_1, currently_worked_by_w2] = 1

        input_morphology[worker_2, currently_worked_by_w2] = 0
        input_morphology[worker_2, currently_worked_by_w1] = 1

    return np.array(input_morphology)
