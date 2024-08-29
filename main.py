import numpy as np
from pathlib import Path

from corpus import from_gutenberg

def classic_zipf(N, k, s=1):
    return (1 / k ** s) / (np.sum(1 / (np.arange(1, N + 1 ) ** s)))

def main():
    whale = Path(".data/moby_dick.txt")
    text = from_gutenberg(whale)

    hapax = len(text.legomena(1))
    dis = len(text.legomena(2))
    tris = len(text.legomena(3))
    tetrakis = len(text.legomena(4))

    print(f'''
        Count of hapax legomena: {hapax}
        Count of dis legomena: {dis}
        Count of tris legomena: {tris}
        Count of tetrakis legomena: {tetrakis}
    ''')

main()