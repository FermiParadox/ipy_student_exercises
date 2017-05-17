"""
Contains patterns used in order to determine if answer has expected form,
or detect answer contents (eg. ints, decimals, etc).

Sympy's `Assumptions` or `type(sympify())` are not used
since they sometimes produce counter-intuitive results,
eg. `type(sympify('1/3'))` is `Pow`
    `sympify('1+2').is_integer` is `True`
"""


import re
import operator


from arbitrary_pieces import UnexpectedValueError, print_delimiter


_PLUS_OR_MINUS_PATT = r'(?:\+|-)'
_MAYBE_PLUS_OR_MINUS_PATT = _PLUS_OR_MINUS_PATT + '?'


PATTERNS = []


class _PatternBase(str):
    _ALLOWED_OCCURRENCE_STR_OPS = {
        r'==': operator.eq,
        r'!=': operator.ne,
        r'>': operator.gt,
        r'>=': operator.ge,
        r'<': operator.lt,
        r'<=': operator.le,
    }

    with_sign = ''  # (added here simply for static analysis by IDE)

    def __new__(cls, compile_obj, fullmatch, no_fullmatch, two_matches, **kwargs):
        """String that can be used by `re` module as pattern
        to validate user's answers.

        The rest of the parameters are examples used automatically during unit-testing,
        and must be non-empty containers.

        :param compile_obj: The output of `re.compile` (used for visibility provided by IDE)
        :param fullmatch: Container of strings that `fullmatch` the pattern.
        :param no_fullmatch: (container)
        :param two_matches: Container of strings that each contains 2 matches of the pattern.
        :param kwargs: The rest of the kwargs of `str` class.
        :return: (str)
        """
        try:
            patt = compile_obj.pattern
            inst = str.__new__(cls, patt)
        except AttributeError:
            # (`re.compile` objects contain `.pattern`)
            raise UnexpectedValueError('`compile_obj` must be a `re.compile` object.')
        if ('_' in patt) or (' ' in patt):
            raise UnexpectedValueError('Pattern must not include whitespaces or "_".')
        if not (fullmatch and no_fullmatch and two_matches):
            # No need to test if they are containers
            # since unit-testing would fail anyway if they weren't.
            raise UnexpectedValueError('Expected non empty containers as match/mismatch examples.')
        inst.__dict__.update({'with_sign': _MAYBE_PLUS_OR_MINUS_PATT + inst})
        inst.__dict__.update({'fullmatch': fullmatch, 'no_fullmatch': no_fullmatch, 'two_matches': two_matches})
        _PatternBase._check_duplicates_and_note_new_pattern(pattern=inst)
        return inst

    @staticmethod
    def total_matches_within_bounds(m, bounds_str):
        """
        Checks if total matches found meet the criteria of `bounds_str`.

        :param m: Total bounds found.
        :param bounds_str: Expresses bounds of total matches found (must contain 'm').
            eg. 'm>2', 'm!=3', '2<=m<3'
        :return: (bool)
        """
        for k in _PatternBase._ALLOWED_OCCURRENCE_STR_OPS:
            match = re.fullmatch('m({})(\d+)'.format(k), bounds_str)
            if match:
                op, num = match.group(1), int(match.group(2))
                return _PatternBase._ALLOWED_OCCURRENCE_STR_OPS[op](m, num)
        for k1 in _PatternBase._ALLOWED_OCCURRENCE_STR_OPS:
            for k2 in _PatternBase._ALLOWED_OCCURRENCE_STR_OPS:
                match = re.fullmatch('(\d+)({k1})m({k2})(\d+)'.format(k1=k1, k2=k2), bounds_str)
                if match:
                    num1, op1, op2, num2 = int(match.group(1)), match.group(2), match.group(3), int(match.group(4))
                    within_1st_bound = _PatternBase._ALLOWED_OCCURRENCE_STR_OPS[op1](num1, m)
                    within_2nd_bound = _PatternBase._ALLOWED_OCCURRENCE_STR_OPS[op2](m, num2)
                    return within_1st_bound and within_2nd_bound
        else:
            raise UnexpectedValueError('Occurrence string {} not matching requirements.'.format(bounds_str))

    @staticmethod
    def _check_duplicates_and_note_new_pattern(pattern):
        existing_patterns = [i for i in PATTERNS]
        if pattern in existing_patterns:
            raise UnexpectedValueError('Following pattern exists more than once: {}'.format(pattern))
        else:
            PATTERNS.append(pattern)

    @staticmethod
    def findall(compile_obj, expr, bounds_str):
        matches = re.findall(compile_obj, expr)
        tot_matches_found = len(matches)
        return _PatternBase.total_matches_within_bounds(m=tot_matches_found, bounds_str=bounds_str)


find_m_patterns = _PatternBase.findall


# TEMPLATE
"""
? = _PatternBase(re.compile(r'\'),
                 fullmatch=,
                 no_fullmatch=,
                 two_matches=)
"""


# Patterns must account for the fact that variables might be named 'x1'.
INTEGER = _PatternBase(
    re.compile(r'(?<![a-zA-Z0-9.])\d+(?!\.)'),
    fullmatch=['123', '24', '0'],
    no_fullmatch=['(10990)', '-+1', '93.2', '2.00', '.4', '-1/3', 'x2', 'x52', '4*'],
    two_matches=['1*z3+2+1.4-x24', '135+0.1/7000-2.84', '4x-5y'])
DECIMAL = _PatternBase(
    re.compile(r'(?<![a-zA-Z0-9.])\d+\.\d+'),
    fullmatch=['1.3', '0.004', '1888.2', '488.024', '0.0'],
    no_fullmatch=['1422', '0', '.4', '.422', '4.', '455.', '4.2*x6', '4.23.1', 'x22.4'],
    two_matches=['-1.4+1145.552+4+2', '(4.5*x5/2)**0.001'])
FRACTION_OF_INTS = _PatternBase(
    re.compile(r'{i}/{i}'.format(i=INTEGER)),
    fullmatch=['1/7', '111/7', '1/557', '877/9087'],
    no_fullmatch=['1/7x', '1/5+7', '(-2)/4', '.9/2', '4.9/2', '1/9/7'],
    two_matches=['1/3+7/8-0*122/2.3', '1/3+7/8x', '-2/566-(9/8)+(-11)/3'])
FRACTION_OF_INTS_WITH_PARENTHESES = _PatternBase(
    re.compile(r'(?:{i}/{i})|(?:\({s}{i}\)/{i})|(?:{i}/\({s}{i}\))|(?:\({s}{i}\)/\({s}{i}\))'.format(i=INTEGER,
                                                                                                     s=_PLUS_OR_MINUS_PATT)),
    fullmatch=['1/3', '(+2)/4', '(-95)/(+34)'],
    no_fullmatch=['2/3.0', '(1)/2', '-x4/2', '1.2'],
    two_matches=['1/3+4/20*0.1', '400/2-200/777', '(-10)/(+4)-4/20'])


if __name__ == '__main__':

    print_delimiter()
    print('PATTERNS:\n')
    for p in PATTERNS:
        print('{}'.format(p))

    print_delimiter()
    print(INTEGER)
    print(re.fullmatch(INTEGER, '2'))
    print(re.fullmatch(INTEGER, '+2'))
    print(re.fullmatch(INTEGER.with_sign, '+2'))

