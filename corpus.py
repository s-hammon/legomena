import re
import string
from typing import Tuple, Union, List, Dict


class Corpus:
    def __init__(self, text: str):
        self.text = text
        
        self.legomena_ratio = self.__legomena_ratio()

    def __eq__(self, other: 'Corpus'):
        return self.text == other.text

    def __len__(self):
        return len(self.word_arr())

    def __repr__(self):
        return f"{self.text[:500]}..." if len(self.text) > 500 else f"{self.text}"

    
    def zipf_params(self, s=1) -> Tuple[int, Tuple[int], int]:
        '''
        Returns the parameters of the Zipf distribution for the text.
        
        Args:
            s (int): Optional, the Zipf constant
                - Default: 1
        '''
        N = len(self.word_arr())
        k = tuple([ i+1 for i in range(len(self.rank_words())) ])
        return N, k, s

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
        text_split = self.text.split()
        return list(map(lambda x: x.strip(string.punctuation), text_split))

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
    
    def rank_words(self) -> Tuple[int]:
        '''
        Returns the rank of the text by the number of words.
        '''
        word_count = self.get_word_count()
        
        return tuple(word_count.values())
    
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


    def __legomena_ratio(self) -> Tuple[float]:
        legomena = [ len(self.legomena(i)) for i in range(1, 5) ]
        return tuple([ round(l / min(legomena), 2) for l in legomena ])


def from_file(fpath: str, is_gutenberg: bool=False) -> Corpus:
    with open(fpath, 'r') as f:
        text = f.read()

    if is_gutenberg:
        sep = r"\*\*\* .*? \*\*\*"
        return __from_gutenberg(text, sep)

    return Corpus(text)

def __from_gutenberg(text: str, sep: Union[str, re.Pattern]) -> Corpus:
    sep = re.compile(sep)
    text_split = split_text(text, sep=sep)
    return text_split[1]

def split_text(text: str, sep: Union[str, re.Pattern]=None, maxsplit: int=-1) -> List['Corpus']:
        if text == "":
            raise ValueError("Text is empty")

        if isinstance(sep, re.Pattern):
            split_text = re.split(pattern=sep, string=text)
        else:
            split_text = text.split(sep=sep, maxsplit=maxsplit)
        
        return [ Corpus(text.strip()) for text in split_text ]
