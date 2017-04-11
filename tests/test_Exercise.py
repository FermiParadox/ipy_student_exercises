from unittest import TestCase

from exercises import Exercise
import sympy
from arbitrary_pieces import AnyNumber, NoSolution, ANY_NUMBER, NO_SOLUTION


def _sympify_type(expr):
    return sympy.sympify(expr, evaluate=False)


class Test__is_special_or_sympifiable_answer(TestCase):
    VALID_SYMPY_NUMBERS = [4, -2, -2.2, '4', '4.2', '-4.2', ]
    VALID_SYMPY_FRACTIONS = ['-2/4', '2/3']  # Fractions are type: sympy.Mul
    NOT_SYMPY_NUMBERS = ['2+1']
    INVALID_SYMPY_EXPRESSIONS = ['-', '0-', '2/.']

    def test_sympy_number_valid(self):
        for n in self.VALID_SYMPY_NUMBERS:
            self.assertTrue(Exercise._is_special_or_sympifiable_answer(answer=n, allowed_answer_types=[sympy.Number]),
                            msg='{} type is: {}'.format(n, _sympify_type(expr=n)))

    def test_sympy_fraction_valid(self):
        for n in self.VALID_SYMPY_FRACTIONS:
            self.assertTrue(Exercise._is_special_or_sympifiable_answer(answer=n, allowed_answer_types=[sympy.Mul]),
                            msg='{} type is: {}'.format(n, _sympify_type(expr=n)))

    def test_sympy_number_invalid(self):
        for n in self.NOT_SYMPY_NUMBERS:
            self.assertFalse(Exercise._is_special_or_sympifiable_answer(answer=n, allowed_answer_types=[sympy.Number]),
                             msg='{} type is: {}'.format(n, _sympify_type(expr=n)))

    def test_no_error_when_unsympifiable(self):
        for n in self.INVALID_SYMPY_EXPRESSIONS:
            self.assertFalse(Exercise._is_special_or_sympifiable_answer(answer=n, allowed_answer_types=[sympy.Number]),
                             msg=n)

    def test_anynumber_valid(self):
        self.assertTrue(Exercise._is_special_or_sympifiable_answer(answer=ANY_NUMBER, allowed_answer_types=[AnyNumber]))

    def test_nosolution_valid(self):
        self.assertTrue(
            Exercise._is_special_or_sympifiable_answer(answer=NO_SOLUTION, allowed_answer_types=[NoSolution]))

    def test_nosolution_invalid(self):
        self.assertFalse(
            Exercise._is_special_or_sympifiable_answer(answer=NO_SOLUTION, allowed_answer_types=[AnyNumber]))


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
        self.assertTrue(Exercise._is_correct_answer(answer=NO_SOLUTION, expected_answer=NO_SOLUTION))
        self.assertTrue(Exercise._is_correct_answer(answer=ANY_NUMBER, expected_answer=ANY_NUMBER))

    def test_special_answer_is_wrong(self):
        self.assertFalse(Exercise._is_correct_answer(answer=NO_SOLUTION, expected_answer=ANY_NUMBER))
        self.assertFalse(Exercise._is_correct_answer(answer=ANY_NUMBER, expected_answer=NO_SOLUTION))
        self.assertFalse(Exercise._is_correct_answer(answer=ANY_NUMBER, expected_answer='4'))
        self.assertFalse(Exercise._is_correct_answer(answer='4', expected_answer=ANY_NUMBER))

