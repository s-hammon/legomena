import math
from typing import Sequence, Tuple, Union

import numpy as np 


def classic_zipf(N: int, k: float, s: int=1):
    return (1 / k ** s) / float(np.sum(1 / (np.arange(1, N + 1 ) ** s)))

def vectorized_zipf(N: int, data: Sequence[Union[int, float]], s: int=1):
    vectorize = np.vectorize(lambda x: classic_zipf(N, x, s))
    return vectorize(data)

def chi_square_test(observed: np.ndarray, expected: np.ndarray) -> Tuple[float, float]:
    if not len(observed) == len(expected):
        raise ValueError("The observed and expected values must have the same length.")

    chi = np.sum((observed - expected) ** 2 / expected)
    return float(round(chi, 2))