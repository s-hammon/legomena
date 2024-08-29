from typing import List


class Corpus:
    def __init__(self, text: str):
        self.text = text

    def __repr__(self):
        return f"{self.text[:500]}..." if len(self.text) > 500 else f"{self.text}"

    
    def split(self, sep: str=None, maxsplit: int=-1) -> List['Corpus']:
        split_text = self.text.split(sep=sep, maxsplit=maxsplit)
        return [ Corpus(text.strip()) for text in split_text ]

    def print_lines(self, n: int, start: int=0) -> str:
        lines = self.text.splitlines()
        end = min(start + n, len(lines))

        return '\n'.join([lines[i] for i in range(start, end)])

def from_file(fpath: str) -> Corpus:
    with open(fpath, 'r') as f:
        text = f.read()

    return Corpus(text)

def from_gutenberg(fpath: str) -> Corpus:
    text = from_file(fpath)
    delim = '*END THE SMALL PRINT! FOR PUBLIC DOMAIN ETEXTS*Ver.04.29.93*END*'
    return text.split(delim)[1]