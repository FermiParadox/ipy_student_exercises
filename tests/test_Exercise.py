from unittest import TestCase

from exercises import Exercise
import sympy
from arbitrary_pieces import AnyNumber, NoSolution


def _sympify_type(expr):
    return sympy.sympify(expr, evaluate=False)


class Test__is_allowed_special_or_sympifiable_answer(TestCase):
    SYMPIFIABLE_EXPRESSIONS = [4, -2, -2.2, '4', '4.2', '-4.2', '2+1']
    UNSYMPIFIABLE_EXPRESSIONS = ['-', '+-1', '*-2', '0-', '2/.']

    def test_sympifiable(self):
        for n in self.SYMPIFIABLE_EXPRESSIONS:
            self.assertTrue(Exercise._is_allowed_special_or_sympifiable_answer(answer_val=n, allowed_answer_types=[sympy.Number]),
                            msg='{} type is: {}'.format(n, _sympify_type(expr=n)))

    def test_unsympifiable(self):
        for n in self.UNSYMPIFIABLE_EXPRESSIONS:
            self.assertFalse(Exercise._is_allowed_special_or_sympifiable_answer(answer_val=n, allowed_answer_types=[NoSolution, AnyNumber]),
                             msg=n)

    def test_AnyNumber_valid(self):
        self.assertTrue(Exercise._is_allowed_special_or_sympifiable_answer(answer_val=AnyNumber, allowed_answer_types=[AnyNumber]))

    def test_AnyNumber_invalid(self):
        self.assertFalse(
            Exercise._is_allowed_special_or_sympifiable_answer(answer_val=AnyNumber, allowed_answer_types=[NoSolution]))

    def test_NoSolution_valid(self):
        self.assertTrue(
            Exercise._is_allowed_special_or_sympifiable_answer(answer_val=NoSolution, allowed_answer_types=[NoSolution]))

    def test_NoSolution_invalid(self):
        self.assertFalse(
            Exercise._is_allowed_special_or_sympifiable_answer(answer_val=NoSolution, allowed_answer_types=[AnyNumber]))


class Test__is_correct_answer(TestCase):
    def test_sympy_number_is_correct(self):
        expected_a = '4'
        for a in [4, '4', '+4', '4.0', '4.004']:
            self.assertTrue(Exercise._is_correct_answer(answer=a, expected_answer=expected_a),
                            msg='{} not equal (or almost equal) to {}'.format(a, expected_a))

    def test_sympy_number_is_wrong(self):
        expected_a = '4'
        for a in [2, '2', '-4', '3.0', '4.008']:
            self.assertFalse(Exercise._is_correct_answer(answer=a, expected_answer=expected_a),
                             msg='{} equal (or almost equal) to {}'.format(a, expected_a))

    def test_special_answer_is_correct(self):
        self.assertTrue(Exercise._is_correct_answer(answer=NoSolution, expected_answer=NoSolution))
        self.assertTrue(Exercise._is_correct_answer(answer=AnyNumber, expected_answer=AnyNumber))

    def test_special_answer_is_wrong(self):
        self.assertFalse(Exercise._is_correct_answer(answer=NoSolution, expected_answer=AnyNumber))
        self.assertFalse(Exercise._is_correct_answer(answer=AnyNumber, expected_answer=NoSolution))
        self.assertFalse(Exercise._is_correct_answer(answer=AnyNumber, expected_answer='4'))
        self.assertFalse(Exercise._is_correct_answer(answer='4', expected_answer=AnyNumber))

