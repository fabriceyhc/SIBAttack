from ..abstract_transformation import AbstractTransformation, _get_tran_types
from ..data.phrases import POSITIVE_PHRASES, NEGATIVE_PHRASES
from random import sample 

class InsertSentimentPhrase(AbstractTransformation):
    """
    Appends a sentiment-laden phrase to a string based on 
    a pre-defined list of phrases.  
    """

    def __init__(self, sentiment='positive', task=None, meta=False):
        """
        Initializes the transformation and provides an
        opporunity to supply a configuration if needed

        Parameters
        ----------
        sentiment : str
            Determines whether the inserted phraase will 
            feature a positive or negative sentiment.
        task : str
            the type of task you wish to transform the
            input towards
        """
        self.sentiment = sentiment
        if self.sentiment.lower() not in ['positive', 'negative']:
            raise ValueError("Sentiment must be 'positive' or 'negative'.")
        self.task = task
        self.metadata = meta
    
    def __call__(self, string):
        """
        Appends a sentiment-laden phrase to a string.

        Parameters
        ----------
        string : str
            Input string

        Returns
        -------
        ret
            String with sentiment phrase appended
        """
        if 'positive' in self.sentiment:
        	phrase = sample(POSITIVE_PHRASES,1)[0]
        if 'negative' in self.sentiment:
        	phrase = sample(NEGATIVE_PHRASES,1)[0]
        ret = string + " " + phrase
        assert type(ret) == str
        meta = {'change': string!=ret}
        if self.metadata: return ret, meta
        return ret

    def get_tran_types(self, task_name=None, tran_type=None):
        self.tran_types = {
            'task_name': ['sentiment', 'topic'],
            'tran_type': ['SIB', 'INV']
        }
        df = _get_tran_types(self.tran_types, task_name, tran_type)
        return df

    def transform_Xy(self, X, y):
        X_ = self(X)
        tran_type = self.get_tran_types(task_name=self.task)['tran_type'][0]
        if tran_type == 'INV':
            y_ = y
        if tran_type == 'SIB':
            if self.sentiment == 'positive':
                y_ = 1
            if self.sentiment == 'negative':
                y_ = 0
        if self.metadata: return X_[0], y_, X_[1]
        return X_, y_

class InsertPositivePhrase(InsertSentimentPhrase):
    """
    Appends a sentiment-laden phrase to a string based on 
    a pre-defined list of phrases.  
    """

    def __init__(self, meta=False):
        super().__init__(sentiment = 'positive')
        self.metadata = meta
    def __call__(self, string):
        phrase = sample(POSITIVE_PHRASES,1)[0]
        ret = string + " " + phrase
        assert type(ret) == str
        meta = {'change': string!=ret}
        if self.metadata: return ret, meta
        return ret

    def get_tran_types(self, task_name=None, tran_type=None):
        self.tran_types = {
            'task_name': ['sentiment', 'topic'],
            'tran_type': ['SIB', 'INV']
        }
        df = _get_tran_types(self.tran_types, task_name, tran_type)
        return df

    def transform_Xy(self, X, y):
        X_ = self(X)
        tran_type = self.get_tran_types(task_name=self.task)['tran_type'][0]
        if tran_type == 'INV':
            y_ = y
        if tran_type == 'SIB':
            y_ = 1
        if self.metadata: return X_[0], y_, X_[1]
        return X_, y_

class InsertNegativePhrase(InsertSentimentPhrase):
    """
    Appends a sentiment-laden phrase to a string based on 
    a pre-defined list of phrases.  
    """

    def __init__(self, meta=False):
        super().__init__(sentiment = 'negative')
        self.metadata = meta
    def __call__(self, string):
        phrase = sample(NEGATIVE_PHRASES,1)[0]
        ret = string + " " + phrase
        assert type(ret) == str
        meta = {'change': string!=ret}
        if self.metadata: return ret, meta
        return ret

    def get_tran_types(self, task_name=None, tran_type=None):
        self.tran_types = {
            'task_name': ['sentiment', 'topic'],
            'tran_type': ['SIB', 'INV']
        }
        df = _get_tran_types(self.tran_types, task_name, tran_type)
        return df

    def transform_Xy(self, X, y):
        X_ = self(X)
        tran_type = self.get_tran_types(task_name=self.task)['tran_type'][0]
        if tran_type == 'INV':
            y_ = y
        if tran_type == 'SIB':
            y_ = 0
        if self.metadata: return X_[0], y_, X_[1]
        return X_, y_