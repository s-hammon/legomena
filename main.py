import matplotlib.pyplot as plt 
import numpy as np 
from pathlib import Path 

from corpus import from_gutenberg


def classic_zipf(N, k, s=1):
    return (1 / k ** s) / float(np.sum(1 / (np.arange(1, N + 1 ) ** s)))

def main():
    whale = Path(".data/moby_dick.txt")
    pattern = r"\*\*\* START OF THE PROJECT GUTENBERG EBOOK .*? \*\*\*"
    text = from_gutenberg(whale, pattern)
    wordbank = text.rank_words()
    prop = text.get_ranked_proportion()
    print(wordbank[0])

    N = len(text.word_arr())
    print(N)
    
    vectorize = np.vectorize(lambda x: classic_zipf(N, x))

    pred = vectorize([ w[0] for w in wordbank ])
    print(pred[:5])
    print(prop[:5])


    actual = np.array([ p[1] for p in prop ])
    log_a = np.log(actual * N)
    log_v = np.log(pred * N)
    x = np.log(list(range(1, len(prop)+1)))

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