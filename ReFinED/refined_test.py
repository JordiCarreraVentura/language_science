from nltk import ngrams
from nltk import sent_tokenize as splitter
from nltk import wordpunct_tokenize as tokenizer
from refined.inference.processor import Refined

from texts import (
    TEXT__PAPER_TITLES,
    TEXT_VENICE
)



class ReFinED:

    def __init__(self):
        self.refined = Refined.from_pretrained(
            model_name='wikipedia_model_with_numbers',
            entity_set="wikipedia"
        )

    def __call__(self, text):
        annotations = []
        for sent in splitter(text):
            onset = text.index(sent)
            for span in self.refined.process_text(sent):
                if not span.predicted_entity:
                    continue
                annotations.append((
                    span.start + onset,
                    span.start + len(span.text) + onset,
                    span.text,
                    span.predicted_entity
                ))
        return annotations



if __name__ == '__main__':

    rfed = ReFinED()

    print(TEXT_VENICE)
    print()

    for p in rfed(TEXT_VENICE):
        print(p)
