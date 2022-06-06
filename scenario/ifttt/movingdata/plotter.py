from typing import List, Tuple
import matplotlib.pyplot as plt


def plot_data(
    dataset: List[Tuple[float, float]],
    result_file_path: str
):
    dataset = dataset[:10000]
    x1, y1 = zip(*dataset)
    fig, ax = plt.subplots(1, 1)
    ax.scatter(x1, y1)
    fig.savefig(result_file_path)


def parse_line(line: str):
    x, y = line.split(',')
    return float(x), float(y)


def moving_data_consumer(
    dataset_path: str,
    result_file_path: str,
):
    with open(dataset_path) as f:
        dataset = [parse_line(line) for line in f]
        plot_data(dataset, result_file_path)
