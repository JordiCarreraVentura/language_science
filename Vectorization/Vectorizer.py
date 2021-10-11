import collections
import math
import random
import re

from collections import Counter



TOKENIZER = re.compile('[a-zA-Z]+')




class Vectorizer:

    def __init__(self, group_by_class=False):
        self.group_by_class = group_by_class
        self.vocab = dict([])
    
    def __str__(self):
        return self.__class__.__name__
    
    def __make_vocab(self, documents):
        vocab = set([])
        for doc in documents:
            words = TOKENIZER.findall(doc.lower())
            vocab.update(words)
        self.vocab = {
            w: i for i, w in enumerate(vocab)
        }
    
    def fit(self, documents, labels):
        self.__make_vocab(documents)
        self.fit_specific(documents, labels)
    
    def transform(self, documents):
        return [
            self(doc) for doc in documents
        ]
    
    def fit_transform(self, documents, labels):
        self.fit(documents, labels)
        return self.transform(documents)
    
    def feature_names(self):
        return sorted(list(self.vocab.items()), key=lambda x: x[1])
    
    def interpret(self, vector):
        non_zero = []
        for feature_name, word_i in self.feature_names():
            if vector[word_i]:
                non_zero.append((feature_name, vector[word_i]))
        return sorted(non_zero, key=lambda x: x[1], reverse=True)


class CountVectorizer(Vectorizer):

    def __init__(self, group_by_class=False):
        super().__init__(group_by_class=group_by_class)
    
    def fit_specific(self, documents, labels):
        return
    
    def __call__(self, document):
        vec = [0 for _ in self.vocab]
        words = TOKENIZER.findall(document.lower())
        for word in set(words):
            if word in self.vocab:
                vec[self.vocab[word]] = words.count(word)
        return vec
        

class TfidfVectorizer(Vectorizer):

    def __init__(self, group_by_class=False):
        super().__init__(group_by_class=group_by_class)
        self.dfs = Counter()
        self.tfs = collections.defaultdict(Counter)
        self.idf = dict([])
        self.W = dict([])
    
    def fit_specific(self, documents, labels):
        for doc_i, (doc, label) in enumerate(zip(documents, labels)):
            words = TOKENIZER.findall(doc.lower())
            if self.group_by_class:
                self.tfs[label].update(words)
            else:
                self.tfs[doc_i].update(words)
        self.__make_tfidf()
    
    def __make_tfidf(self):
        n = len(self.tfs.keys())
        dfs = Counter()

        for w, tfs in self.tfs.items():
            dfs.update(tfs.keys())
        
        for w, df in dfs.items():
            self.W[w] = math.log(n / float(df))
    
    
    def __call__(self, document):
        vec = [0 for _ in self.vocab]
        words = TOKENIZER.findall(document.lower())
        for word in set(words):
            if word in self.vocab:
                tf = math.log(words.count(word) + 1)
                vec[self.vocab[word]] = tf * self.W[word]
        return vec
    
    def interpret(self, vector):
        non_zero = []
        dimensions = sorted(list(self.vocab.items()), key=lambda x: x[1])
        for word, word_i in dimensions:
            if vector[word_i]:
                non_zero.append((word, self.W[word]))
        return sorted(non_zero, key=lambda x: x[1], reverse=True)
        
    # TODO: standard TFIDF over new doc TF, not prev docs!




class DictionaryVectorizer(Vectorizer):

    def __init__(self, group_by_class=False):
        super().__init__(group_by_class=group_by_class)
    
    def fit_specific(self, documents, labels):
        return
    
    def __call__(self, document):
        vec = [0 for _ in self.vocab]
        words = TOKENIZER.findall(document.lower())
        for word in set(words):
            if word in self.vocab:
                vec[self.vocab[word]] = 1
        return vec
