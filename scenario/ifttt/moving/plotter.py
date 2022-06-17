"""Contains the function to run as target function in the moving data scenario."""
from typing import List, Tuple
import matplotlib.pyplot as plt


def plot_data(
    dataset: List[Tuple[float, float]],
    result_file_path: str
):
    """Plots the dataset and saves to a file."""
    # Plots the first 10k points of the dataset
    dataset = dataset[:10000]
    x1, y1 = zip(*dataset)
    fig, ax = plt.subplots(1, 1)

    # Draws the title and legends
    ax.scatter(x1, y1, label='Bivariate Normal Distribution')
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_title('Moving Data Result')
    ax.legend()

    # Saves to file
    fig.savefig(result_file_path)


def parse_line(line: str):
    """Parse line into two floats."""
    x, y = line.split(',')
    return float(x), float(y)


def moving_data_consumer(
    dataset_path: str,
    result_file_path: str,
):
    """Consumes the data in moving data scenario."""
    with open(dataset_path) as f:
        dataset = [parse_line(line) for line in f]
        plot_data(dataset, result_file_path)
