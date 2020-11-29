from ..abstract_transformation import AbstractTransformation, _get_tran_types
import numpy as np
import en_core_web_sm
from ..data.locations import NAMED_ENTITIES

class ChangeLocation(AbstractTransformation):
    """
    Changes Location names
    """

    def __init__(self):
        """
        Transforms an input by replacing names of recognized location entity.
        """
        self.nlp = en_core_web_sm.load()
    
    def __call__(self, string):
        """
        Parameters
        ----------
        string : str
            The input string

        Returns
        ----------
        newString : str
            The output with location names replaced
        """
        doc = self.nlp(string)
        newString = string
        for e in reversed(doc.ents): #reversed to not modify the offsets of other entities when substituting
            start = e.start_char
            end = start + len(e.text)
            # print(e.text, "label is ", e.label_)
            if e.label_ in ('GPE', 'NORP', 'FAC', 'ORG', 'LOC'):
                name = newString[start:end]
                name = name.split()
                name[0] =  self._get_loc_name()
                name = " ".join(name)
                newString = newString[:start] + name + newString[end:]
        return newString

    def _get_loc_name(self):
        """Return a random location name."""
        loc = np.random.choice(['country', 'nationality', 'city'])
        return np.random.choice(NAMED_ENTITIES[loc])

    def get_tran_types(self, task_name=None, tran_type=None):
        self.tran_types = {
            'task_name': ['sentiment', 'topic'],
            'tran_type': ['INV', 'INV']
        }
        df = _get_tran_types(self.tran_types, task_name, tran_type)
        return df