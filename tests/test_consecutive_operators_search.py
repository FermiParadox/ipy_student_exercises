from unittest import TestCase

from arbitrary_pieces import consecutive_operators_search


class Test__consecutive_operators_search(TestCase):
    def test_finds_pattern(self):
        expressions = ['*/', '+-', '-/', '--', '++']
        for expr in expressions:
            self.assertTrue(consecutive_operators_search(expr=expr))

    def test_doesnt_find_pattern(self):
        expressions = ['1+(-2)+4-x', '4/(-2)*8', '(-4*2+1)', ]
        for expr in expressions:
            self.assertFalse(consecutive_operators_search(expr=expr))
