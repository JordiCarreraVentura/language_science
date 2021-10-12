# Vectorization of short texts

Currently, many NLP tasks receive as input tweets or tweet-like messages, that is, short texts that usually correspond to a single sentence. Think of e-commerce product titles, questions in question-answering systems, requests in intent detection, or individual sentences for a common use case of SEQ2SEQ and Transformer-based sentence encoders.

However, standard bag-of-word (BoW) representations, as originally developed in the area of Information Retrieval and later adopted for Natural Language Processing, generally make the assumption that a system's input are whole documents, not isolated sentences, and longer documents providing a far larger context for language processing than sentences only.

For instance, Latent-Dirichlet-Allocation (LDA)-based topic modelling was initially designed to represent the meaning of each word based on the meaning of its neighboring words. As such, long documents provided a much richer context from which to derive this kind of inferences, whereas short texts are usually too fragmented to allow or effective modelling using the same technique, and LDA is well-known to struggle with short documents.

So, what is the specific impact of short texts on vectorization? If BoW representations are intended for longer texts, what happens if we suddenly start using them for shorter texts? Does it matter? Or does everything remain the same?

In this notebook we want to show that it generally does not matter, except in one possible situation.

For our experiment, we will need to
1. define the dataset we will be using,
2. define which text vectorization methods we want to compare;
3. and assess the differences between each method when run on the given dataset.

Points 1 and 2 will be covered next. After that, we will use them as inputs for the analysis in point 3.

## 1. Dataset

For our example, we will consider a small toy dataset consisting of 3 classes

`Y = {"cell-phones", "books", "nutrition"}`

with a few documents each:
1. 9 documents for `cell-phones`
2. 6 documents for `nutrition`
3. 6 documents for `books`

The dataset is hard-coded as variable `ads` inside the `Dataset` module.

## 2. Vectorizers

We will consider four types of vectorization strategies:
1. Dictionary vectorization
2. Frequency vectorization
3. TFIDF-weighted vectorization
4. TFICF-weighted vectorization

All of these strategies are implemented as Python classes in the `Vectorizer` module under the following names, respectively:
1. `DictionaryVectorizer`
2. `CountVectorizer`
3. `TfidfVectorizer` and 4 (`TfidfVectorizer` with keyword argument `group_by_class` set to `True`)

### 2.1. Technical specifications
Here is the one-paragraph description of each of these methods:

#### 2.1.1. `DictionaryVectorizer`
The `DictionaryVectorizer` will take each document and return its binary encoding, that is, a vector
1. with as many columns as words are in our vocabulary (where vocabulary is defined as the set of all unique words occurring in our documents) and,
2. for each column, either a 1 or a 0, depending on whether the document contains that word.
   
This is esentially an implementation of the identity function over a vocabulary and over all the words in an input text. The output should the same as if we used the `scikit-learn.feature_extraction.text.CountVectorizer` class with the `binary` parameter set to `True`, for those who are familiar with Python's `scikit-learn` library.

#### 2.1.2. `CountVectorizer`
The `CountVectorizer` also returns a vector for each input document and with as many columns as words are in our vocabulary. However, in this case the value of each column is **not** 1 or 0, but actually the **frequency** of a word in the input text (each column of the vector corresponds to one of the words in our vocabulary, and only that word). So, the values in the columns can be 0, 1, or any higher natural number.

#### 2.1.3. `TfidfVectorizer`
The `TfidfVectorizer` returns a vector where, instead of a categorical binary label or a frequency count, each column contains the TFIDF weight for that term.

