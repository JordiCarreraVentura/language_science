from doctest import testmod


character_coverage_tests = [
    # text, annotations, float
    ('alpha', [(2, 4, 'ph', 'Phi Eta')], 0.4),
    ('beta', [(0, 2, 'be', 'Beta Epsilon')], 0.5),
    ('omega', [(0, 1, 'o', 'Omicron'), (1, 5, 'mega', 'Megas')], 1.0),
    ('kappa', [], 0.0),
]


not_int = lambda x: False if isinstance(x, int) else True
not_incr = lambda x: True if x[0] >= x[1] else False



def f_score(p: float, r: float, f=1.0) -> float:
    """
    Calculate the F_beta score, a weighted harmonic mean of precision and recall.

    Parameters
    ----------
    p : float
        The precision value, must be in the range [0.0, 1.0].
    r : float
        The recall value, must be in the range [0.0, 1.0].
    f : float, optional
        The beta value determining the weight of precision in the score calculation (default is 1.0).

    Returns
    -------
    float
        The F_beta score.

    Raises
    ------
    ValueError
        If any input parameter is not a floating point number.
        If parameters `p` or `r` are not in the range [0.0, 1.0].

    Examples
    --------
    >>> f_score(0.7, 0.8)
    0.75

    >>> f_score(0.6, 0.9, 2.0)
    0.82
    """
    if not isinstance(p, float) or p > 1 or p < 0:
        raise ValueError(
            'Argument `p` must be a floating point number '
            f'between 0.0 and 1.0, got {p} instead.'
        )
    if not isinstance(r, float) or r > 1 or r < 0:
        raise ValueError(
            'Argument `r` must be a floating point number '
            f'between 0.0 and 1.0, got {r} instead.'
        )
    if not isinstance(f, float):
        raise ValueError(f'Argument `f` must be a floating point number, got {f}')

    coef = f ** 2
    num = p * r
    denom = (p * coef) + r
    return round((1 + coef) * (num / denom), 2)


def check_annotations(annotations: list[tuple[int, int, str, str]]) -> None:
    if not isinstance(annotations[0], tuple):
        raise ValueError('Values stored in `annotations` must be tuples, got '
                         f'"{annotations[0]}"')
    starts = [ann[0] for ann in annotations]
    ends = [ann[1] for ann in annotations]
    if list(filter(not_int, starts)) \
    or list(filter(not_int, ends)) \
    or list(filter(not_incr, [(x, y) for x, y in zip(starts, ends)])):
        raise ValueError('Values stored in `annotations` must be tuples, '
                         'the first two elements in the tuple must be '
                         'integers, and the second integer must be greater '
                         f'than the first one, but got "{annotations}"')



def character_coverage(
    text: str,
    annotations: list[tuple[int, int, str, str]]
) -> float:
    """Calculates the percentage of characters in text `text` covered by the
    entity annotations in `annotations`.

    It is calculated according to the following formula:

    `coverage = covered / total`

    Where
    - `total` is defined as the length of `text`
    - `covered` is defined as the delta between the start and end positions
      of each annotation in `annotations`.
    (all lengths are measured in characters)

    That is, given a 5-character long text containing a single entity spanning
    from index 1 to index 3,
    ```
    coverage = (3-1 / 5)
             = ( 2  / 5)
             =    0.4
    ```

    Parameters
    ----------
    text: str
        The text where the entity annotations have been extracted from.
    annotations: list[tuple[int, int, str, str]]
        The entity annotations extracted from the input text (note that the
        extraction must be performed prior to calling this function). Each
        annotation consists of 4 items:
        - start: int: the index denoting the start of the extracted entity in
                      `text`.
        - end:   int: the index denoting its end position.
        - text:  str: the substring corresponding to the text span of the ex-
                      tracted entity.
        - entity str: the title of the Wikipedia page corresponding to the de-
                      tected entity.

    Examples
    --------
    >>> character_coverage('alpha', [(2, 4, 'ph', 'Phi Eta')])
    0.4
    >>> character_coverage('beta', [(0, 2, 'be', 'Beta Epsilon')])
    0.5
    >>> character_coverage(
    ...   'omega',
    ...   [(0, 1, 'o', 'Omicron'), (1, 5, 'mega', 'Megas')]
    ... )
    1.0
    >>> character_coverage('kappa', [])
    0.0

    Returns
    -------
    float
        The floating point number denoting the measure defined as `coverage` above.

    Raises
    ------
    ValueError
        If `text` or `annotation` are not of the expected data type
        (data typing is explicitly enforced).

    """
    if not isinstance(text, str):
        raise ValueError(f'Argument `text` must be a string, got "{text}"')
    if not isinstance(annotations, list):
        raise ValueError('Argument `annotations` must be a list, got '
                         f'"{annotations}"')
    if not annotations:
        return 0.0
    check_annotations(annotations)

    num = 0.0
    denom = len(text)
    for start, end, _, _ in annotations:
        delta = end - start
        num += delta
    if denom:
        return round(num / denom, 2)
    return 0.0



