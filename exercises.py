import abc
import random
import re

import mpmath
import sympy
from IPython.display import display
from sympy import sympify

import answer_patterns
import arbitrary_pieces
import languages
from arbitrary_pieces import r_int, solve_1rst_degree_poly, UnexpectedValueError
from ipython_ui.qa_display_widgets import QADisplayBox, FillGapsBox


class Exercise(metaclass=abc.ABCMeta):
    def __init__(self, display_class):
        if not issubclass(self.DEFAULT_DISPLAY_CLASS, QADisplayBox):
            raise UnexpectedValueError('{}'.format(self.DEFAULT_DISPLAY_CLASS))
        self.display_class = display_class
        self.question_title = self._question_title()
        self.question = self._question()
        self.question_in_latex = arbitrary_pieces.placeholder
        self.expected_answers = arbitrary_pieces.placeholder
        self.expected_answers_in_latex = arbitrary_pieces.placeholder
        self._create_remaining_data_based_on_question()

    def _create_remaining_data_based_on_question(self):
        self.question_in_latex = self._question_in_latex()
        self.expected_answers = self._expected_answers()
        self.expected_answers_in_latex = self._expected_answers_in_latex()

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
    def _expected_answers(self):
        """
        Return all variable names along with their expected values.
        The reason this is a dict is because some exercises
        will have multiple solutions, eg. polynomials.

        When there is "no solution" (eg. `x**2 = 1` in Real domain),
        *all* answers should have the equivalent NoSolution object assigned.
        Same goes for "any number", etc.

        :return: (dict)
        """
        pass

    # TODO test
    @staticmethod
    def _default_simpify_and_convert_to_latex(expected_answers_dct):
        d = {}
        for ans_name, ans_val in expected_answers_dct.items():
            if ans_val in arbitrary_pieces.SPECIAL_ANSWERS_TYPES:
                d.update({ans_name: ans_val})
            else:
                v = sympy.latex(sympify(ans_val))
                d.update({ans_name: v})

    @abc.abstractmethod
    def _expected_answers_in_latex(self):
        """For most cases `sympy.latex` can be used to convert all answers to latex
        by using `_default_simpify_and_convert_to_latex`.

        When `sympy.latex` doesn't do the job adequately a custom method is needed.
        """
        pass

    @abc.abstractproperty
    def special_answers_allowed(self):
        """
        Used for answer-objects that represent "no solution", "any number is a solution" etc.
        """
        pass

    @abc.abstractproperty
    def interchangeable_answers(self):
        """
        If x1, x2, x3 can be provided as an answer in non-specific order
        (for example the roots of a polynomial),
        then they are interchangeable and this method should
        `return {[x1, x2, x3], ..}`.
        """
        pass

    @abc.abstractproperty
    def DEFAULT_DISPLAY_CLASS(self):
        pass

    def display_in_jupyter(self):
        displ_class = self.display_class or self.DEFAULT_DISPLAY_CLASS
        display(displ_class(self).box())

    @staticmethod
    def _is_allowed_special_or_sympifiable_answer(answer_val, allowed_answer_types):
        """Checks if answer is either within allowed special-types or sympifiable."""
        # Covers special answer types like "AnyNumber"
        if answer_val in arbitrary_pieces.SPECIAL_ANSWERS_TYPES:
            return answer_val in allowed_answer_types
        # Consecutive ops are not allowed
        # (sympify doesn't mind them, so much check here)
        elif arbitrary_pieces.consecutive_operators_search(expr=str(answer_val)):
            return False
        else:
            try:
                sympify(answer_val, evaluate=False)
                return True
            except sympy.SympifyError:
                return False
            # (empty string would raise that)
            except IndexError:
                return False

    @abc.abstractmethod
    def _is_valid_answer(self, answer):
        """
        Checks if answer meets specified restrictions.

        Without restrictions, a user would be able to insert the question itself
        and sympify wouldn't be able to distinguish it from genuine attempts.
        Therefor, the dev must add restrictions (using answer-patterns)
        to prevent it from happening.

        :return: (bool)
        """
        pass

    @staticmethod
    def _is_correct_answer(answer, expected_answer):
        if answer in arbitrary_pieces.SPECIAL_ANSWERS_TYPES:
            return answer == expected_answer

        else:
            try:
                sympified_given_a = sympify(answer)
                sympified_expected_a = sympify(expected_answer)
                # (special expected answers can't be sympified, but if given_answer is '4'
                # and expecting a special answer, it should return False anyway.)
            except sympy.SympifyError:
                return False

            try:
                if mpmath.almosteq(sympified_given_a, sympified_expected_a, rel_eps=0.001):
                    return True
            except TypeError:
                return sympified_given_a == sympified_expected_a

        return False

    def _is_valid_and_correct_answer(self, answer_val, expected_answer):
        if self._is_allowed_special_or_sympifiable_answer(answer_val=answer_val,
                                                          allowed_answer_types=self.special_answers_allowed):
            if self._is_valid_answer(answer=answer_val):
                if self._is_correct_answer(answer=answer_val, expected_answer=expected_answer):
                    return True
        return False

    def _is_interchangeable_and_correct_answer(self, answer_val, expected_answers, used_interchangeable_a_names):
        for group in self.interchangeable_answers:
            if answer_val not in group:
                continue
            for interch_a_name in group:
                if interch_a_name in used_interchangeable_a_names:
                    continue
                else:
                    if self._is_valid_and_correct_answer(answer_val=answer_val,
                                                         expected_answer=expected_answers[interch_a_name]):
                        used_interchangeable_a_names.append(interch_a_name)
                        return True

    # TODO test individually for each Exercise
    def _check_all_answers(self, answers, expected_answers):
        used_interchangeable_a_names = []
        for given_answer_name, answer_val in answers.items():
            if self._is_valid_and_correct_answer(answer_val=answer_val,
                                                 expected_answer=expected_answers[given_answer_name]):
                continue
            # If answer name didn't match the expected val, then it might be interchangeable.
            if self._is_interchangeable_and_correct_answer(answer_val=answer_val,
                                                           expected_answers=expected_answers,
                                                           used_interchangeable_a_names=used_interchangeable_a_names):
                continue
            return False
        # If loop wasn't prematurely interrupted then all answers were correct.
        else:
            return True

    # (contains *args since it's used as callback)
    def check_all_answers(self, answers_given, *args):
        print(answers_given)
        return self._check_all_answers(answers=answers_given, expected_answers=self.expected_answers)


