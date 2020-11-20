from ..abstract_transformation import AbstractTransformation
import numpy as np
import random
from nltk.corpus import wordnet

class RandomInsertion(AbstractTransformation):
    """
    Inserts random words
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
            Number of word insertions

        Returns
        ----------
        ret : str
            The output with random words swapped
        """
        new_words = words.split()
        for _ in range(n):
            add_word(new_words)
        return ' '.join(new_words)

def add_word(new_words):
	synonyms = []
	counter = 0
	while len(synonyms) < 1:
		random_word = new_words[random.randint(0, len(new_words)-1)]
		synonyms = get_synonyms(random_word)
		counter += 1
		if counter >= 10:
			return
	random_synonym = synonyms[0]
	random_idx = random.randint(0, len(new_words)-1)
	new_words.insert(random_idx, random_synonym)

def get_synonyms(word):
	synonyms = set()
	for syn in wordnet.synsets(word): 
		for l in syn.lemmas(): 
			synonym = l.name().replace("_", " ").replace("-", " ").lower()
			synonym = "".join([char for char in synonym if char in ' qwertyuiopasdfghjklzxcvbnm'])
			synonyms.add(synonym) 
	if word in synonyms:
		synonyms.remove(word)
	return list(synonyms)