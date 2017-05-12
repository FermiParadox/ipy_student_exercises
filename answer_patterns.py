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


PLUS_OR_MINUS_PATT = r'(?:\+|-)'
MAYBE_PLUS_OR_MINUS_PATT = PLUS_OR_MINUS_PATT + '?'


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

    def __new__(cls, compile_obj):
        try:
            patt = compile_obj.pattern
            inst = str.__new__(cls, patt)
        except AttributeError:
            # (`re.compile` objects contain `.pattern`)
            raise UnexpectedValueError('`compile_obj` must be a `re.compile` object.')
        if ('_' in patt) or (' ' in patt):
            raise UnexpectedValueError('Pattern must not include whitespaces or "_".')
        inst.__dict__.update({'with_sign': MAYBE_PLUS_OR_MINUS_PATT + inst})
        _PatternBase._check_duplicates_and_note_new_pattern(pattern=patt)
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
? = _PatternBase(re.compile(r'\'))
"""


# (Using `re.compile` for visibility provided by IDE)
# Patterns must account for the fact that variables might be named 'x1'.
# TODO: Add examples and counter-examples here that are automatically checked by PatternBase
INTEGER = _PatternBase(re.compile(r'(?<![a-zA-Z0-9.])\d+(?!\.)'))
DECIMAL = _PatternBase(re.compile(r'(?<![a-zA-Z0-9.])\d+\.\d+'))
FRACTION_OF_INTS = _PatternBase(re.compile(r'{i}/{i}'.format(i=INTEGER)))
FRACTION_OF_INTS_WITH_PARENTHESES = _PatternBase(
    re.compile(r'(?:{i}/{i})|(?:\({s}{i}\)/{i})|(?:{i}/\({s}{i}\))|(?:\({s}{i}\)/\({s}{i}\))'.format(i=INTEGER,
                                                                                                     s=PLUS_OR_MINUS_PATT)))


if __name__ == '__main__':

    print_delimiter()
    print('PATTERNS AND OBJ:\n')
    for p in PATTERNS:
        print('{}'.format(p))

    print_delimiter()
    print(INTEGER)
    print(re.fullmatch(INTEGER, '2'))
    print(re.fullmatch(INTEGER, '+2'))
    print(re.fullmatch(INTEGER.with_sign, '+2'))

