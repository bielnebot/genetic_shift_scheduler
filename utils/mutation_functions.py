import numpy as np


def mutation_old(initial_morphology, mutation_rate, problem_parameters):
    """

    :param initial_morphology: numpy array
    :param mutation_rate: float
    :param problem_size:
        amount_workers: int
        amount_activities: int
        amount_shifts: int
    :return: new morphology
    """

    min_amount_shifts_allowed = 1
    max_amount_shifts_allowed = 100

    amount_workers, amount_activities, amount_shifts, availability_matrix = problem_parameters

    for worker_i in range(amount_workers):
        shifts_worked_by_current_worker = initial_morphology[worker_i].sum()
        available_shifts_by_current_worker = availability_matrix[worker_i].sum()

        for shift_i in range(amount_shifts):
            if availability_matrix[worker_i,shift_i] > 0.5:
                if np.random.rand() < mutation_rate:

                    if shifts_worked_by_current_worker <= min_amount_shifts_allowed:
                        if available_shifts_by_current_worker > shifts_worked_by_current_worker:

                            shifts_currently_active = initial_morphology[worker_i].sum(axis=0)
                            new_shift = select_new_position(worker_i, shifts_currently_active, availability_matrix)
                            new_activity = np.random.randint(amount_activities)
                            initial_morphology[worker_i, new_activity, new_shift] = 1
                            break
                    elif shifts_worked_by_current_worker >= max_amount_shifts_allowed:

                        shifts_currently_active = initial_morphology[worker_i].sum(axis=0)
                        existing_shift = select_existing_position(shifts_currently_active)
                        initial_morphology[worker_i, :, existing_shift] = 0
                        break
                    else:
                        if np.random.rand() < 0.5:  # 50 % chance on the type of mutation
                            # print("works - doesn't work")
                            if sum(initial_morphology[worker_i, :, shift_i]) > 0.9:  # if works
                                initial_morphology[worker_i, :, shift_i] = np.zeros(amount_activities)
                            else: # if doesn't work
                                new_vector = np.zeros(amount_activities)
                                new_activity = np.random.randint(amount_activities)
                                new_vector[new_activity] = 1
                                initial_morphology[worker_i, :, shift_i] = new_vector
                        else:
                            # print("change of activity")
                            if sum(initial_morphology[worker_i, :, shift_i]) > 0.9:
                                initial_morphology[worker_i, :, shift_i] = change_activity(initial_morphology[worker_i, :, shift_i], amount_activities)
    return initial_morphology


def mutation(initial_morphology, mutation_rate, problem_parameters):

    amount_workers, amount_activities, amount_shifts, availability_matrix, requirements_matrix = problem_parameters

    # Find the shifts with missing or exceeding workers available
    available_vs_required = abs(availability_matrix.sum(axis=0) - requirements_matrix.sum(axis=0))
    flexible_shifts = np.where(available_vs_required > 0.5)[0] # shifts with missing or exceeding workers = [0 1 4 5 8 39]

    for shift_i in flexible_shifts:
        if np.random.rand() < mutation_rate:
            # Redistribute activities between available workers in a random way
            requirements_vector = requirements_matrix[:, shift_i].copy()  # [0 1 2 2]
            current_distribution = initial_morphology[:, :, shift_i]  # matrix activity x worker

            available_workers = availability_matrix[:, shift_i].copy()  # [1 1 0 1 1]

            # OPTIONAL: make sure new_activity_worker != starting one
            # current_workers_working = current_distribution.sum(axis=1)

            new_activity_worker = np.zeros(current_distribution.shape)
            for i in range(min(available_workers.astype(int).sum(), requirements_vector.astype(int).sum())):

                # Choose activity
                index_pending_activity = np.where(requirements_vector > 0.5)[0]  # [0 1 3 4]
                chosen_activity = np.random.choice(index_pending_activity)
                requirements_vector[chosen_activity] -= 1

                # Choose worker
                index_available_workers = np.where(available_workers > 0.5)[0]  # [0 1 3 4]

                chosen_worker = np.random.choice(index_available_workers)
                available_workers[chosen_worker] = 0

                new_activity_worker[chosen_worker, chosen_activity] = 1

            initial_morphology[:,:,shift_i] = new_activity_worker

    return initial_morphology


def change_activity(vector, amount_activities):
    """
    Changes the position of the 1 in the array.
    Eg: [0 1 0 0 0] ---> [0 0 0 0 1]

    :param vector: numpy array
    :param amount_activities: int
    :return: numpy array
    """

    # Find current working activity
    elem_index = np.where(vector > 0.9)

    # Pick new activity
    activity_number = np.random.randint(amount_activities)

    # Make sure the new activity is different from the current
    while activity_number == elem_index[0][0]:
        activity_number = np.random.randint(amount_activities)

    # Build the new vector
    new_vector = np.zeros(amount_activities)
    new_vector[activity_number] = 1
    return new_vector


def select_new_position(worker_number, shifts_currently_active, availability_matrix):
    """
    worker_number = 3
    shifts_currently_active =            [0 0 1 1 0 1]
    availability_matrix[worker_number] = [0 1 1 1 1 1]
    remaining_shifts =                   [0 1 0 0 1 0] are the shifts that can be still picked

    Adds a shift to shifts_currently_active. That would either be [0 0 1 1 1 1] or [0 1 1 1 0 1]

    The function returns a random index of the ones in remaining_shifts

    :param worker_number: int
    :param shifts_currently_active: numpy array
    :param availability_matrix:  numpy array
    :return: int
    """
    remaining_shifts = availability_matrix[worker_number] - shifts_currently_active
    index_remaining_shifts = np.where(remaining_shifts > 0.5)[0]
    new_shift_index = np.random.choice(index_remaining_shifts)

    return new_shift_index


def select_existing_position(shifts_currently_active):
    """
    shifts_currently_active = [0 0 1 1 0 1]
    The function returns a random index of the ones in shifts_currently_active

    :param shifts_currently_active: numpy array
    :return: int
    """
    index_existing_shifts = np.where(shifts_currently_active > 0.5)[0]
    existing_shift_index = np.random.choice(index_existing_shifts)

    return existing_shift_index
