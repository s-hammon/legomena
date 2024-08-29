import numpy as np
from pathlib import Path

from corpus import from_gutenberg

def classic_zipf(N, k, s=1):
    return (1 / k ** s) / (np.sum(1 / (np.arange(1, N + 1 ) ** s)))

def main():
    whale = Path(".data/moby_dick.txt")
    text = from_gutenberg(whale)

    print(text.print_lines(200))


main()