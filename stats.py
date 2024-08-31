import numpy as np 


def classic_zipf(N, k, s=1):
    return (1 / k ** s) / float(np.sum(1 / (np.arange(1, N + 1 ) ** s)))

def vectorized_zipf(N, data, s=1):
    vectorize = np.vectorize(lambda x: classic_zipf(N, x, s))
    return vectorize(data)