def diff_annotations(
    ann1: list[tuple[int, int, str, str]],
    ann2: list[tuple[int, int, str, str]]
) -> tuple[
    list[list[tuple[int, int, str, str]]],
    list[list[tuple[int, int, str, str]]]
]:
    """Compare and deduplicate annotations between two lists based on start and end positions.

    Parameters
    ----------
    ann1: list[tuple[int, int, str, str]]
        The first list of items to compare and deduplicate according to their
        integers `int`.
    ann2: list[tuple[int, int, str, str]]
        The second list of items to compare and deduplicate according to their
        integers `int`.

    Returns
    -------
    tuple[
        list[tuple[int, int, str, str]],
        list[tuple[int, int, str, str]]
    ]
        Given all elements in either `ann1` or `ann2`, and considering the
        first and second sub-elements in each element (the two integers
        denoting `start` and `end` position indexes for each annotation),
        returns two new lists, one for `ann1` and another for `ann2`,
        respectively, such that each new list contains all elements in the
        corresponding input argument whose start and end positions match none
        of those for the elements in the other list.

    Raises
    ------
    ValueError
        If `text` or `annotation` are not of the expected data type
        (data typing is explicitly enforced).

    Examples
    --------
    >>> ann1 = []
    >>> ann2 = []
    """
    if not ann2:
        return ann1
    if not ann1:
        return ann2
    check_annotations(ann1)
    check_annotations(ann2)

    ann1_idxs = set([(start, end) for start, end, _, _ in ann1])
    ann2_idxs = set([(start, end) for start, end, _, _ in ann2])
    _intersection = ann1_idxs.intersection(ann2_idxs)

    ann1_diff = ann1_idxs - _intersection
    ann2_diff = ann2_idxs - _intersection

    is_uniq = lambda x: True \
              if (x[0], x[1]) in ann1_diff \
              or (x[0], x[1]) in ann2_diff \
              else False

    ann1_uniq = list(filter(is_uniq, ann1))
    ann2_uniq = list(filter(is_uniq, ann2))

    return ann1_uniq, ann2_uniq




def test_character_coverage():
    for text, annotations, metric in character_coverage_tests:
        assert character_coverage(text, annotations) == metric


def test_diff_annotations():

    ann1 = (2, 4, 'ph', 'Phi Eta')
    ann2 = (0, 2, 'be', 'Beta Epsilon')

    anns = [
        ([ann1], [ann2], 1, 1),
        ([ann1, ann2], [ann2], 1, 0),
        ([ann2], [ann2, ann1], 0, 1),
        ([ann1], [ann1], 0, 0),
        ([ann2], [ann2], 0, 0),
    ]
    for ann1, ann2, expected_len_diff1, expected_len_diff2 in anns:
        ann1_uniq, ann2_uniq = diff_annotations(ann1, ann2)
        assert len(ann1_uniq) == expected_len_diff1
        assert len(ann2_uniq) == expected_len_diff2


def test_f_score():
    prfs = [
        (1.00, 1.00, 1.0),
        (1.00, 0.75, 1.0),
        (1.00, 0.50, 1.0),
        (1.00, 0.25, 1.0),
        (0.70, 0.80, 1.0),
        (0.60, 0.90, 2.0)
    ]
    for p, r, f in prfs:
        f_score(p, r, f=f)
        continue
        print(p, r, f, f_score(p, r, f=f))




if __name__ == '__main__':
    test_f_score()
    test_character_coverage()
    test_diff_annotations()
    testmod()