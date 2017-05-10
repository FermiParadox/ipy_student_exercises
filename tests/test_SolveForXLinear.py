import re
from unittest import TestCase

from exercises import SolveForXLinear
from answer_patterns import find_m_patterns
from arbitrary_pieces import AnyNumber, NoSolution
from tests import REPETITIONS


class Test__x_terms_strings(TestCase):
    def setUp(self):
        self.terms = set()
        for i in range(1, 5):
            self.terms.update(SolveForXLinear()._x_terms_strings(x_terms=i))

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
            self.terms.update(SolveForXLinear()._non_x_terms_strings(non_x_terms=i))

    def test_non_empty(self):
        for t in self.terms:
            self.assertTrue(t)

    def test_minus_digits_format(self):
        for t in self.terms:
            match = re.search(r'-?\d+', t)   # e.g "-21", "21"
            self.assertTrue(match, t)


class Test__hard_diff_left_and_right(TestCase):
    def test_at_least_one_side_non_empty(self):
        for i in range(1, 5):
            l, r = SolveForXLinear()._hard_diff_left_and_right(x_terms=i, non_x_terms=i)
            self.assertTrue(l or r)

    def test_n_x_terms(self):
        n_x_terms = 6
        for _ in range(REPETITIONS // 100):
            l, r = SolveForXLinear()._hard_diff_left_and_right(x_terms=n_x_terms, non_x_terms=3)

            x_terms = re.findall(r'\d+\*x', l+r)
            self.assertEqual(len(x_terms), n_x_terms, (l, r))

    def test_n_non_x_terms(self):
        n_non_x_terms = 6
        for _ in range(REPETITIONS // 100):
            l, r = SolveForXLinear()._hard_diff_left_and_right(x_terms=3, non_x_terms=n_non_x_terms)
            non_x_terms = re.findall(r'\d+(?!\d*\*x)', '='.join([l, r]))
            self.assertEqual(len(non_x_terms), n_non_x_terms, (l, r, non_x_terms))


class Test_question(TestCase):
    def setUp(self):
        self.questions = set()
        for _ in range(REPETITIONS//100):
            for d in SolveForXLinear.ALLOWED_DIFFICULTIES:
                inst = SolveForXLinear(difficulty=d)
                self.questions.add(inst.question)

    def test_signs_not_consecutive(self):
        for q in self.questions:
            self.assertNotIn('+-', q)

    def test_equal_sign_present(self):
        for q in self.questions:
            self.assertIn('=', q)

    def test_contains_x(self):
        for q in self.questions:
            self.assertIn('x', q)


class Test__check_all_answers(TestCase):

    def test_special_answers_occur_often_enough_in_d2(self):
        reps = REPETITIONS//10
        detected = 0
        for _ in range(reps):
            # only diff==2 focuses on teaching special answers
            inst = SolveForXLinear(difficulty=2)
            # Don't detect `=0` or `40`
            # Assumes question is always \d*x+\d=\d
            if find_m_patterns(r'(?<![=\d])0', inst.question.replace(' ', ''), 'm==2'):
                detected += 1
        self.assertGreater(detected/reps, .05)
        self.assertLess(detected/reps, .2)

    def _test_answer_correctness_base(self, dct, true_or_false_assertion):
        if true_or_false_assertion is True:
            assert_f = self.assertTrue
        elif true_or_false_assertion is False:
            assert_f = self.assertFalse
        else:
            raise TypeError

        inst = SolveForXLinear()
        for q, answers_lst in dct.items():
            inst.question = q
            for a in answers_lst:
                expected_a = inst.answers['x']
                assert_f(inst._check_all_answers(answers={'x': a}, expected_answers={'x': expected_a}),
                         msg='\nGiven answer: {}\nExpected: {}'.format(a, expected_a))

    def test_correct_answers(self):
        dct = {
            '2*x-1=0': ['1/2', '+1/2', '(+1)/2', '0.5', '0.50000000000000000000000001'],
            '0*x-0=0': [AnyNumber],
            '0*x-1=0': [NoSolution],
        }
        return self._test_answer_correctness_base(dct=dct, true_or_false_assertion=True)

    def test_incorrect_answers(self):
        dct = {
            '2*x-1=0': ['-1/2', '1.0/2', '(1)/2', '-0.5', '0.51'],
            '0*x-0=0': ['6', '-', '=+-', NoSolution],
            '0*x-1=0': ['6', '-', '=+-', AnyNumber],
        }
        return self._test_answer_correctness_base(dct=dct, true_or_false_assertion=False)