class SolveForXLinear(Exercise):
    """
    Example:
    3*x + 2 = 0

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
            left_side = '{a}*x+{b}'.format(a=a, b=b)
            right_side = '0'
        elif d == 2:
            # Real solution/no solution/infinite solutions
            a = r_int(10, '-+0', weights={0: 10})
            b = r_int(10, '-+0', weights={0: 8})
            left_side = '{a}*x+{b}'.format(a=a, b=b)
            right_side = '0'
        else:
            # Real solution/no solution/infinite solutions, any number of terms.
            left_side, right_side = self._hard_diff_left_and_right(x_terms=self.x_terms,
                                                                   non_x_terms=self.non_x_terms)

            # Add '0' if the side is empty.
            left_side = left_side or '0'
            right_side = right_side or '0'
        final_string = '='.join([left_side, right_side])
        final_string = final_string.replace('+-', '-')
        return final_string.replace('x', self.var_name)

    def _expected_answers(self):
        left_str, right_str = self.question.replace(' ', '').split('=')
        left_sympified = sympify(left_str)
        right_sympified = sympify(right_str)
        expr = left_sympified - right_sympified
        ans = solve_1rst_degree_poly(expr)
        return {self.VARIABLE_NAME: ans}

    def _expected_answers_in_latex(self):
        return Exercise._default_simpify_and_convert_to_latex(expected_answers_dct=self.expected_answers)

    def _is_valid_answer(self, answer):
        if answer in self.special_answers_allowed:
            return True

        patterns_allowed = [answer_patterns.DECIMAL.with_sign,
                            answer_patterns.INTEGER.with_sign,
                            answer_patterns.FRACTION_OF_INTS.with_sign]
        for patt in patterns_allowed:
            if re.fullmatch(patt, answer):
                return True
        return False

    def _question_in_latex(self):
        return '${}$'.format(self.question.replace('*', ''))

    @property
    def special_answers_allowed(self):
        return {arbitrary_pieces.AnyNumber,
                arbitrary_pieces.NoSolution}

    @property
    def interchangeable_answers(self):
        return {}


if __name__ == '__main__':
    _inst = SolveForXLinear(difficulty=3)
    print(_inst.question)
    print(_inst.expected_answers)
    while 1:
        _inst = SolveForXLinear(difficulty=2)
        _ques = _inst.question
        _ans = _inst.expected_answers
        if arbitrary_pieces.AnyNumber in _ans.values():
            print(_ques)
            print(_ans)
            break
