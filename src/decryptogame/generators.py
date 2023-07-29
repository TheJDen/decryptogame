import random
from collections.abc import Sequence
from decryptogame.components import Keywords
from itertools import permutations


DEFAULT_CODE_LENGTH = 3

class RandomCodes:
    def __init__(self, keyword_cards: Sequence[Keywords], code_lengths: Sequence[int] = None):
        self.lengths = code_lengths if code_lengths is not None else [DEFAULT_CODE_LENGTH] * len(keyword_cards)
        self.codes = []
        for keywords, code_length in zip(keyword_cards, self.lengths):
            codes = list(permutations(range(len(keywords)), code_length))
            self.codes.append(codes)
    
    def __next__(self):
        return [random.choice(codes) for codes in self.codes]

    def __iter__(self):
        return self