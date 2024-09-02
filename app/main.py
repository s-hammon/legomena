import json
import numpy as np
from pathlib import Path 
from typing import Any, Dict
from yaml import safe_load

from .corpus import Corpus, from_file, multi_file
from .stats import vectorized_zipf, chi_square_test


def handle_command(**kwargs):
    try:
        text = _handle_load_text(**kwargs)

        if text is None:
            raise ValueError("You must provide a file or configuration file to analyze.")
        
        if kwargs.get("command") == "zipf":
            results = [ 
                _process_zipf(t, **kwargs) for t in text 
            ] if isinstance(text, list) else _process_zipf(text, **kwargs)

        elif kwargs.get("command") == "wordcount":
            results = [ 
                _process_wordcount(t, **kwargs) for t in text 
            ] if isinstance(text, list) else _process_wordcount(text, **kwargs)

        else:
            raise ValueError("Invalid command. Must be either 'zipf' or 'wordcount'.")
        
        if kwargs.get("save"):
            with open(kwargs["save"], "w") as f:
                json.dump(results, f)
        else:
            print(results)

    except Exception as e:
        print(f"An error occurred: {e}")

def _process_zipf(t: Corpus, **kwargs):
    exclude_legomena = kwargs.get("exclude_legomena", False)
    results = _get_zipf_results(t, exclude_legomena=exclude_legomena)
    if not kwargs.get("proportions", True):
        results.pop("predicted_proportions", None)
        results.pop("actual_proportions", None)

    return results

def _process_wordcount(t: Corpus, **kwargs):
    return {
        "name": t.name,
        "top_words": t.get_top_words(5),
        "legomena_ratio": {
            "hapax": t.legomena_ratio[0],
            "dis": t.legomena_ratio[1],
            "tris": t.legomena_ratio[2],
            "tetrakis": t.legomena_ratio[3],
        },
        "percent_hapax_legomena": t.percent_hapax(),
    }

def _handle_load_text(**kwargs):
    if kwargs.get("file"):
        fpath = Path(kwargs["file"])
        name = kwargs.get("name", kwargs["file"])
        is_gutenberg = kwargs.get("from_gutenberg", False)

        return from_file(fpath=fpath, name=name, is_gutenberg=is_gutenberg)

    elif kwargs.get("config"):
        file_configs = _handle_config_file(kwargs["config"])
        combine = kwargs.get("combine", False)

        return multi_file(file_configs=file_configs, combine=combine)

    raise ValueError("You must provide a file or configuration file to analyze.")

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

def _get_zipf_results(text: Corpus, exclude_legomena=False) -> Dict[str, Any]:
    N, k, s = text.zipf_params(exclude_legomena=exclude_legomena)
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
