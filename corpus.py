import re
from typing import List, Dict


class Corpus:
    def __init__(self, text: str):
        self.text = text

    def __repr__(self):
        return f"{self.text[:500]}..." if len(self.text) > 500 else f"{self.text}"

    
    def split(self, sep: str=None, maxsplit: int=-1) -> List['Corpus']:
        split_text = self.text.split(sep=sep, maxsplit=maxsplit)
        return [ Corpus(text.strip()) for text in split_text ]

    def read_lines(self, n: int, start: int=0) -> str:
        '''
        Returns the specified number of lines in the text, starting from the start index.

        Args:
            n (int): The number of lines to return
            start (int): The starting index of the lines to return
                - Default: 0 (start from the beginning of the text)
        '''
        lines = self.text.splitlines()
        end = min(start + n, len(lines))

        return '\n'.join([lines[i] for i in range(start, end)])

    def word_arr(self) -> List[str]:
        return self.text.split()

    def total_words(self) -> int:
        '''
        Returns the total number of words in the text.
        Calls word_arr() and returns the length of the list.
        '''
        return len(self.word_arr())

    def get_word_count(self) -> Dict[str, int]:
        '''
        Returns a dictionary of words and their counts in the text.
        It will ignore case and punctuation.
        '''
        word_count = {}

        words = re.findall(r'\b\w+\b', self.text.lower())
        for word in words:
            if word in word_count:
                word_count[word] += 1
                continue

            word_count[word] = 1

        return dict(sorted(word_count.items(), key=lambda x: x[1], reverse=True)) 

    def get_word_count_proportion(self) -> Dict[str, float]:
        '''
        Returns a dictionary of words and their proportion in the text.
        The proportion is the count of the word divided by the total number of words.
        '''
        word_count = self.get_word_count()
        total_words = self.total_words()

        return dict(map(lambda x: (x, word_count[x] / total_words), word_count))
    
    def get_top_words(self, n: int=5) -> Dict[str, int]:
        '''
        Returns the top n words and their count in the text by frequency of occurrence.

        Args:
            n (int): The number of top words to return
                - Default: 5
        '''
        word_count = self.get_word_count()
        return dict(list(word_count.items())[:n])

    def legomena(self, n: int=1) -> List[str]:
        '''
        Returns a list of words that appear exactly n times in the text.
        
        Args:
            n (int): The number of times a word appears in the text
                - Default: 1 (hapax legomena)
        '''
        word_count = self.get_word_count()
        return list(filter(lambda x: word_count[x] == n, word_count))

def from_file(fpath: str) -> Corpus:
    with open(fpath, 'r') as f:
        text = f.read()

    return Corpus(text)

def from_gutenberg(fpath: str) -> Corpus:
    text = from_file(fpath)
    delim = '*END THE SMALL PRINT! FOR PUBLIC DOMAIN ETEXTS*Ver.04.29.93*END*'
    return text.split(delim)[1]