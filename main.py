import matplotlib.pyplot as plt 
import numpy as np
from pathlib import Path 

from corpus import from_file
from stats import vectorized_zipf


def main():
    whale = Path(".data/fake.txt")
    text = from_file(whale)

    N, k, s = text.zipf_params()
    print(f"Length of corpus: {N}")
    print(f"Zipf Const: {s}")
    print(f"ranks: {len(k)}")
    
    print(text.legomena_ratio)
    pred = vectorized_zipf(N, k, s)
    ranks = text.rank_words()

    actual = np.array(ranks)
    log_a = np.log(actual)
    log_v = np.log(pred * N)
    x = np.log(k)

    plt.figure(figsize=(10,6))
    plt.plot(x, log_v, marker='o')
    plt.plot(x, log_a, marker='x')
    plt.xlabel('Word Rank')
    plt.ylabel('Log Zipf Proportion')
    plt.title("Plot of Word Index vs Log Zipf Proportion")
    plt.grid(True)

    plt.savefig(".data/fake.png")
    plt.close()
    

main()