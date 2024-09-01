import re
import string
from typing import Tuple, Union, Any, List, Dict


class Corpus:
    def __init__(self, text: str, name: str=""):
        self.name = name
        self.text = text

        self.word_dict = self.__get_word_count()
        self.legomena_ratio = self.__legomena_ratio()

    def __eq__(self, other: 'Corpus'):
        return self.text == other.text

    def __len__(self):
        return len(self.word_arr())

    def __repr__(self):
        return f"{self.text[:500]}..." if len(self.text) > 500 else f"{self.text}"

    
    def zipf_params(self, s=1, exclude_legomena=False) -> Tuple[int, Tuple[int], int]:
        '''
        Returns the parameters of the Zipf distribution for the text.
        
        Args:
            s (int): Optional, the Zipf constant
                - Default: 1

        Returns:
            Tuple[N, Tuple[k], s]: A tuple of the parameters of the Zipf distribution
                - N (int): The total number of words in the text
                - k (Tuple[int]): The rank of each word in the text by frequency of occurrence, descending
                - s (int): The Zipf constant
        '''
        arr = self.word_arr()
        if exclude_legomena:
            arr = list(filter(lambda x: self.word_dict[x] > 4, arr))

        N = len(arr)
        k = tuple([ i+1 for i in range(len(self.rank_words())) ])
        return N, k, s

    def read_lines(self, n: int, start: int=0) -> str:
        '''
        Returns the specified number of lines in the text, starting from the start index.

        Args:
            n (int): The number of lines to return
            start (int): The starting index of the lines to return
                - Default: 0 (start from the beginning of the text)

        Returns:
            str: The specified lines in the text, appended by a newline character
        '''
        lines = self.text.splitlines()
        end = min(start + n, len(lines))

        return '\n'.join([lines[i] for i in range(start, end)])

    def word_arr(self) -> List[str]:
        text_split = self.text.lower().split()
        return list(map(lambda x: x.strip(string.punctuation), text_split))

    def total_words(self) -> int:
        '''
        Returns the total number of words in the text.
        Calls word_arr() and returns the length of the list.
        '''
        return len(self.word_arr())
 
    
    def rank_words(self) -> Tuple[int]:
        '''
        Returns a tuple of the rank of each word in the text by frequency of occurrence.
        '''
        return tuple(self.word_dict.values())
    
    def get_top_words(self, n: int=5) -> Dict[str, int]:
        '''
        Returns the top n words and their count in the text by frequency of occurrence.

        Args:
            n (int): The number of top words to return
                - Default: 5
        
        Returns:
            Dict[str, int]: A dictionary of the top n words and their counts
        '''
        return dict(list(self.word_dict.items())[:n])

    def legomena(self, n: int=1) -> List[str]:
        '''
        Args:
            n (int): The number of times a word appears in the text
                - Default: 1 (hapax legomena)

        Returns:
            List[str]: A list of words that appear exactly n times in the text
        '''
        return list(filter(lambda x: self.word_dict[x] == n, self.word_dict))


    def __legomena_ratio(self) -> Tuple[float]:
        legomena = [ len(self.legomena(i)) for i in range(1, 5) ]
        return tuple([ round(l / max(min(legomena), 1), 2) for l in legomena ])

    def __get_word_count(self) -> Dict[str, int]:
        '''
        Returns a dictionary of words and their counts in the text.
        It will ignore case and punctuation.
        '''
        word_count = {}

        words = self.text.lower().split()
        for word in list(map(lambda x: x.strip(string.punctuation), words)):
            if word in word_count:
                word_count[word] += 1
                continue

            word_count[word] = 1

        return dict(sorted(word_count.items(), key=lambda x: x[1], reverse=True))


def from_file(fpath: str, name: str="", is_gutenberg: bool=False) -> Corpus:
    '''
    Create a Corpus object directly from the contents of a file. Will only deliminiate if
    the file is from Project Gutenberg, in which the header && footer will be removed. If
    you need to split the text, refer to split_text().

    Args:
        fpath (str): The path to the file
        is_gutenberg (bool): Optional, if the file is from Project Gutenberg
            - Default :False
    
    Returns:
        Corpus: A Corpus object
    '''
    with open(fpath, 'r') as f:
        text = f.read()

    if is_gutenberg:
        sep = r"\*\*\* .*? \*\*\*"
        return __from_gutenberg(text, name, sep)

    return Corpus(text, name=name)

def split_text(text: str, name: str="", sep: Union[str, re.Pattern]=None, maxsplit: int=-1) -> List['Corpus']:
        '''
        Splits the text into a list of Corpus objects. Use this after loading text from a file (using 
        open() or any other method).  After providing the delimiter, the text will be split into a list
        of Corpus objects, from which you can select the desired text.

        Args:
            text (str): The text to split
            sep (Union[str, re.Pattern]): The delimiter to split the text
                - Default: None
            maxsplit (int): Optional, the maximum number of splits to make
                - Default: -1 (no limit
        
        Returns:
            List['Corpus']: A list of Corpus objects
        '''
        if text == "":
            raise ValueError("Text is empty")

        if isinstance(sep, re.Pattern):
            split_text = re.split(pattern=sep, string=text)
        else:
            split_text = text.split(sep=sep, maxsplit=maxsplit)
        
        return [ Corpus(text.strip(), name=name) for text in split_text ]

def multi_file(file_configs: List[Dict[str, Any]], set_name: str="", combine=False) -> Union[List[Corpus], Corpus]:
    '''
    Load multiple files into Corpus objects. If combine is set to True, then the text from each file
    will be combined into a single Corpus object.

    Args:
        file_configs (List[Dict[str, Any]]): A list of dictionaries containing the file path and whether
            the file is from Project Gutenberg
        combine (bool): Optional, if the text from each file should be combined
            - Default: False

    Returns:
        Union[List[Corpus], Corpus]: A list of Corpus objects or a single Corpus object
    '''
    corpus_list: List[Corpus] = []
    for file_config in file_configs:
        try:
            fpath = file_config['fpath']
        except KeyError:
            raise ValueError("File path not provided")

        name = file_config.get('name', "")
        is_gutenberg = file_config.get('is_gutenberg', False)
        corpus_list.append(from_file(fpath, name, is_gutenberg))

    if combine:
        text = "\n".join([corpus.text for corpus in corpus_list])
        return Corpus(text=text, name=set_name)

    return corpus_list

def __from_gutenberg(text: str, name: str, sep: Union[str, re.Pattern]) -> Corpus:
    sep = re.compile(sep)
    text_split = split_text(text, name=name, sep=sep)
    return text_split[1]
