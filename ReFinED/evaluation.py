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
        return num / denom
    return 0.0



def diff_annotations(
    ann1: list[tuple[int, int, str, str]],
    ann2: list[tuple[int, int, str, str]]
) -> list[list[tuple[int, int, str, str]]]:
    """TODO: add description

    Parameters
    ----------
    ann1: list[tuple[int, int, str, str]]
        TODO: fill
    ann2: list[tuple[int, int, str, str]]
        TODO: fill

    Returns
    -------
    list[tuple[int, int, str, str]]
        Given all elements in either `ann1` or `ann2`, and considering the
        first and second sub-elements in each element (the two integers
        denoting `start` and `end` position indexes for each annotation),
        returns a new set with all elements from either `ann1` or `ann2`
        whose start and end positions do not match those of any other element
        in the other set (`ann2` or `ann1` respectively).

    Examples
    --------

    Raises
    ------

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
    _union = ann1_idxs.union(ann2_idxs)
    _diff = _union - _intersection
    return list(map(
        lambda x: True if (x[0], x[1]) in _diff else False,
        ann1 + ann2
    ))







def test_character_coverage():
    for text, annotations, metric in character_coverage_tests:
        assert character_coverage(text, annotations) == metric


def test_diff_annotations():
    anns = [
        [(2, 4, 'ph', 'Phi Eta')],
        [(0, 2, 'be', 'Beta Epsilon')],
    ]
    for ann1 in anns:
        for ann2 in anns:
            diff_annotations(ann1, ann2)







if __name__ == '__main__':
    test_diff_annotations()
#     test_character_coverage()
#
#     testmod()