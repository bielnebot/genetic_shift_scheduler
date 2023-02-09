import numpy as np


def mutation(initial_morphology, mutation_rate, problem_size):
    """

    :param initial_morphology: numpy array
    :param mutation_rate: float
    :param problem_size:
        amount_workers: int
        amount_activities: int
        amount_shifts: int
    :return: new morphology
    """
    amount_workers, amount_activities, amount_shifts = problem_size

    for shift_i in range(amount_shifts):
        for worker_i in range(amount_workers):
            # print(shift_i, worker_i)
            if np.random.rand() < mutation_rate:
                # print(shift_i, worker_i,"mutates")
                if np.random.rand() < 0.5:  # 50 % chance on the type of mutation
                    # print("works - doesn't work")
                    if sum(initial_morphology[shift_i, worker_i, :]) > 0.9: # if works
                        initial_morphology[shift_i, worker_i, :] = np.zeros(amount_activities)
                    else: # if doesn't work
                        new_vector = np.zeros(amount_activities)
                        activity_number = np.random.randint(amount_activities)
                        new_vector[activity_number] = 1
                        initial_morphology[shift_i, worker_i, :] = new_vector
                else:
                    # print("change of activity")
                    if sum(initial_morphology[shift_i, worker_i, :]) > 0.9:
                        initial_morphology[shift_i, worker_i, :] = change_activity(initial_morphology[shift_i, worker_i, :],amount_activities)
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
