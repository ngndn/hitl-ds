import numpy as np


if __name__ == '__main__':
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

    with open('../../../data/move_src_data', 'w') as fw:
        for _ in range(10000000):
            x = np.random.multivariate_normal(
                underlying_mean_vector_1, underlying_cov_matrix_1
            )

            # Convert before writing
            x = [str(elem) for elem in x]
            # Each data point is a line
            fw.write(', '.join(x) + '\n')
