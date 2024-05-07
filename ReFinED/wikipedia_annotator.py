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
from texts import (
    TEXT__PAPER_TITLES,
    TEXT_VENICE
)


WIKIPEDIA_CACHE_SIZE = 25000

STOPWORDS = stopwords.words('english')
STOPWORDS.extend([
    'almost', 'also',
    'lesser',
    'one', 'ones', 'other', 'others',
    'rest',
    'seven'
])

CACHE_PAGES = Cache(size=WIKIPEDIA_CACHE_SIZE, path='cache_pages.p')

CACHE_ARTICLES = Cache(size=WIKIPEDIA_CACHE_SIZE, path='cache_articles.p')

TOKEN = re.compile(r'\w+', re.IGNORECASE)



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



def extract_terms(text, orders=[4, 3, 2, 1], ratio=0.75):
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
                        'text': term,
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
    time.sleep(random.randrange(3, 5) + random.uniform(0.5, 2.5))
    return results



class WikipediaAnnotator:

    def __init__(self, orders=[3, 2, 1], ratio=0.88):
        self.orders = orders
        self.ratio = ratio
        wikipedia.set_lang("en")

    def __call__(self, text):
        return {
            'text': text,
            'annotations': extract_terms(
                text,
                orders=self.orders,
                ratio=self.ratio
            )
        }



if __name__ == '__main__':

    ann = WikipediaAnnotator()

    results = []
    for text in [TEXT__PAPER_TITLES, TEXT_VENICE]:
#     for text in ["From the 9th to the 12th centuries, Venice developed into a powerful maritime empire (an Italian thalassocracy known also as repubblica marinara). In addition to Venice there were seven others: the most important ones were Genoa, Pisa, and Amalfi; and the lesser known were Ragusa, Ancona, Gaeta and Noli."]:
        results.append(ann(text))

    with open('results.json', 'w') as wrt:
        json.dump(results, wrt, indent=4)
