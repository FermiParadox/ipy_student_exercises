import sympy
import abc
from random_pieces import r_int
from sympy.abc import x


class UnexpectedValueError(Exception):
    pass


class Exercise(metaclass=abc.ABCMeta):
    @abc.abstractproperty
    def QUESTION_TITLE(self):
        pass

    @abc.abstractproperty
    def question(self):
        pass

    @abc.abstractproperty
    def answer(self):
        pass

    @abc.abstractproperty
    def answer_type(self):
        pass


class SolveForX(Exercise):
    """
    Example:
    3x + 2 = 0

    Fractional or decimal solutions should be kept for harder difficulty.
    """

    QUESTION_TITLE = 'Find the value of x.'
    answer_type = None

    def __init__(self, x_terms: int, non_x_terms: int):
        """
        :param x_terms: number of terms containing x
        :param non_x_terms: number of terms not containing x
        """
        self.x_terms = x_terms
        self.non_x_terms = non_x_terms

    def question(self):
        return '{a}*x + {b} = 0'.format(a=r_int(), b=r_int())

    def answer(self):
        pass
