from unittest import TestCase
from re import compile, fullmatch


import answer_patterns

from answer_patterns import _PatternBase, PATTERNS
from arbitrary_pieces import UnexpectedValueError


# ---------------------------------------------------------------------------------
class Test_total_matches_within_bounds(TestCase):
    WITHIN_BOUNDS_INPUTS = {'m>2': 3,
                            'm<=1': 1,
                            'm>=10': 111,
                            'm==45': 45,
                            'm!=5': 2,
                            '2<=m<15': 3}
    OUT_OF_BOUNDS_INPUTS = {'m>2': 2,
                            'm<=1': 34,
                            'm>=10': 8,
                            'm==45': 2,
                            'm!=5': 5,
                            '2<=m<15': 1}
    INVALID_INPUTS = {'2',
                      '<=',
                      '10>',
                      '2>1',
                      '4==4',
                      '4!=5',
                      '>x',
                      '2<x<4',
                      '1.3<m<4'}

    def test_within_bounds(self):
        for k, v in self.WITHIN_BOUNDS_INPUTS.items():
            self.assertTrue(_PatternBase.total_matches_within_bounds(m=v, bounds_str=k))

    def test_out_of_bounds(self):
        for k, v in self.OUT_OF_BOUNDS_INPUTS.items():
            self.assertFalse(_PatternBase.total_matches_within_bounds(m=v, bounds_str=k),
                             msg='m: {}, Pattern: {}'.format(v, k))

    def test_invalid_input(self):
        for i in self.INVALID_INPUTS:
            from random import randint
            self.assertRaises(UnexpectedValueError, _PatternBase.total_matches_within_bounds, randint(1, 1000), i)


class Test__check_duplicates_and_note_new_pattern(TestCase):
    def test_duplicate_detected(self):
        _PatternBase(compile(r'1'))
        self.assertRaises(UnexpectedValueError, _PatternBase, compile(r'1'))

    def test_noted_new_pattern(self):
        inst = _PatternBase(compile(r'x'))
        # Must be in either key or val
        self.assertIn(inst, PATTERNS)


class Test_PatternBase(TestCase):
    def test_str_not_accepted(self):
        self.assertRaises(UnexpectedValueError, _PatternBase, r'\d+')
        self.assertRaises(UnexpectedValueError, _PatternBase, '\d+')


