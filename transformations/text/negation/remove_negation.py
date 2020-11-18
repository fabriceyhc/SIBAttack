from ..abstract_transformation import AbstractTransformation
import collections
import pattern
import spacy
import en_core_web_sm

class RemoveNegation(AbstractTransformation):
    """
    Defines a transformation that removes a negation
    if found within the input. Otherwise, return the 
    original string unchanged. 
    """

    def __init__(self):
        """
        Initializes the transformation and provides an
        opporunity to supply a configuration if needed
        """
        self.nlp = en_core_web_sm.load()
    
    def __call__(self, string):
        """Removes negation from a string by first 
        converting it to spacy.token.Doc. 

        Parameters
        ----------
        string : str
            Input to have negation removed

        Returns
        -------
        ret : str
            Output with *all* negations removed

        """
        # This removes all negations in the doc. I should maybe add an option to remove just some.
        doc = self.nlp(string)
        notzs = [i for i, z in enumerate(doc) if z.lemma_ == 'not' or z.dep_ == 'neg']
        new = []
        for notz in notzs:
            before = doc[notz - 1] if notz != 0 else None
            after = doc[notz + 1] if len(doc) > notz + 1 else None
            if (after and after.pos_ == 'PUNCT') or (before and before.text in ['or']):
                continue
            new.append(notz)
        notzs = new
        if not notzs:
            return None
        ret = ''
        start = 0
        for i, notz in enumerate(notzs):
            id_start = notz
            to_add = ' '
            id_end = notz + 1
            before = doc[notz - 1] if notz != 0 else None
            after = doc[notz + 1] if len(doc) > notz + 1 else None
            if before and before.lemma_ in ['will', 'can', 'do']:
                id_start = notz - 1
                tenses = collections.Counter([x[0] for x in pattern.en.tenses(before.text)]).most_common(1)
                tense = tenses[0][0] if len(tenses) else 'present'
                p = pattern.en.tenses(before.text)
                params = [tense, 3]
                if p:
                    tmp = [x for x in p if x[0] == tense]
                    if tmp:
                        params = list(tmp[0])
                    else:
                        params = list(p[0])
                to_add = ' '+ pattern.en.conjugate(before.lemma_, *params) + ' '
            if before and after and before.lemma_ == 'do' and after.pos_ == 'VERB':
                id_start = notz - 1
                tenses = collections.Counter([x[0] for x in pattern.en.tenses(before.text)]).most_common(1)
                tense = tenses[0][0] if len(tenses) else 'present'
                p = pattern.en.tenses(before.text)
                params = [tense, 3]
                if p:
                    tmp = [x for x in p if x[0] == tense]
                    if tmp:
                        params = list(tmp[0])
                    else:
                        params = list(p[0])
                to_add = ' '+ pattern.en.conjugate(after.text, *params) + ' '
                id_end = notz + 2
            ret += doc[start:id_start].text + to_add
            start = id_end
        ret += doc[id_end:].text
        return ret