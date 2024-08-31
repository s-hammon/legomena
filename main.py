import matplotlib.pyplot as plt 
import numpy as np 
from pathlib import Path 

from corpus import from_file, from_gutenberg


def classic_zipf(N, k, s=1):
    return (1 / k ** s) / float(np.sum(1 / (np.arange(1, N + 1 ) ** s)))

def vectorized_zipf(N, data, s=1):
    vectorize = np.vectorize(lambda x: classic_zipf(N, x, s))
    return vectorize(data)

def main():
    whale = Path(".data/moby_dick.txt")
    pattern = r"\*\*\* .*? \*\*\*"
    text = from_gutenberg(whale, pattern)
    ranks = text.rank_words()

    N = len(text.word_arr())
    
    pred = vectorized_zipf(N, [ i+1 for i in range(len(ranks)) ])

    actual = np.array(ranks)
    log_a = np.log(actual)
    log_v = np.log(pred * N)
    x = np.log(list(range(1, len(ranks)+1)))

    plt.figure(figsize=(10,6))
    plt.plot(x, log_v, marker='o')
    plt.plot(x, log_a, marker='x')
    plt.xlabel('Word Rank')
    plt.ylabel('Log Zipf Proportion')
    plt.title("Plot of Word Index vs Log Zipf Proportion")
    plt.grid(True)

    plt.savefig(".data/moby_dick.png")
    plt.close()
    

main()