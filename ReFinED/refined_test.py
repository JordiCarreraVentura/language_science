from nltk import ngrams
from nltk import sent_tokenize as splitter
from nltk import wordpunct_tokenize as tokenizer
from refined.inference.processor import Refined

from texts import (
    TEXT__PAPER_TITLES,
    TEXT_VENICE
)

refined = Refined.from_pretrained(model_name='wikipedia_model_with_numbers',
                                  entity_set="wikipedia")


for sent in splitter(text):
    tokens = tokenizer(sent)
    for n in [3, 1]:
        for chunk in ngrams(tokens, n):
            phrase = ' '.join(chunk).lower()
            for span in refined.process_text(phrase):
                print(f'{phrase}  ||  {str(span)}')
