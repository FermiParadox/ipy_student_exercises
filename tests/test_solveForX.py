import re
from unittest import TestCase
from main import SolveForX


class Test__x_terms_strings(TestCase):
    def setUp(self):
        self.terms = set()
        for i in range(1, 5):
            self.terms.update(SolveForX()._x_terms_strings(x_terms=i))

    def test_non_empty(self):
        for t in self.terms:
            self.assertTrue(t)

    def test_minus_digits_times_x_format(self):
        for t in self.terms:
            match = re.search(r'-?\d+\*x', t)   # e.g "-21*x", "21*x"
            self.assertTrue(match, t)


class Test__non_x_terms_strings(TestCase):
    def setUp(self):
        self.terms = set()
        for i in range(1, 5):
            self.terms.update(SolveForX()._non_x_terms_strings(non_x_terms=i))

    def test_non_empty(self):
        for t in self.terms:
            self.assertTrue(t)

    def test_minus_digits_format(self):
        for t in self.terms:
            match = re.search(r'-?\d+', t)   # e.g "-21", "21"
            self.assertTrue(match, t)


class Test__hard_diff_left_and_right(TestCase):
    def test_non_empty(self):
        for i in range(1, 4):
            l, r = SolveForX()._hard_diff_left_and_right(x_terms=i, non_x_terms=i)
            self.assertTrue(l)
            self.assertTrue(r)
