import abc
import random
import sympy
import mpmath

from sympy import sympify
from IPython.display import display


import languages
from never_importer import UnexpectedValueError
from arbitrary_pieces import r_int, solve_1rst_degree_poly, AnyNumber, NoSolution, SPECIAL_ANSWERS_TYPES
from qa_display_widgets import QADisplayBox, FillGapsBox


class Exercise(metaclass=abc.ABCMeta):
    def __init__(self, display_class):
        if not issubclass(self.DEFAULT_DISPLAY_CLASS, QADisplayBox):
            raise UnexpectedValueError('{}'.format(self.DEFAULT_DISPLAY_CLASS))
        self.display_class = display_class
        self.question_title = self._question_title()
        self.question = self._question()
        self.question_in_latex = self._question_in_latex()
        self.answer = self._answer()
        self.answer_types = self._answer_types()

    @abc.abstractmethod
    def _question_title(self):
        pass

    @abc.abstractmethod
    def _question(self):
        pass

    @abc.abstractmethod
    def _question_in_latex(self):
        pass

    @abc.abstractmethod
    def _answer(self):
        pass

    @abc.abstractmethod
    def _answer_types(self):
        pass

    @abc.abstractproperty
    def DEFAULT_DISPLAY_CLASS(self):
        pass

    def display_in_jupyter(self):
        displ_class = self.display_class or self.DEFAULT_DISPLAY_CLASS
        display(displ_class(self).box())

    @staticmethod
    def _is_valid_answer(answer, allowed_answer_types):
        types_tuple = tuple(allowed_answer_types)
        # Covers special answer types like "AnyNumber"
        if isinstance(answer, SPECIAL_ANSWERS_TYPES):
            return isinstance(answer, types_tuple)
        # Otherwise, it must be sympified before checked.
        else:
            try:
                sympified_a = sympify(answer, evaluate=False)
                return isinstance(sympified_a, types_tuple)
            except sympy.SympifyError:
                return False

    @staticmethod
    def _is_correct_answer(answer, expected_answer):
        """
        Checks if answer is correct.

        WARNING: Assumes answer is "valid" as defined above.
        """
        if answer == expected_answer:
            return True
        else:
            try:
                if mpmath.almosteq(sympify(answer), sympify(expected_answer), rel_eps=0.001):
                    return True
            except sympy.SympifyError:
                return False

        return False

    @staticmethod
    def is_correct_and_valid_answer(answer, expected_answer, allowed_answer_types):
        if Exercise._is_valid_answer(answer=answer, allowed_answer_types=allowed_answer_types):
            if Exercise._is_correct_answer(answer=answer, expected_answer=expected_answer):
                return True
        return False


class SolveForXLinear(Exercise):
    """
    Example:
    3x + 2 = 0

    Fractional or decimal solutions should be kept for harder difficulty.
    """
    ALLOWED_DIFFICULTIES = {1, 2, 3}
    DEFAULT_TERM_N_ON_HIGH_DIFF = 3
    VARIABLE_NAME = 'x'
    DEFAULT_DISPLAY_CLASS = FillGapsBox

    def __init__(self, difficulty=1, var_name='x', display_class=None,
                 x_terms=DEFAULT_TERM_N_ON_HIGH_DIFF, non_x_terms=DEFAULT_TERM_N_ON_HIGH_DIFF):
        """
        :param difficulty: Defines number of terms (if not provided)
            and type of solution (int, fraction etc)
        :param var_name: Name of variable.
        :param x_terms: number of terms containing x
        :param non_x_terms: number of terms not containing x
        """
        if difficulty not in self.ALLOWED_DIFFICULTIES:
            raise UnexpectedValueError('Difficulty {}, not allowed'.format(difficulty))
        if difficulty != max(self.ALLOWED_DIFFICULTIES):
            if (x_terms != self.DEFAULT_TERM_N_ON_HIGH_DIFF) or (non_x_terms != self.DEFAULT_TERM_N_ON_HIGH_DIFF):
                raise UnexpectedValueError("Number of terms can be set manually only on highest difficulty.")
        self.difficulty = difficulty
        self.var_name = var_name
        self.x_terms = x_terms
        self.non_x_terms = non_x_terms
        super().__init__(display_class=display_class)

    def _question_title(self):
        return languages.Message(
            texts_dct={
                languages.english: 'Find the value of {}.'.format(self.var_name),
                languages.greek: 'Βρες την τιμή του {}.'.format(self.var_name),
            })

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
        return final_string.replace('x', self.var_name)

    def _answer(self):
        left_str, right_str = self.question.replace(' ', '').split('=')
        left_sympified = sympify(left_str)
        right_sympified = sympify(right_str)
        expr = left_sympified - right_sympified
        ans = solve_1rst_degree_poly(expr)
        return {self.VARIABLE_NAME: ans}

    def _question_in_latex(self):
        return '${}$'.format(self.question.replace('*', ''))

    def _answer_types(self):
        return {sympy.Number, sympy.Mul, AnyNumber, NoSolution}


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
