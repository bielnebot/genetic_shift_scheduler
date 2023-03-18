import numpy as np
import matplotlib.pyplot as plt


def plot_availability_matrix(availability_matrix, axes):
    amount_workers, amount_shifts = availability_matrix.shape

    # Plot
    axes.spy(availability_matrix)

    # Set axis labels
    axes.set_xticks(range(amount_shifts), [f"shift_{i}" for i in range(1, amount_shifts + 1)], rotation=60)
    axes.set_yticks(range(amount_workers), [f"worker_{i}" for i in range(1, amount_workers + 1)]);


def plot_requirements_matrix(requirements_matrix, axes):
    amount_activities, amount_shifts = requirements_matrix.shape

    # Plot
    mat_plot = axes.matshow(requirements_matrix)  # cmap=plt.cm.jet,
    # cb = fig.colorbar(mat_plot, shrink=0.2)

    # Anotate values
    for x in range(amount_activities):
        for y in range(amount_shifts):
            axes.annotate(str(requirements_matrix[x][y]), xy=(y, x), horizontalalignment='center',
                          verticalalignment='center')

    # Set axis labels
    axes.set_xticks(range(amount_shifts), [f"shift_{i}" for i in range(1, amount_shifts + 1)], rotation=60)
    axes.set_yticks(range(amount_activities), [f"activity_{i}" for i in range(1, amount_activities + 1)])


def matrix_plot(problem_parameters):

    availability_matrix, requirements_matrix, solution_matrix = problem_parameters

    fig, (ax_second_row, ax_third_row) = plt.subplots(2, 1, figsize=(15, 15))

    # Subplot 1
    # plot_availability_matrix(availability_matrix, ax_first_row)
    # ax_first_row.set_title("Availability matrix")
    # Subplot 2
    plot_requirements_matrix(requirements_matrix, ax_second_row)
    ax_second_row.set_title("Requirements matrix")
    # Subplot 3
    filled_slots = solution_matrix.sum(axis=0).astype(int)
    plot_requirements_matrix(filled_slots, ax_third_row)
    ax_third_row.set_title("Solution matrix")
    # Subplot 4
    # ...

    plt.tight_layout()


def plot_all_workers(num_rows, amount_workers, solution_matrix):

    n_files = num_rows
    n_columnes = amount_workers//n_files+1
    print("columnes=",n_columnes)

    fig, axes = plt.subplots(figsize=(15, 15), sharex=True, sharey=True, ncols=n_columnes, nrows=n_files)

    for i in range(amount_workers):
        fila_i = i//n_columnes
        columna_i = i%n_columnes
        # print("i =",i," ---> ",fila_i,columna_i)
        axes[fila_i, columna_i].spy(solution_matrix[i])
        axes[fila_i, columna_i].set_title(f"worker_{i+1}")
    fig.tight_layout()