from functools import lru_cache
import json
import random
import time

from nltk import ngrams
from nltk.corpus import stopwords
from nltk import sent_tokenize as splitter
from nltk import wordpunct_tokenize as tokenizer
from refined.inference.processor import Refined
import wikipedia

from cache import Cache



WIKIPEDIA_CACHE_SIZE = 5000

STOPWORDS = stopwords.words('english')
STOPWORDS.extend([
    'also', 'lesser',
    'one', 'ones', 'other', 'others',
    'seven'
])

CACHE = Cache(size=WIKIPEDIA_CACHE_SIZE)



def extract_terms(text, orders=(1, 3)):
    start, end = orders
    for sent in splitter(text):
        tokens = tokenizer(sent.lower())
        for n in range(start, end + 1):
            for gram in ngrams(tokens, n):
                first = gram[0]
                last = gram[-1]
                if first in STOPWORDS \
                or last in STOPWORDS \
                or [token for token in gram if not token.isalpha()]:
                #or filter(lambda x: x.isdigit(), gram):
                    continue
                yield ' '.join(gram)


def cached_lookup(term):
    if term in CACHE:
        #print(term, CACHE.data.keys())
        return CACHE[term]
    else:
        results = wikipedia.search(term)
        CACHE.add(term, results)
    time.sleep(random.randrange(1, 3) + random.uniform(0.0, 1.0))
    return results


"""
wikipedia.search("Barack")
# [u'Barak (given name)', u'Barack Obama', u'Barack (brandy)', u'Presidency of Barack Obama', u'Family of Barack Obama', u'First inauguration of Barack Obama', u'Barack Obama presidential campaign, 2008', u'Barack Obama, Sr.', u'Barack Obama citizenship conspiracy theories', u'Presidential transition of Barack Obama']

>>> ny = wikipedia.page("New York")
>>> ny.title
# u'New York'
>>> ny.url
# u'http://en.wikipedia.org/wiki/New_York'
>>> ny.content
# u'New York is a state in the Northeastern region of the United States. New York is the 27th-most exten'...
>>> ny.links[0]
# u'1790 United States Census'

>>> wikipedia.set_lang("fr")
>>> wikipedia.summary("Facebook", sentences=1)
# Facebook est un service de réseautage social en ligne sur Internet permettant d'y publier des informations (photographies, liens, textes, etc.) en contrôlant leur visibilité par différentes catégories de personnes.
"""

class WikipediaAnnotator:

    def __init__(self):
        wikipedia.set_lang("en")

    def __call__(self, text):
        annotation = dict([])
        annotation['text'] = text
        annotations = []
        for term in extract_terms(text):
            entities = cached_lookup(term)
            annotations.append({
                'text': term,
                'entities': entities
            })
        annotation['annotations'] = annotations
        return annotation


if __name__ == '__main__':

    ann = WikipediaAnnotator()

    text = "From the 9th to the 12th centuries, Venice developed into a powerful maritime empire (an Italian thalassocracy known also as repubblica marinara). In addition to Venice there were seven others: the most important ones were Genoa, Pisa, and Amalfi; and the lesser known were Ragusa, Ancona, Gaeta and Noli."

    for sent in splitter(text):
        annotations = ann(sent)
        print(json.dumps(annotations, indent=4))