from unittest import TestCase
from random import randint, choice

from arbitrary_pieces import sometimes_replace_1x_with_x
from tests import REPETITIONS


class Test_sometimes_replace_1x_with_x(TestCase):
    def test_1x_to_x_conversion_ratio(self):
        l = []
        for _ in range(REPETITIONS):
            l.append(sometimes_replace_1x_with_x('1x', 'x'))
        ratio_x = l.count('x') / len(l)
        ratio_1x = l.count('1x') / len(l)
        self.assertAlmostEqual(ratio_x + ratio_1x, 1, 'ratio x: {}, ratio 1x: {}'.format(ratio_x, ratio_1x))
        self.assertGreaterEqual(ratio_x, .40)   # About 50%

    def test_num1x_not_converted(self):
        for _ in range(REPETITIONS):
            num1x_expr = '{}1x'.format(randint(1, 100))
            final_expr = sometimes_replace_1x_with_x(num1x_expr, var_name='x')
            self.assertEqual(num1x_expr, final_expr)

    def test_never_change_not_selected_var_names(self):
        for _ in range(REPETITIONS):
            expr = '1{}+1r'.format(choice(list('abcdefg')))
            final_expr = sometimes_replace_1x_with_x(expr, var_name='y')
            self.assertEqual(expr, final_expr)

    def test_decimals_not_converted(self):
        for _ in range(REPETITIONS):
            num1x_expr = '{}.1x'.format(randint(1, 100))
            final_expr = sometimes_replace_1x_with_x(num1x_expr, var_name='x')
            self.assertEqual(num1x_expr, final_expr)
