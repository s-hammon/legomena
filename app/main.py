import json
import numpy as np
from pathlib import Path 
from yaml import safe_load

from corpus import from_file, multi_file
from stats import vectorized_zipf, chi_square_test


def zipf_command(*args, **kwargs):
    if kwargs.get("file"):
        text = from_file(kwargs["file"])

    elif kwargs.get("config"):
        match kwargs["config"].split(".")[-1]:
            case "json":
                with open(kwargs["config"], "r") as f:
                    config = json.load(f)
            case "yaml":
                with open(kwargs["config"], "r") as f:
                    config = safe_load(f)
            case _:
                raise ValueError("The configuration file must be either JSON or YAML.")

        name = kwargs.get("name", "")
        combine = kwargs.get("combine", False)
        text = multi_file(config, name, combine)
    
    else:
        raise ValueError("You must provide either a file or a configuration file.")

    if isinstance(text, list):
        for idx, corpus in enumerate(text):
            N, k, s = corpus.zipf_params(exclude_legomena=False)
            print(f"Length of corpus {idx}: {N}")
            print(f"Zipf Const {idx}: {s}")
            print(f"ranks {idx}: {len(k)}")

            pred = vectorized_zipf(N, k, s)
            actual = np.array(corpus.rank_words())

            chi2 = chi_square_test(pred * N, actual)
            print(f"Chi-Squared {idx}: {chi2}")
    else:
        N, k, s = text.zipf_params(exclude_legomena=False)
        print(f"Length of corpus: {N}")
        print(f"Zipf Const: {s}")
        print(f"ranks: {len(k)}")
    
        pred = vectorized_zipf(N, k, s)
        actual = np.array(text.rank_words())

        chi2 = chi_square_test(pred * N, actual)
        print(f"Chi-Squared: {chi2}")