"""Contains the function to run as target function in the streaming data scenario."""
from typing import List, Tuple
import matplotlib.pyplot as plt


def plot_data(
    dataset_1: List[Tuple[float, float]],
    dataset_2: List[Tuple[float, float]],
    result_file_path: str
):
    """Plots the data from two data sets into a single file."""
    # Plots the data
    x1, y1 = zip(*dataset_1)
    x2, y2 = zip(*dataset_2)
    fig, ax = plt.subplots(1, 1)
    ax.scatter(x1, y1, label='First Distribution')
    ax.scatter(x2, y2, label='Second Distribution')

    # Draws the title and legend
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_title('Streaming Data Result')
    ax.legend()

    # Saves into file
    fig.savefig(result_file_path)


def parse_line(line: str):
    """Parses line into two floats."""
    x, y = line.split(',')
    return float(x), float(y)


def streaming_data_consumer(
    dataset_1_path: str,
    dataset_2_path: str,
    result_file_path: str,
):
    """Consumes the data in streaming data scenario."""
    f1 = open(dataset_1_path)
    f2 = open(dataset_2_path)

    dataset_1 = [parse_line(line) for line in f1]
    dataset_2 = [parse_line(line) for line in f2]
    plot_data(dataset_1, dataset_2, result_file_path)

    f1.close()
    f2.close()
