import random
from main import UnexpectedValueError
from sympy import sympify


_ALLOWED_POS_NEG_0 = set('+-0')
_MANDATORY_POS_NEG_0 = _ALLOWED_POS_NEG_0 - {'0'}


def r_int(bounds, pos_neg_0='+-0', excluded=()) -> int:
    """
    Return random integer within bounds, excluding a list of ints.

    Examples:
    =========

    # Any int including 0 within [-7, 7]
    >>> r_int(7)
    # Any int excluding 0 within [-7, 7]
    >>> r_int(7, '+-')
    # A positive int including 0 within [-7, 7] (effectively within [0, 7])
    >>> r_int(7, '+0')
    # A negative int within [-5 to 3] excluding -4 and -1
    >>> r_int((-5, 3), '-', {-4, -1})

    :param bounds: Either a single int (the upper bound)
        or a tuple of ints (lower, upper bounds).
    :param pos_neg_0: String containing any of the following '+-' and optionally '0',
        corresponding to positive, negative and 0.
    :param excluded: Numbers to be excluded.
    """
    if isinstance(bounds, int):
        b1, b2 = -bounds, bounds
    else:
        # .. it's a tuple.
        b1, b2 = bounds

    if (not pos_neg_0) or (pos_neg_0 == '0'):
        raise UnexpectedValueError('Need at least one of the following: {}.'.format(_MANDATORY_POS_NEG_0))
    extra_chars = set(pos_neg_0) - _ALLOWED_POS_NEG_0
    if extra_chars:
        raise UnexpectedValueError('Only {} are allowed. Found: {}.'.format(_ALLOWED_POS_NEG_0, extra_chars))

    nums = set(range(b1, b2+1)) - set(excluded)
    if '0' not in pos_neg_0:
        nums -= {0}
    if '-' not in pos_neg_0:
        nums = {i for i in nums if not i < 0}
    if '+' not in pos_neg_0:
        nums = {i for i in nums if not i > 0}

    # Easier to understand error compared to `choice`'s error.
    if not nums:
        raise ValueError('No number exists for given args.')
    return random.choice(list(nums))


if __name__ == '__main__':

    n = r_int(2, '-', (-1,))
    print(n)
