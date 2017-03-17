import sympy
import random
import abc
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


def solve_1rst_degree_poly(eq):
    # Sympy Eq returns 0 when the the generated expression is 0x=0 ...
    if eq == 0:
        return 'any Real'
    # ... and [] when it's 0x=4.
    elif eq is False:
        return []
    else:
        return sympy.solve(eq, x)


class SolveForX(Exercise):
    """
    Example:
    3x + 2 = 0

    Fractional or decimal solutions should be kept for harder difficulty.
    """
    ALLOWED_DIFFICULTIES = {1, 2, 3}

    def __init__(self, difficulty=1, x_terms=2, non_x_terms=2):
        """
        :param difficulty: Defines number of terms (if not provided)
            and type of solution (int, fraction etc)
        :param x_terms: number of terms containing x
        :param non_x_terms: number of terms not containing x
        """
        if difficulty not in self.ALLOWED_DIFFICULTIES:
            raise UnexpectedValueError('Difficulty {}, not allowed'.format(difficulty))
        if difficulty != max(self.ALLOWED_DIFFICULTIES):
            if (x_terms != 2) or (non_x_terms != 2):
                raise UnexpectedValueError("Number of terms can be set manually only on highest difficulty.")
        self.difficulty = difficulty
        self.x_terms = x_terms
        self.non_x_terms = non_x_terms
        super().__init__()

    def _question_title(self):
        pass

    @staticmethod
    def _x_terms_strings(x_terms):
        return {'{}*x'.format(r_int(10, '-+')) for _ in range(x_terms)}

    @staticmethod
    def _non_x_terms_strings(non_x_terms):
        return {str(r_int(10, '-+')) for _ in range(non_x_terms)}

    @staticmethod
    def _hard_diff_left_and_right(x_terms, non_x_terms):
        x_terms_strings = SolveForX._x_terms_strings(x_terms)
        non_x_terms_strings = SolveForX._non_x_terms_strings(non_x_terms)
        mixed = list(x_terms_strings | non_x_terms_strings)

        left_side_terms_num = random.randint(0, len(mixed))

        left_side_terms = mixed[:left_side_terms_num]
        left_side_terms = left_side_terms or ['0', ]
        right_side_terms = mixed[left_side_terms_num:]
        right_side_terms = right_side_terms or ['0', ]

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
            # Integer solution
            a = r_int(5, '-+')
            b = r_int(10, '-+') * a
            left_side = '{a}*x + {b}'.format(a=a, b=b)
            right_side = '0'
        else:
            # Real solution/no solution/infinite solutions, any number of terms.
            left_side, right_side = self._hard_diff_left_and_right(x_terms=self.x_terms,
                                                                   non_x_terms=self.non_x_terms)
        final_string = ' = '.join([left_side, right_side])
        final_string = final_string.replace('+-', '-')
        return final_string

    def _answer(self):
        left_str, right_str = self.question.replace(' ', '').split('=')
        left_sympified = sympify(left_str)
        right_sympified = sympify(right_str)
        eq = left_sympified - right_sympified
        return solve_1rst_degree_poly(eq)

    def _answer_types(self):
        return {sympify('1'), sympify('-1/2')}


if __name__ == '__main__':
    inst = SolveForX(difficulty=3)
    print(inst.question)
    print(inst.answer)
    while 1:
        inst = SolveForX(difficulty=3)
        q = inst.question
        a = inst.answer
        if a == 'any Real':
            print(q)
            print(a)
            break
