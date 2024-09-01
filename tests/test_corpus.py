import re
import unittest

from app.corpus import Corpus, split_text

class TestCorpus(unittest.TestCase):
    def test_corpus_split_text(self):
        cases = [
            {
                "name": "test split on whitespace",
                "params": {
                    "text": "test split on whitespace",
                },
                "want": [
                    Corpus("test"), Corpus("split"), Corpus("on"), Corpus("whitespace")
                ]
            },
            {
                "name": "test split on delimiter",
                "params": {
                    "text": "test, split, on, delimiter",
                    "sep": ", ",
                },
                "want": [
                    Corpus("test"), Corpus("split"), Corpus("on"), Corpus("delimiter")
                ]
            },
            {
                "name": "test split on pattern",
                "params": {
                    "text": "test split ** on ** pattern",
                    "sep": re.compile(r'\s*\*\*.*?\*\*\s*'),
                },
                "want": [
                    Corpus("test split"), Corpus("pattern")
                ]
            },
        ]

        for case in cases:
            got = split_text(**case["params"])
            self.assertEqual(case["want"], got, f"\tcase: {case['name']}")

    def test_corpus_split_test_throw_error(self):
        cases = [
            {
                "name": "test throw error on invalid pattern type",
                "params": {
                    "text": "test split on invalid pattern type",
                    "sep": 1,
                },
                "want":
                    TypeError
            },
            {
                "name": "test throw error on empty text",
                "params": {
                    "text": "",
                },
                "want":
                    ValueError
            },
            {
                "name": "test throw error on invalid maxsplit type",
                "params": {
                    "text": "test split on invalid maxsplit type",
                    "maxsplit": "1",
                },
                "want":
                    TypeError
            },
        ]

        for case in cases:
            with self.assertRaises(case["want"]):
                split_text(**case["params"])