# ---------------------------------------------------------------------------------
class TestEachPattern(TestCase):
    # fullmatch test-base
    def _fullmatch_base_(self, lst_of_strs, search_patt, _y_n):
        assert_func = self.assertTrue if (_y_n == 'y') else self.assertFalse
        for s in lst_of_strs:
            assert_func(fullmatch(search_patt, s),
                        'Pattern: {} \nnot found in: {}'.format(search_patt, s))

    def _does_fullmatch(self, lst_of_strs, pattern):
        return self._fullmatch_base_(lst_of_strs=lst_of_strs, search_patt=pattern, _y_n='y')

    def _does_not_fullmatch(self, lst_of_strs, pattern):
        return self._fullmatch_base_(lst_of_strs=lst_of_strs, search_patt=pattern, _y_n='n')

    # find_m_patterns test-base
    def _find2patterns_base(self, bounds_strs_lst, searched_patt, _y_n):
        m = 2
        m_str = 'm==2'
        assert_func = self.assertTrue if (_y_n == 'y') else self.assertFalse
        for expr in bounds_strs_lst:
            assert_func(answer_patterns.find_m_patterns(compile_obj=searched_patt, expr=expr, bounds_str=m_str),
                        'Did not find {} times \nthe pattern: {} \nin the string: {}'.format(m, searched_patt, expr))

    def _does_find2patterns(self, bounds_strs_lst, pattern):
        return self._find2patterns_base(bounds_strs_lst=bounds_strs_lst, searched_patt=pattern, _y_n='y')

    def _does_not_find2patterns(self, bounds_strs_lst, pattern):
        return self._find2patterns_base(bounds_strs_lst=bounds_strs_lst, searched_patt=pattern, _y_n='n')

    # TEMPLATE: fullmatch
    """
    # ?
    def test_fullmatch_?(self):
        self._does_fullmatch(lst_of_strs=[?],
                             pattern=answer_patterns.?)

    def test_not_fullmatch_?(self):
        self._does_not_fullmatch(lst_of_strs=[?],
                                 pattern=answer_patterns.?)

    """

    # TEMPLATE: find_m_patterns
    """
    def test_find2patterns_?(self):
        lst = [?]
        self._does_find2patterns(bounds_strs_lst=lst,
                           pattern=answer_patterns.?)

    def test_not_find2patterns_?(self):
        lst = [?]
        self._does_not_find2patterns(bounds_strs_lst=lst,
                               pattern=answer_patterns.?)
    """

    # integer
    def test_fullmatch_integer(self):
        self._does_fullmatch(lst_of_strs=['123', '-24', '0', '-0', '+0', '+2'],
                             pattern=answer_patterns.integer.with_sign)

    def test_not_fullmatch_integer(self):
        self._does_not_fullmatch(lst_of_strs=['93.2', '2.0', '.4', '-1/3', '-2x5', '4*2'],
                                 pattern=answer_patterns.integer)

    def test_find2patterns_integer(self):
        lst = ['1*z3+2+1.4', '135+0.1/7000-2.84']
        self._does_find2patterns(bounds_strs_lst=lst,
                                 pattern=answer_patterns.integer)

    def test_not_find2patterns_integer(self):
        lst = ['2+4+3', '1.73-4/2+7']
        self._does_not_find2patterns(bounds_strs_lst=lst,
                                     pattern=answer_patterns.integer)

    # decimal
    def test_fullmatch_decimal(self):
        self._does_fullmatch(lst_of_strs=['1.3', '0.004', '-1888.2', '+488.2', '0.0', '-0.0', '+0.0'],
                             pattern=answer_patterns.decimal.with_sign)

    def test_not_fullmatch_decimal(self):
        self._does_not_fullmatch(lst_of_strs=['1', '1422', '0', '.4', '4.', '4.2*x6', '4.2-3.1', '0x'],
                                 pattern=answer_patterns.decimal.with_sign)

    def test_find2patterns_decimal(self):
        lst = ['-1.4+1145.552', '(4.5*x5/2)**0.001']
        self._does_find2patterns(bounds_strs_lst=lst,
                                 pattern=answer_patterns.decimal)

    def test_not_find2patterns_decimal(self):
        lst = ['-1+1145.552', '.5+0.1']
        self._does_not_find2patterns(bounds_strs_lst=lst,
                                     pattern=answer_patterns.decimal)

    # fraction_of_ints
    def test_fullmatch_fraction_of_ints(self):
        self._does_fullmatch(lst_of_strs=['-1/3', '(+2)/4', '(-95)/(+34)'],
                             pattern=answer_patterns.fraction_of_ints.with_sign)

    def test_not_fullmatch_fraction_of_ints(self):
        self._does_not_fullmatch(lst_of_strs=['2/3.0', '-x4/2', '1.2'],
                                 pattern=answer_patterns.fraction_of_ints.with_sign)

    def test_find2patterns_fraction_of_ints(self):
        lst = ['1/3+4/20*0.1', '400/2-200/777', '(-10)/(+4)-4/20']
        self._does_find2patterns(bounds_strs_lst=lst,
                                 pattern=answer_patterns.fraction_of_ints.with_sign)

    def test_not_find2patterns_fraction_of_ints(self):
        lst = ['1/2.3+1/4', '(-1)/2/4']
        self._does_not_find2patterns(bounds_strs_lst=lst,
                                     pattern=answer_patterns.fraction_of_ints.with_sign)
