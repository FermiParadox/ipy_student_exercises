import abc
import random
import re
import itertools
import sympy
from sympy.abc import x

import languages


# ---------------------------------------------------------------------------------
class UnexpectedValueError(Exception):
    """Used for Exceptions that should not be handled,
    instead of an existing Exception (to prevent accidental handling during `try`).
    """
    pass


# ---------------------------------------------------------------------------------
# PLACEHOLDER

class PlaceholderUsedError(Exception):
    """
    NOT TO BE HANDLED!
    Raised when placeholder is accidentally used.
    """
    pass


def _placeholder_error_func(*args, **kwargs):
    raise PlaceholderUsedError


class PlaceholderClass(object):
    """
    Used for adding an extra layer of bug preventions
    when accidentally placeholders have not been removed.

    WARNING: Some accidental uses of a placeholder will not raise an exception as they should.
        Only most common usage is covered.
    """

    def __init__(self, allowed_values=None, data_type=None, non_restricted_choice=False):
        self._allowed_values = allowed_values
        self._data_type = data_type
        self._non_restricted_choice = non_restricted_choice

    @property
    def allowed_values(self):
        return self._allowed_values

    @property
    def allowed_type(self):
        return self._data_type

    @property
    def non_restricted_choice(self):
        return self._non_restricted_choice


# TODO: add more methods
SUPPRESSED_MAGIC_METHODS = ('__bool__', '__eq__', '__ge__', '__gt__', '__le__', '__lt__',
                            '__ne__', '__get__', '__iter__', '__set__')
for magic_method in SUPPRESSED_MAGIC_METHODS:
    setattr(PlaceholderClass, magic_method, _placeholder_error_func)

placeholder = PlaceholderClass()


# ---------------------------------------------------------------------------------
def delimiter(num_of_lines, line_type='-'):
    """
    Creates a newline and then a long line string.
    """

    string = '\n'
    string += line_type * num_of_lines

    return string


def fat_delimiter(num_of_lines):
    return delimiter(num_of_lines=num_of_lines, line_type='=')


def print_delimiter(num_of_lines=80, line_type='='):
    print(delimiter(num_of_lines=num_of_lines, line_type=line_type))


# ---------------------------------------------------------------------------------
def class_children(cls):
    s = set()
    for subc in cls.__subclasses__():
        s.add(subc)
        s.update(class_children(cls=subc))
    return s


# ---------------------------------------------------------------------------------
_ALLOWED_POS_NEG_0 = set('+-0')
_MANDATORY_POS_NEG_0 = _ALLOWED_POS_NEG_0 - {'0'}


def r_int(bounds, pos_neg_0='+-0', excluded=(), weights=None) -> int:
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
    # Any int within [-1,4] with 3 having double the odds of appearing than any other int
    >>> r_int((-1, 4), weights={3: 2})

    :param bounds: Either a single int (the upper bound)
        or a tuple of ints (lower, upper bounds).
    :param pos_neg_0: String containing any of the following '+-' and optionally '0',
        corresponding to positive, negative and 0.
    :param excluded: Numbers to be excluded.
    :param weights: Weights of individual numbers (each number has `weight = 1` by default)
        To calculate the odds of a number appearing,
        divide its weight by the total weights of all numbers.
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
    nums_lst = list(nums)

    if weights:
        for n, w in weights.items():
            if n not in nums_lst:
                raise ValueError("Can't provide weight for number that is out of the bounds ({}).".format(n))
            if (w <= 0) or (not isinstance(w, int)):
                raise ValueError('Weight must be positive int.')
            nums_lst.extend(itertools.repeat(n, w-1))

    # (Easier to understand error compared to `choice`'s error.)
    if not nums_lst:
        raise ValueError('No number exists for given args.')
    return random.choice(nums_lst)


# ---------------------------------------------------------------------------------
def sometimes_replace_1x_with_x(expr, var_name):
    """
    Half of the time converts "1x" to "x".
    "31x", "461x", "4.1x", etc will always remain the same.
    """
    if random.choice([0, 1]):
        expr = re.sub(r'(?<![0-9.])1{}'.format(var_name), r'{}'.format(var_name), expr)
    return expr


# ---------------------------------------------------------------------------------
def solve_1rst_degree_poly(expr):
    """Returns the solution of a linear polynomial equation.

    WARNING: A `sympy.Eq(stmt)` output needs to be provided (not `sympy.Eq(stmt1, stmt2)`,
        since this method takes into account its peculiarities.
    """
    eq = sympy.Eq(expr)
    # `sympy.Eq` returns True (sympy-type True)
    # when the the generated expression is 2x-2x=0 or 0x=0,
    # and False when 0x=4.
    if eq is sympy.sympify(True):
        return AnyNumber
    elif eq is sympy.sympify(False):
        return NoSolution
    else:
        return sympy.solve(eq, x)[0]


# --------------------------------------------------------------------------------------------------------
# Escaped `re` special chars.
_re_compatible_op_symbols = ('\+', '-', '/', '\*')


def consecutive_operators_search(expr):
    patterns = itertools.product(_re_compatible_op_symbols, repeat=2)
    for t in patterns:
        pat = '{}{}'.format(*t)
        found = re.search(pat, expr)
        if found:
            return found


# ---------------------------------------------------------------------------------

ANY_NUM_SHORT_DESCRIPTION_MSG = languages.Message(
    texts_dct={
        languages.english: 'Any number.',
        languages.greek: 'Οποιοσδήποτε αριθμός',
    })

NO_SOLUTION_SHORT_DESCRIPTION_MSG = languages.Message(
    texts_dct={
        languages.english: 'No solution',
        languages.greek: 'Καμία λύση',
    })

ANY_NUM_LONG_DESCRIPTION_MSG = languages.Message(
    texts_dct={
        languages.english: 'Any number is a solution.',
        languages.greek: 'Οποιοσδήποτε αριθμός αποτελεί λύση.',
    })

NO_SOLUTION_LONG_DESCRIPTION_MSG = languages.Message(
    texts_dct={
        languages.english: 'No solution exists.',
        languages.greek: 'Δεν υπάρχει λύση.',
    })


class SpecialAnswerType(metaclass=abc.ABCMeta):
    @abc.abstractproperty
    def button_text(self):
        pass

    @abc.abstractproperty
    def long_description(self):
        pass


class AnyNumber(SpecialAnswerType):
    button_text = ANY_NUM_SHORT_DESCRIPTION_MSG
    long_description = ANY_NUM_LONG_DESCRIPTION_MSG


class NoSolution(SpecialAnswerType):
    button_text = NO_SOLUTION_SHORT_DESCRIPTION_MSG
    long_description = NO_SOLUTION_LONG_DESCRIPTION_MSG


SPECIAL_ANSWERS_TYPES = tuple(class_children(SpecialAnswerType))


SYMPY_ANSWERS_TYPES = tuple(i for i in dir(sympy.Q) if not i.startswith('_'))


if __name__ == '__main__':
    n = r_int(2, '-', (-1,))
    print(n)

    print(SPECIAL_ANSWERS_TYPES)
