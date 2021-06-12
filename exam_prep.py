import numpy as np

N = 6
D = 4
M = 8

X = np.random.rand(N, D)
W = np.random.rand(D, M)
b = np.full((M,), 0.1)

def linear_python(X, W, b):
    y = []
    for i in range(N):
        y_i = []
        for j in range(M):
            y_ij = b[j]
            for k in range(D):
                y_ij += X[i, k] * W[k, j]
            y_i.append(y_ij)
        y.append(y_i)
    return np.array(y)


def linear_numpy(X, W, b):
    # START TODO #################
    # Re-implement linear_python without for loops using Numpy
    y = np.dot(X, W) + b
    return y
    # END TODO #################
    return y

assert np.allclose(linear_python(X, W, b), linear_numpy(X, W, b))