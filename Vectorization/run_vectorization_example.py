import collections
import math
import random
import re

from Dataset import ads

from Vectorizer import *





if __name__ == '__main__':

    vectorizers = [
        CountVectorizer(),
        DictionaryVectorizer(),
        TfidfVectorizer(),
        TfidfVectorizer(group_by_class=True)
    ]
    
    
    # Prepare training and test sets
    doc_ids__by__label = collections.defaultdict(list)
    for i, (_, label) in enumerate(ads):
        doc_ids__by__label[label].append(i)
    
    X_train, X_test, Y_train, Y_test = [], [], [], []
    for label, doc_ids in doc_ids__by__label.items():
        i = random.choice(list(range(len(doc_ids))))
        doc_id = doc_ids.pop(i)
        document, _ = ads[doc_id]
        X_test.append(document)
        Y_test.append(label)

        X_train.extend([
            ads[_doc_id][0] for _doc_id in doc_ids
            if _doc_id != doc_id
        ])

        Y_train.extend([
            label for _doc_id in doc_ids
             if _doc_id != doc_id
        ])

    

    # Fit all the vectorizers on the same dataset
    for vec in vectorizers:
        vec.fit(X_train, Y_train)



    # Vectorize with each one and compare the results
    for doc, label in zip(X_test, Y_test):
        print(doc)
        print(label)
        for vec in vectorizers:
            v = vec.transform([doc])[0]
            print('\t', vec)
            for name, weight in vec.interpret(v):
                print('\t\t%.2f\t%s' % (weight, name))
        print()

