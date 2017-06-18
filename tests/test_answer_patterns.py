from unittest import TestCase
from re import compile, fullmatch


import answer_patterns

from answer_patterns import _PatternBase, PATTERNS


# ---------------------------------------------------------------------------------
class Test_total_matches_within_bounds(TestCase):

    def test_within_bounds(self):
        within_bounds_inputs = {'m>2': 3,
                                'm<=1': 1,
                                'm>=10': 111,
                                'm==45': 45,
                                'm!=5': 2,
                                '2<=m<15': 3}
        for k, v in within_bounds_inputs.items():
            self.assertTrue(_PatternBase.total_matches_within_bounds(m=v, bounds_str=k))

    def test_out_of_bounds(self):
        out_of_bounds_inputs = {'m>2': 2,
                                'm<=1': 34,
                                'm>=10': 8,
                                'm==45': 2,
                                'm!=5': 5,
                                '2<=m<15': 1}
        for k, v in out_of_bounds_inputs.items():
            self.assertFalse(_PatternBase.total_matches_within_bounds(m=v, bounds_str=k),
                             msg='m: {}, Pattern: {}'.format(v, k))

    def test_invalid_input(self):
        invalid_inputs = {'2',
                          '<=',
                          '10>',
                          '2>1',
                          '4==4',
                          '4!=5',
                          '>x',
                          '2<x<4',
                          '1.3<m<4'}
        for i in invalid_inputs:
            from random import randint
            self.assertRaises(ValueError, _PatternBase.total_matches_within_bounds, randint(1, 1000), i)


class Test__check_duplicates_and_note_new_pattern(TestCase):
    FILLER_ARGS = ([''],[''],[''])

    def test_duplicate_detected(self):
        _PatternBase(compile(r'1'), *self.FILLER_ARGS)
        self.assertRaises(ValueError, _PatternBase, compile(r'1'), *self.FILLER_ARGS)

    def test_new_pattern_noted(self):
        inst = _PatternBase(compile(r'x'), *self.FILLER_ARGS)
        # Must be in either key or val
        self.assertIn(inst, PATTERNS)


class Test_PatternBase(TestCase):
    FILLER_ARGS = Test__check_duplicates_and_note_new_pattern.FILLER_ARGS

    def test_str_not_accepted_as_patt(self):
        self.assertRaises(TypeError, _PatternBase, r'\d+', *self.FILLER_ARGS)
        self.assertRaises(TypeError, _PatternBase, '\d+', *self.FILLER_ARGS)


# ---------------------------------------------------------------------------------
class TestEachPattern(TestCase):
    # fullmatch test-base
    def _fullmatch_base_(self, search_patt, _y_n):
        if _y_n == 'y':
            assert_func = self.assertTrue
            lst_of_strs = getattr(search_patt, 'fullmatch')
        else:
            assert_func = self.assertFalse
            lst_of_strs = getattr(search_patt, 'no_fullmatch')
        for s in lst_of_strs:
            assert_func(fullmatch(search_patt, s),
                        '\nPattern: {} \nexpression: {}'.format(search_patt, s))

    def _does_fullmatch(self, pattern):
        return self._fullmatch_base_(search_patt=pattern, _y_n='y')

    def _does_not_fullmatch(self, pattern):
        return self._fullmatch_base_(search_patt=pattern, _y_n='n')

    # find_m_patterns test-base
    def _does_find2patterns(self, pattern):
        m = 2
        m_str = 'm==2'
        for expr in getattr(pattern, 'two_matches'):
            self.assertTrue(answer_patterns.found_m_patterns(compile_obj=pattern, expr=expr, bounds_str=m_str),
                            'Did not find {} times \nthe pattern: {} \nin the string: {}'.format(m, pattern, expr))

    def test_all_patterns_examples_and_non_examples(self):
        for p in PATTERNS:
            self._does_fullmatch(p)
            self._does_not_fullmatch(p)
            self._does_find2patterns(p)
