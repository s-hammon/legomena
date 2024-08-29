import matplotlib.pyplot as plt 
import numpy as np 
from pathlib import Path 

from corpus import from_gutenberg


def classic_zipf(N, k, s=1):
    return (1 / k ** s) / float(np.sum(1 / (np.arange(1, N + 1 ) ** s)))

def main():
    whale = Path(".data/moby_dick.txt")
    text = from_gutenberg(whale)
    wordbank = text.get_word_count()

    vocab_size = len(wordbank)
    N = sum(wordbank.values())
    
    vectorize = np.vectorize(lambda x: classic_zipf(N, x))

    prop = np.array(list(sorted(list(wordbank.values()), reverse=True))) / len(wordbank)
    pred = vectorize(list(wordbank.values()))

    log_a = np.log(prop * N)
    log_v = np.log(pred * N)
    x = np.log(list(range(1, vocab_size+1)))

    plt.figure(figsize=(10,6))
    plt.plot(x, log_v, marker='o')
    plt.plot(x, log_a, marker='x')
    plt.xlabel('Word Rank')
    plt.ylabel('Log Zipf Proportion')
    plt.title("Plot of Word Index vs Log Zipf Proportion")
    plt.grid(True)

    plt.savefig(".data/zipf.png")
    plt.close()
    

main()