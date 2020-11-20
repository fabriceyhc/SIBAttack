from ..abstract_transformation import AbstractTransformation
import numpy as np
import random
import re

class RandomSwap(AbstractTransformation):
    """
    Swaps random words
    """

    def __init__(self):
        """
        Initializes the transformation

        Parameters
        ----------
        """
        pass
    
    def __call__(self, words, n=1):
        """
        Parameters
        ----------
        word : str
            The input string
        n : int
            Number of word swaps

        Returns
        ----------
        ret : str
            The output with random words swapped
        """
        new_words = (words).split()
        for _ in range(n):
            new_words = swap_word(new_words)
        return ' '.join(new_words)

def swap_word(new_words):
	random_idx_1 = random.randint(0, len(new_words)-1)
	random_idx_2 = random_idx_1
	counter = 0
	while random_idx_2 == random_idx_1:
		random_idx_2 = random.randint(0, len(new_words)-1)
		counter += 1
		if counter > 3:
			return new_words
	new_words[random_idx_1], new_words[random_idx_2] = new_words[random_idx_2], new_words[random_idx_1] 
	return new_words