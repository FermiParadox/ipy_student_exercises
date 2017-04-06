from unittest import TestCase

from main import Exercise
import sympy
from arbitrary_pieces import AnyNumber, NoSolution


VALID_SYMPY_NUMBERS = [4, -2, -2.2, '4', '4.2', '-4.2', ]
VALID_SYMPY_FRACTIONS = ['-2/4', '2/3']     # Fractions are type: sympy.Mul
NOT_SYMPY_NUMBERS = ['2+1']
INVALID_SYMPY_EXPRESSIONS = ['-', '0-', '2/.']


def _sympify_type(expr):
    return sympy.sympify(expr, evaluate=False)


class Test__is_valid_answer(TestCase):
    def test_sympy_number_valid(self):
        for n in VALID_SYMPY_NUMBERS:
            self.assertTrue(Exercise._is_valid_answer(answer=n, allowed_answer_types=[sympy.Number]),
                            msg='{} type is: {}'.format(n, _sympify_type(expr=n)))

    def test_sympy_fraction_valid(self):
        for n in VALID_SYMPY_FRACTIONS:
            self.assertTrue(Exercise._is_valid_answer(answer=n, allowed_answer_types=[sympy.Mul]),
                            msg='{} type is: {}'.format(n, _sympify_type(expr=n)))

    def test_sympy_number_invalid(self):
        for n in NOT_SYMPY_NUMBERS:
            self.assertFalse(Exercise._is_valid_answer(answer=n, allowed_answer_types=[sympy.Number]),
                             msg='{} type is: {}'.format(n, _sympify_type(expr=n)))

    def test_no_error_when_unsympifiable(self):
        for n in INVALID_SYMPY_EXPRESSIONS:
            self.assertFalse(Exercise._is_valid_answer(answer=n, allowed_answer_types=[sympy.Number]),
                             msg=n)

    def test_anynumber_valid(self):
        self.assertTrue(Exercise._is_valid_answer(answer=AnyNumber(), allowed_answer_types=[AnyNumber]))

    def test_nosolution_valid(self):
        self.assertTrue(Exercise._is_valid_answer(answer=NoSolution(), allowed_answer_types=[NoSolution]))

    def test_nosolution_invalid(self):
        self.assertFalse(Exercise._is_valid_answer(answer=NoSolution(), allowed_answer_types=[AnyNumber]))






