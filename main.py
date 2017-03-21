import sympy
import random
import abc

import languages

from sympy.abc import x
from sympy import sympify

from random_pieces import r_int
from never_importer import UnexpectedValueError


class Exercise(metaclass=abc.ABCMeta):
    def __init__(self):
        self.question = self._question()
        self.question_title = self._question_title()
        self.answer = self._answer()
        self.answer_types = self._answer_types()

    @abc.abstractmethod
    def _question_title(self):
        pass

    @abc.abstractmethod
    def _question(self):
        pass

    @abc.abstractmethod
    def _answer(self):
        pass

    @abc.abstractmethod
    def _answer_types(self):
        pass


class AnyNumber(object):
    pass
ANY_NUMBER = AnyNumber()


class NoSolution(object):
    pass
NO_SOLUTION = NoSolution()


def solve_1rst_degree_poly(expr):
    """Returns the solution of a linear polynomial equation.

    WARNING: A `sympy.Eq(stmt)` output needs to be provided (not `sympy.Eq(stmt1, stmt2)`,
        since this method takes into account its peculiarities.
    """
    eq = sympy.Eq(expr)
    # `sympy.Eq` returns True (sympy-type True)
    # when the the generated expression is 2x-2x=0 or 0x=0,
    # and False when 0x=4.
    if eq is sympify(True):
        return ANY_NUMBER
    elif eq is sympify(False):
        return NO_SOLUTION
    else:
        return sympy.solve(eq, x)[0]


class SolveForXLinear(Exercise):
    """
    Example:
    3x + 2 = 0

    Fractional or decimal solutions should be kept for harder difficulty.
    """
    ALLOWED_DIFFICULTIES = {1, 2, 3}
    DEFAULT_TERM_N_ON_HIGH_DIFF = 3
    QUESTION_TITLE = languages.Message(
        texts_dct={
            languages.english: 'Find the value of x.',
            languages.greek: 'Βρες την τιμή του x.',
        })

    def __init__(self, difficulty=1, x_terms=DEFAULT_TERM_N_ON_HIGH_DIFF, non_x_terms=DEFAULT_TERM_N_ON_HIGH_DIFF):
        """
        :param difficulty: Defines number of terms (if not provided)
            and type of solution (int, fraction etc)
        :param x_terms: number of terms containing x
        :param non_x_terms: number of terms not containing x
        """
        if difficulty not in self.ALLOWED_DIFFICULTIES:
            raise UnexpectedValueError('Difficulty {}, not allowed'.format(difficulty))
        if difficulty != max(self.ALLOWED_DIFFICULTIES):
            if (x_terms != self.DEFAULT_TERM_N_ON_HIGH_DIFF) or (non_x_terms != self.DEFAULT_TERM_N_ON_HIGH_DIFF):
                raise UnexpectedValueError("Number of terms can be set manually only on highest difficulty.")
        self.difficulty = difficulty
        self.x_terms = x_terms
        self.non_x_terms = non_x_terms
        super().__init__()

    def _question_title(self):
        return self.QUESTION_TITLE

    @staticmethod
    def _x_terms_strings(x_terms):
        return ['{}*x'.format(r_int(10, '-+')) for _ in range(x_terms)]

    @staticmethod
    def _non_x_terms_strings(non_x_terms):
        return [str(r_int(10, '-+')) for _ in range(non_x_terms)]

    @staticmethod
    def _hard_diff_left_and_right(x_terms, non_x_terms):
        x_terms_strings = SolveForXLinear._x_terms_strings(x_terms)
        non_x_terms_strings = SolveForXLinear._non_x_terms_strings(non_x_terms)
        mixed = x_terms_strings + non_x_terms_strings
        random.shuffle(mixed)

        left_side_terms_num = random.randint(0, len(mixed))

        left_side_terms = mixed[:left_side_terms_num]
        right_side_terms = mixed[left_side_terms_num:]

        left_side = '+'.join(left_side_terms)
        right_side = '+'.join(right_side_terms)
        return left_side, right_side

    def _question(self):
        d = self.difficulty
        if d == 1:
            # Positive integer solution
            a = r_int(5, '+')
            b = r_int(10, '-') * a
            left_side = '{a}*x + {b}'.format(a=a, b=b)
            right_side = '0'
        elif d == 2:
            # Real solution/no solution/infinite solutions
            a = r_int(10, '-+0')
            b = r_int(10, '-+0')
            left_side = '{a}*x + {b}'.format(a=a, b=b)
            right_side = '0'
        else:
            # Real solution/no solution/infinite solutions, any number of terms.
            left_side, right_side = self._hard_diff_left_and_right(x_terms=self.x_terms,
                                                                   non_x_terms=self.non_x_terms)

            # Add '0' if the side is empty.
            left_side = left_side or '0'
            right_side = right_side or '0'
        final_string = ' = '.join([left_side, right_side])
        final_string = final_string.replace('+-', '-')
        return final_string

    def _answer(self):
        left_str, right_str = self.question.replace(' ', '').split('=')
        left_sympified = sympify(left_str)
        right_sympified = sympify(right_str)
        expr = left_sympified - right_sympified
        return solve_1rst_degree_poly(expr)

    def _answer_types(self):
        return {sympy.Number, AnyNumber, NoSolution}


if __name__ == '__main__':
    _inst = SolveForXLinear(difficulty=3)
    print(_inst.question)
    print(_inst.answer)
    while 1:
        _inst = SolveForXLinear(difficulty=2)
        _ques = _inst.question
        _ans = _inst.answer
        if isinstance(_ans, AnyNumber):
            print(_ques)
            print(_ans)
            break
