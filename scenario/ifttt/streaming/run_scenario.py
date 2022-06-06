import math
import time

import numpy as np
import redis


def schwefel_func(x):
    """Computes the Schwefel's function with the input x.

    :param x: The input.
    :return: Value of Schwefel's function of x.
    """
    total = sum(x_i * math.sin(math.sqrt(abs(x_i))) for x_i in x)
    return 418.9829 * len(x) - total


if __name__ == '__main__':
    redis_client = redis.Redis('localhost', 6379)

    # Underlying distribution 1
    # matrix_size = 2
    underlying_mean_vector_1 = [1, 1]
    underlying_sqrt_cov_1 = np.array([
        [1, 3],
        [2, 2],
    ])
    underlying_cov_matrix_1 = np.dot(
        underlying_sqrt_cov_1, underlying_sqrt_cov_1.transpose()
    )

    # Underlying distribution 2
    underlying_mean_vector_2 = [2, 1]
    underlying_sqrt_cov_2 = np.array([
        [0.5, 0],
        [0.2, 1]
    ])
    underlying_cov_matrix_2 = np.dot(
        underlying_sqrt_cov_2, underlying_sqrt_cov_2.transpose()
    )

    counter_1 = 0
    counter_key_1 = 'counter_1'
    counter_2 = 0
    counter_key_2 = 'counter_2'

    dataset_1 = []
    dataset_2 = []

    f1 = open('../../../data/streaming_data_1', 'w')
    f2 = open('../../../data/streaming_data_2', 'w')

    print('Generate streaming data.')

    for i in range(20000):
        if i < 1e4:
            x_1 = np.random.multivariate_normal(
                underlying_mean_vector_1, underlying_cov_matrix_1
            )

            # Convert before writing
            x_1 = [str(elem) for elem in x_1]
            # Each data point is a line
            f1.write(', '.join(x_1) + '\n')
            f1.flush()

            # Increase the counter 1 and write it into Redis
            counter_1 += 1
            redis_client.set(counter_key_1, counter_1)

        if i % 10 == 0:
            x_2 = np.random.multivariate_normal(
                underlying_mean_vector_2, underlying_cov_matrix_2
            )

            # Convert before writing
            x_2 = [str(elem) for elem in x_2]
            # Each data point is a line
            f2.write(', '.join(x_2) + '\n')
            f2.flush()

            # Increase the counter 2 and write it into Redis
            counter_2 += 1
            redis_client.set(counter_key_2, counter_2)

        time.sleep(0.001)

    f1.close()
    f2.close()
