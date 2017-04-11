from unittest import TestCase
from re import compile

from restriction_patterns import RestrictionBase, CUSTOM_RESTRICTIONS
from arbitrary_pieces import UnexpectedValueError


class Test__occurrence_op_and_num(TestCase):
    None

class Test__prohibit_nonsensical_occurrence_op_and_num(TestCase):
    None

class Test__check_duplicates_and_note_new_restriction(TestCase):
    def test_duplicate_detected(self):
        RestrictionBase(compile(r'1'))
        self.assertRaises(UnexpectedValueError, RestrictionBase, compile(r'1'))

    def test_noted_new_restriction(self):
        inst = RestrictionBase(compile('x'))
        # Must be in either key or val
        keys_and_vals = list(CUSTOM_RESTRICTIONS.keys()) + list(CUSTOM_RESTRICTIONS.values())
        self.assertIn(inst, keys_and_vals)


class TestRestrictionBase(TestCase):
    None




