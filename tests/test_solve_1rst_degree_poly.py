from unittest import TestCase

from arbitrary_pieces import solve_1rst_degree_poly, AnyNumber, NoSolution


class Test_solve_1rst_degree_poly(TestCase):
    def test_one_solution(self):
        from sympy.abc import x
        sol = solve_1rst_degree_poly(expr=4*x+2)
        self.assertIsNot(sol, AnyNumber)

    def test_no_solution(self):
        from sympy.abc import x
        sol = solve_1rst_degree_poly(expr=0*x-2)
        self.assertIsInstance(sol, NoSolution)

    def test_any_number_is_solution(self):
        from sympy.abc import x
        sol1 = solve_1rst_degree_poly(expr=0*x)
        self.assertIsInstance(sol1, AnyNumber)
        sol2 = solve_1rst_degree_poly(expr=2*x-2*x)
        self.assertIsInstance(sol2, AnyNumber)
