import json
import numpy as np
from pathlib import Path 
from typing import Any, Dict
from yaml import safe_load

from corpus import Corpus, from_file, multi_file
from stats import vectorized_zipf, chi_square_test


def zipf_command(*args, **kwargs):
    try:
        if kwargs.get("file"):
            fpath = Path(kwargs["file"])
            name = kwargs.get("name", kwargs["file"])
            is_gutenberg = kwargs.get("from_gutenberg", False)

            text = from_file(fpath=fpath, name=name, is_gutenberg=is_gutenberg)

        elif kwargs.get("config"):
            config = _handle_config_file(kwargs["config"])

            combine = kwargs.get("combine", False)

            text = multi_file(config=config, combine=combine)
    
        else:
            raise ValueError("You must provide either a file or a configuration file.")

        if isinstance(text, list):
            zipf_results = []
            for t in text:
                results = _get_zipf_results(t)
                if not kwargs.get("proportions"):
                    results.pop("predicted_proportions")
                    results.pop("actual_proportions")

                zipf_results.append(results)
                
        else:
            zipf_results = _get_zipf_results(text)
            if not kwargs.get("proportions"):
                zipf_results.pop("predicted_proportions")
                zipf_results.pop("actual_proportions")

        if kwargs.get("save"):
            with open(kwargs["save"], "w") as f:
                json.dump(zipf_results, f)
        else:
            print(zipf_results)
    except Exception as e:
        print(f"An error occurred: {e}")

def _handle_config_file(fpath: str) -> Dict[str, Any]:
    match fpath.split(".")[-1]:
        case "json":
            with open(fpath, "r") as f:
                return json.load(f)
        case "yaml":
            with open(fpath, "r") as f:
                return safe_load(f)
        case _:
            raise ValueError("The configuration file must be either JSON or YAML.")

def _get_zipf_results(text: Corpus) -> Dict[str, Any]:
    N, k, s = text.zipf_params(exclude_legomena=False)
    pred = vectorized_zipf(N, k, s)
    actual = np.array(text.rank_words())

    chi2 = chi_square_test(pred * N, actual)

    return {
        "name": text.name,
        "word_length": N,
        "ranks": len(k),
        "zipf_const": s,
        "chi2": chi2,
        "predicted_proportions": pred.tolist(),
        "actual_proportions": actual.tolist(),
    }
