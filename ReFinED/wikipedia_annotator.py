from difflib import SequenceMatcher
import json
import random
import re
import time

from nltk import ngrams
from nltk.corpus import stopwords
from nltk import sent_tokenize as splitter
from nltk import wordpunct_tokenize as tokenizer
from refined.inference.processor import Refined
import wikipedia
from wikipedia.exceptions import DisambiguationError, PageError

from cache import Cache



WIKIPEDIA_CACHE_SIZE = 25000

STOPWORDS = stopwords.words('english')
STOPWORDS.extend([
    'also', 'lesser',
    'one', 'ones', 'other', 'others',
    'seven'
])

CACHE_PAGES = Cache(size=WIKIPEDIA_CACHE_SIZE, path='cache_pages.p')

CACHE_ARTICLES = Cache(size=WIKIPEDIA_CACHE_SIZE, path='cache_articles.p')

TOKEN = re.compile(r'\w+', re.IGNORECASE)



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


def extract_words(text):
    terms = []
    for _match in TOKEN.finditer(text):
        terms.append({
            'raw': _match.group(),
            'text': _match.group().lower(),
            'start': _match.start(),
            'end': _match.end(),
        })
    return terms



def filter_categories(categories):
    return [
        cat for cat in categories
        if not (
            (cat.startswith('Articles ') and 'identifiers' in cat)
            or (cat.startswith('Articles '))
            or (cat.startswith('Pages '))
            or (cat.startswith('CS1 '))
            or (cat.startswith('CS1:'))
            or ' stubs' in cat
            or 'EngvarB' in cat
            or 'Featured articles' in cat
            or (cat.startswith('All '))
            or ' template ' in cat
            or 'Source attribution ' in cat
            or 'Wikidata' in cat
            or 'Wikipedia' in cat
            or 'Wikisource' in cat
            or 'Use dmy dates' in cat
            or 'Use mdy dates' in cat
        )
    ]



def extract_terms2(text, orders=[4, 3, 2, 1], ratio=0.75):
    words = extract_words(text)
    covered = set([])
    orders = orders.copy()
    terms = []
    while orders:
        order = orders.pop(0)
        for idx in range(len(words) - order):
            area = set(range(idx, idx + order))
            if area.intersection(covered):
                continue

            tokens = words[idx:idx + order]
            tokens_text = [token['text'] for token in tokens]
            first = tokens_text[0]
            last = tokens_text[-1]

            if first in STOPWORDS \
            or last in STOPWORDS \
            or [token for token in tokens_text if not token.isalpha()]:
                continue

            term = text[tokens[0]['start']:tokens[-1]['end']]
            term_text = ' '.join(tokens_text)
            results = cached_lookup(term, CACHE_PAGES, wikipedia.search)

            matched = False
            for page_title in results:
                if len(page_title.split()) > len(term_text.split()):
                    continue
                matcher = SequenceMatcher(None, page_title.lower(), term_text)
                if matcher.ratio() >= ratio:
                    print('\t>>>', term_text, '||', page_title)
                    try:
                        article = cached_lookup(
                            page_title, CACHE_ARTICLES, wikipedia.page
                        )
                    except DisambiguationError:
                        continue
                    except PageError:
                        continue
                    terms.append({
                        'order': order,
                        'components': tokens,
                        'wikipedia_page': page_title,
                        'wikipedia_article': {
                            'title': article.title,
                            'url': article.url,
                            'categories': filter_categories(article.categories),
                            #'content': article.content,
                            'summary': article.summary
                        }
                    })
                    covered.update(area)
                    matched = True
                    break
            if not matched:
                print(term_text)

    return terms



def cached_lookup(term, cache, func):
    if term in cache:
        return cache[term]
    else:
        if func == wikipedia.page:
            results = func(term, auto_suggest=False)
        else:
            results = func(term)
        cache.add(term, results)
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

    text = "Its own strategic position at the head of the Adriatic made Venetian naval and commercial power almost invulnerable. With the elimination of pirates along the Dalmatian coast, the city became a flourishing trade centre between Western Europe and the rest of the world, especially with the Byzantine Empire and Asia, where its navy protected sea routes against piracy."

    for sent in splitter(text):
        print()
        print(sent)
        for term in extract_terms2(sent):
            print(json.dumps(term, indent=4))
