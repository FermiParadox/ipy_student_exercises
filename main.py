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
            # Real solution, any number of terms.
            x_terms_strings = {'{}*x'.format(r_int(10, '-+')) for _ in range(self.x_terms)}
            non_x_terms_strings = {str(r_int(10, '-+')) for _ in range(self.non_x_terms)}
            mixed = x_terms_strings | non_x_terms_strings
            left_side_terms_num = random.randint(0, len(mixed))
            left_side_terms = list(mixed)[:left_side_terms_num]
            left_side_terms = left_side_terms or ['0', ]
            right_side_terms = list(mixed)[left_side_terms_num:]
            right_side_terms = right_side_terms or ['0', ]
            left_side = '+'.join(left_side_terms)
            right_side = '+'.join(right_side_terms)
        final_string = ' = '.join([left_side, right_side])
        final_string = final_string.replace('+-', '-')
        return final_string

    def _answer(self):
        left, right = self.question.replace(' ', '').split('=')
        left_sympified = sympify(left)
        right_sympified = sympify(right)
        return sympy.solve(sympy.Eq(left_sympified, right_sympified), x)

    def _answer_types(self):
        return {sympify('1'), sympify('-1/2')}


if __name__ == '__main__':
    inst = SolveForX(difficulty=3)
    print(inst.question)
    print(inst.answer)
