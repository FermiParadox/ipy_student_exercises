from unittest import TestCase
from random import randint

from tests import REPETITIONS
from arbitrary_pieces import r_int, _ALLOWED_POS_NEG_0, UnexpectedValueError


class Test_r_int(TestCase):
    def test_0bound_exactly_0(self):
        self.assertEquals(r_int(0), 0)

    def test_XX_bounds_exactly_X(self):
        self.assertEquals(r_int((4, 4)), 4)

    def test_is_int(self):
        self.assertTrue(isinstance(r_int(10000), int))

    def test_within_upper_bound(self):
        for _ in range(REPETITIONS):
            bound = randint(0, 100)
            self.assertLessEqual(r_int(bound), bound)

    def test_within_lower_bound(self):
        for _ in range(REPETITIONS):
            bound = randint(0, 100)
            self.assertGreaterEqual(r_int(bound),  -bound)

    def test_only_negatives(self):
        for _ in range(REPETITIONS):
            self.assertLess(r_int(100, '-'), 0)

    def test_only_positives(self):
        for _ in range(REPETITIONS):
            self.assertGreater(r_int(100, '+'), 0)

    def test_0_included(self):
        s = set()
        small_n = 1
        # Odds of missing the bug for enough reps is extremely small
        # (about 10e-200 for 1k reps)
        for _ in range(10*4):
            s.update({
                r_int(small_n, '+0'),
                r_int(small_n, '-0'),
                r_int(small_n, '-0+'),
                r_int(small_n, )
            })
        self.assertIn(0, s)

    def test_0_excluded(self):
        s = set()
        small_n = 1
        # Odds of missing the bug for enough reps is extremely small
        # (about 10e-200 for 1k reps)
        for _ in range(REPETITIONS):
            s.update({
                r_int(small_n, '+'),
                r_int(small_n, '-'),
                r_int(small_n, '-+'),
            })
        self.assertNotIn(0, s)

    def test_either_pos_or_neg_enforced(self):
        self.assertRaises(UnexpectedValueError, r_int, 100, '0')
        self.assertRaises(UnexpectedValueError, r_int, 100, '')

    def test_posneg0_extra(self):
        from string import printable
        for l in set(printable)-_ALLOWED_POS_NEG_0:
            posneg0 = '-0+{}'.format(l)
            self.assertRaises(UnexpectedValueError, r_int, 100, posneg0)

    def test_no_nums_for_given_args(self):
        for _ in range(REPETITIONS):
            self.assertRaises(ValueError, r_int, (3, 6), '-')
            self.assertRaises(ValueError, r_int, (-5, -3), '+')
            self.assertRaises(ValueError, r_int, (0, 0), '+-')

    def test_excluded(self):
        for _ in range(REPETITIONS):
            bound = 3
            excluded_n = randint(-bound, bound)
            self.assertNotEqual(excluded_n, r_int(bound, excluded={excluded_n}))

    def test_weight_for_disallowed_number(self):
        for _ in range(REPETITIONS):
            self.assertRaises(ValueError, r_int, (-5, +3), '+', (), {-1: 2})

    def test_weight_effect_on_odds(self):
        nums_lst = []
        weight_1 = 3
        for _ in range(REPETITIONS):
            nums_lst.append(r_int((0, 2), weights={1: weight_1}))
        ratio_1 = nums_lst.count(1) / len(nums_lst)
        weight_ratio_1 = weight_1 / (1+weight_1+1)
        self.assertAlmostEqual(weight_ratio_1, ratio_1, delta=.01)

    def test_weight_of_negative_or_0_doesnt_raise(self):
        self.assertIsNotNone(r_int((-1, 2), weights={-1: 4, 0: 4}))

    def test_non_positive_weight(self):
        self.assertRaises(ValueError, r_int, 5, weights={1: 0})
        self.assertRaises(ValueError, r_int, 5, weights={1: -4})