What is the TFIDF weight? [Here's](https://en.wikipedia.org/wiki/Tf–idf) the technical definition, but as a quick summary, it is a measure derived
1. from the word's **frequency** as measured over a document (the TF part of the TFIDF equation),
2. which is then multiplied times that word's frequency over all the documents and, more precisely, by its **inverse** frequency over all the documents (the IDF part of the TFIDF equation).

**Why is the *inverse frequency* used?**

If a word appears in **every** document, it is too general and it is not informative, that is, it is not meaningfully associated with any particular document. This means that, if we used that word to try to find a document, we would end up with the whole set of documents! Put another way, those words contribute little to document search and, in tasks where the goal is to filter a large initial search space down to a few relevant documents, those words will have no effect, proving to be redundant at best, and confounders in the worst case scenario.

That is why, in the context of Document Retrieval (where BoW representations were first introduced, and where the goal is to search for specific documents over a database), it is best to simply filter out these words. In this paradigm, the best way to find any document (and to represent the meaning of that document, since meaning and searchable content are taken to be the same) is to find the words
1. with the highest frequency in the document (TF) (since these terms can be expected to denote what that document is about: a text about politics should contain **many** occurrences of words like *government*, *president* or *country*) and 
2. the lowest frequency over all documents (IDF) (these words will denote what only a few documents are about, and those are the documents we need). If a word appears in a single document, and somebody searches for that word, there is no doubt as to what document they are looking for or, at least, what is the only document that can be returned as a candidate answer.

#### 2.1.4. `TfidfVectorizer` with inverse class frequency (instead of inverse document frequency)
Finally, the `TfidfVectorizer` with class frequency is almost the same as the `TfidfVectorizer` with one major difference:
- it also uses the TF term of the TFIDF equation as defined above
- but it modifies the IDF term so that it is computed over classes of documents instead of all the documents.

That is, given the standard X and Y axis of an annotated dataset, such that $\exists y: y \in Y \land \sum_{i}^{|Y|} \big\{ 1\text{ if }Y_i \neq y\text{ else 0} \big\} \ge 1$, instead of using each _x_ in X as the documents for the IDF calculation, we will modify the definition and consider as a document the concatenation of every _x_ with the same _y_.

Given this requirement, this vectorization is only possible when the vector of Y labels is given. This is (always?) the case in the context of a supervised machine learning task, but differs from e.g. `scikit-learn`'s standard assumptions, whereby their vectorizers ignore the Y axis of the input matrix.

However, if this data is indeed given to us during training, we can leverage it to compute the TFIDF for classes of documents rather than for every document individually.

**And is that a good thing?**

1. Not necessarily in the context of an Information Retrieval task (where document-specific calculation will always return the set of key words that answer a query with the highest precision)
2. but probably yes for other tasks, since another consequence of traditional TFIDF is that it assigns comparatively lower scores to class-defining key words (due to their lower IDFs), which can be particularly damaging for imbalanced datasets (if a class contains many more documents than the rest, all its key words will be assigned weights closer to those of stop words than to those of key words from other classes, penalizing the best features for predicting the majority class just by virtue of it being the majority class).

**Example**

To illustrate our point, imagine we are classifying political articles: names of politicians mentioned in a single story will have a very high IDF, whereas the name of a politician who is always mentioned on political news stories would have a much lower value despite being far more central to our domain. This is the equivalent of Barak Obama being assigned a lower weight in the domain of politics than any local leader he once met with.

That local leader's name is definitely the best cue we could provide the system if we wanted to find documents about that person but, if we are interested in a representation of the domain of politics, assigning a higher weight to those outliers (possibly leading to overfitting) as opposed to a core domain entity like Barak Obama for the topic of politics, seems clearly suboptimal.

In its standard definition, TFIDF favors specificity at the expense of representativity, returning the most direct answer to the question, but not necessarily the best answer overall. When applied as an input representation method, it results in underestimation of all the central categories in the semantic space we are considering, missing the forest for the trees.

The modified class-level TFIDF, or TFICF for short, should provide a slightly better representation whenever the Y axis is available.

## 3. Working hypotheses
Based on these descriptions, we can already venture some hypotheses:
1. `CountVectorizer` represents essentially the same information as the `DictionaryVectorizer` but with raw frequency counts instead of a categorial binary labeling. If we are working with long documents containing many mentions of the same words, then the values in `CountVectorizer`'s vector would be much larger than the values in `DictionaryVectorizer`'s vector, since the latter are effectively capped to 1 no matter how many times each word appears in the text. However, if we are working with short texts, which will tend to contain only one occurrence of each word (except for prepositions, determiners, and similar function words with little lexical meaning), frequency becomes irrelevant, as it will always be either 0 or 1, becoming essentially binary as well, the same set of values used by the `DictionaryVectorizer`. Therefore, our hypothesis is that, with most words having the same frequency in short texts, **a short text's** `DictionaryVectorizer` **-encoded vector will look very similar, if not identical, to a** `CountVectorizer`**-encoded vector** (which is definitely **not** true for long documents).
2. The two implementations of `TfidfVectorizer` are also very similar, with both using the same formula to calculate TFIDF, and with the only difference being what each of them takes as the "document", its unit of analysis for the IDF term, which can be either
  - each individual document (for the standard vectorizer),
  - each class (represented as the concatenation of all its documents) or
  - some number in between, by randomly grouping documents from the same class into an arbitrary subclass, which results in a number of documents that is less than the original but still greater than the number of classes (which helps in binary classification tasks, where having two classes only would make the IDF scores too close).
  
  By grouping the documents in this way, we are shifting the IDF penalty
  - from words that occur in many documents (whether it's a stop word like _the_ or a content word like `Barak Obama`)
  - to words that occur in many classes, regardless of the number of documents,
  since, what we should realize penalize is the latter (because the fact that a word appears with many different classes means it is a constant, not an independent variable that can help us predict those classes –and, in this case, whereas `the` will still meet this definition, given that it will appear in every class, `Barak Obama` will not, given that it will mainly occur in texts about politics).

  Therefore, **we expect class-defining key words, penalized by the traditional TFIDF-weighting scheme, to have higher weights using the modified TFICF weighting.**

## 4. Analysis

### Python pipeline

Let's start by importing the dependencies and all necessary objects:


```python
import collections
import random

from Dataset import ads

from Vectorizer import *
```

Let's seed the random algorithm, for reproducibility:


```python
random.seed(3)
```

Next, we initialize the objects corresponding to all the vectorizers we'll compare, the same we introduced in section 2 above.


```python
vectorizers = [
    CountVectorizer(),
    DictionaryVectorizer(),
    TfidfVectorizer(),
    TfidfVectorizer(group_by_class=1)
]
```

And then, we split the data into training and test set. We will take 1 random instance as the test set, and use the remaining instances of each class as the training set to fit each vectorizer.


```python
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
```

Having defined the training and test sets, we can finally fit each vectorizer, and then use them on the test set to get the feature weights and compare them across the different schemes:


```python
# Fit all the vectorizers on the same dataset
for vec in vectorizers:
    vec.fit(X_train, Y_train)

# Vectorize with each one and compare the results
for doc, label in zip(X_test, Y_test):
    print('INPUT DOCUMENT: "%s"' % doc)
    print('\nDOCUMENT LABEL: %s' % label)
    for vec in vectorizers:
        v = vec.transform([doc])[0]
        print('\n  VECTORIZER TYPE: %s' % vec)
        for name, weight in vec.interpret(v):
            print('\tweight=%.2f\tfeature="%s"' % (weight, name))
    print('\n\n')

```

    INPUT DOCUMENT: "Ericsson DF688 Vintage Flip Cell Phone NEW LISTING Ericsson DF688 Vintage Flip Cell Phone"
    
    DOCUMENT LABEL: cell-phones
    
      VECTORIZER TYPE: CountVectorizer
    	weight=2.00	feature="flip"
    	weight=2.00	feature="phone"
    	weight=2.00	feature="cell"
    	weight=2.00	feature="vintage"
    	weight=1.00	feature="listing"
    	weight=1.00	feature="new"
    
      VECTORIZER TYPE: DictionaryVectorizer
    	weight=1.00	feature="flip"
    	weight=1.00	feature="phone"
    	weight=1.00	feature="listing"
    	weight=1.00	feature="cell"
    	weight=1.00	feature="new"
    	weight=1.00	feature="vintage"
    
      VECTORIZER TYPE: TfidfVectorizer
    	weight=2.83	feature="flip"
    	weight=2.14	feature="listing"
    	weight=2.14	feature="cell"
    	weight=2.14	feature="vintage"
    	weight=1.45	feature="phone"
    	weight=1.22	feature="new"
    
      VECTORIZER TYPE: TfidfVectorizer
    	weight=1.10	feature="flip"
    	weight=1.10	feature="phone"
    	weight=1.10	feature="cell"
    	weight=1.10	feature="vintage"
    	weight=0.41	feature="listing"
    	weight=0.41	feature="new"
    
    
    
    INPUT DOCUMENT: "Kitchen Confidential by Anthony Bourdain FREE SHIPPING a paperback book"
    
    DOCUMENT LABEL: books
    
      VECTORIZER TYPE: CountVectorizer
    	weight=1.00	feature="free"
    	weight=1.00	feature="a"
    	weight=1.00	feature="shipping"
    	weight=1.00	feature="by"
    	weight=1.00	feature="book"
    
      VECTORIZER TYPE: DictionaryVectorizer
    	weight=1.00	feature="free"
    	weight=1.00	feature="a"
    	weight=1.00	feature="shipping"
    	weight=1.00	feature="by"
    	weight=1.00	feature="book"
    
      VECTORIZER TYPE: TfidfVectorizer
    	weight=2.83	feature="free"
    	weight=2.83	feature="a"
    	weight=2.83	feature="shipping"
    	weight=2.83	feature="by"
    	weight=1.45	feature="book"
    
      VECTORIZER TYPE: TfidfVectorizer
    	weight=1.10	feature="free"
    	weight=1.10	feature="a"
    	weight=1.10	feature="shipping"
    	weight=1.10	feature="by"
    	weight=1.10	feature="book"
    
    
    
    INPUT DOCUMENT: "Lanes Calm Life Nutrition Supplement For Relaxation And Tranquility Capsules"
    
    DOCUMENT LABEL: nutrition
    
      VECTORIZER TYPE: CountVectorizer
    	weight=1.00	feature="capsules"
    	weight=1.00	feature="supplement"
    	weight=1.00	feature="for"
    	weight=1.00	feature="nutrition"
    
      VECTORIZER TYPE: DictionaryVectorizer
    	weight=1.00	feature="capsules"
    	weight=1.00	feature="supplement"
    	weight=1.00	feature="for"
    	weight=1.00	feature="nutrition"
    
      VECTORIZER TYPE: TfidfVectorizer
    	weight=2.83	feature="supplement"
    	weight=2.83	feature="for"
    	weight=2.14	feature="capsules"
    	weight=1.22	feature="nutrition"
    
      VECTORIZER TYPE: TfidfVectorizer
    	weight=1.10	feature="capsules"
    	weight=1.10	feature="supplement"
    	weight=1.10	feature="for"
    	weight=1.10	feature="nutrition"
    
    
    


As shown above, the results confirm our two hypotheses, 3.1 and 3.2. More specifically,
1. with regard to hypothesis 3.1, `CountVectorizer` and `DictionaryVectorizer` return identical feature vectors in most cases (compare the features and their weights for labels `nutrition` and `books`). For short texts, therefore, the performance of both should be roughly the same;
2. with regard to hypothesis 3.2, the TFICF version of `TfidfVectorizer` assigns higher weights to core class features, e.g.
   1. in the `cell-phones` class, TFICF returns _vintage_, _cell_, _phone_ and _flip_ as the most-highly-weighted features, all within the same weight tier (top tier, with a score of 1.10), and they are all core concepts in the category `cell-phones`. Compare that to TFIDF, where a key word like _phone_ falls down to the 3rd tier, behind `vintage`, or lower even than `cell`, with which it should be essentially correlated;
   2. in the `books` class, the word _book_ itself is in the 2nd weight tier for TFIDF but the 1st tier for TFICF;
   3. in the `nutrition` class, the word _nutrition_ itself is in the 3rd tier for TIFDF but again the 1st for TFICF, along with the rest of category-defining key words such as _capsules_ and _supplement_. 

In all cases, the feature weights returned by TFICF seem to closer to our own intution as to which words best describe each of the classes and should be weighted accordingly higher.


```python

```
