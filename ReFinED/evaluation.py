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

    num = 0.0
    denom = len(text)
    for start, end, _, _ in annotations:
        delta = end - start
        num += delta
    if denom:
        return num / denom
    return 0.0


def test_character_coverage():
    for text, annotations, metric in character_coverage_tests:
        assert character_coverage(text, annotations) == metric







if __name__ == '__main__':
    test_character_coverage()

    testmod()