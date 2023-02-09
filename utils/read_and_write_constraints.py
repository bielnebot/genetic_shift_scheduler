import numpy as np


def create_matrix_file(sample_matrix, type_of_matrix):
    """
    Creates a file containing a matrix
    :param sample_matrix: list of lists
    :param type_of_matrix: str. Either "availability" or "requirements"
    :return: -
    """
    if type_of_matrix in ["availability", "requirements"]:
        mat = np.array(sample_matrix)
        with open(f"utils/constraints_files/{type_of_matrix}.txt", "wb") as f:
            np.savetxt(f, mat)
    else:
        raise Exception("Invalid type of matrix")


def load_matrix_file(type_of_matrix):
    """
    Loads a matrix from a txt file
    :param type_of_matrix: str. Either "availability" or "requirements"
    :return: numpy array
    """
    if type_of_matrix in ["availability", "requirements"]:
        with open(f"utils/constraints_files/{type_of_matrix}.txt", "r") as f:
            mat = np.loadtxt(f)
        return mat
    else:
        raise Exception("Invalid type of matrix")


def retrieve_constraints():
    """
    Returns all the problem constraints and size parameters
    :return: tuple
    """
    availability_matrix = load_matrix_file("availability")
    requirements_matrix = load_matrix_file("requirements")

    amount_workers, amount_shifts = availability_matrix.shape
    amount_activities, _ = requirements_matrix.shape

    return amount_workers, amount_activities, amount_shifts, availability_matrix, requirements_matrix


if __name__ == "__main__":

    availability_mat = [[1,1,1,1,0],
                        [0,0,1,1,1],
                        [1,1,0,0,0]]

    requirements_mat = [[3,1,1,0,0],
                        [0,0,1,1,1],
                        [0,1,2,2,0],
                        [0,0,0,2,2]]

    create_matrix_file(sample_matrix=availability_mat,
                       type_of_matrix="availability")
    create_matrix_file(sample_matrix=requirements_mat,
                       type_of_matrix="requirements")

    print(retrieve_constraints())