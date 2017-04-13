from unittest import TestCase
from re import compile


import permitted_patterns

from permitted_patterns import PermissionBase, CUSTOM_PERMISSIONS
from arbitrary_pieces import UnexpectedValueError


# ---------------------------------------------------------------------------------
# PermissionBase
class Test_total_matches_within_bounds(TestCase):
    WITHIN_BOUNDS_INPUTS = {'m>2': 3,
                            'm<=1': 1,
                            'm>=10': 111,
                            'm==45': 45,
                            'm!=5': 2,
                            '2<=m<15': 3}
    OUT_OF_BOUNDS_INPUTS = {'m>2': 2,
                            'm<=1': 34,
                            'm>=10': 8,
                            'm==45': 2,
                            'm!=5': 5,
                            '2<=m<15': 1}
    INVALID_INPUTS = {'2',
                      '<=',
                      '10>',
                      '2>1',
                      '4==4',
                      '4!=5',
                      '>x',
                      '2<x<4',
                      '1.3<m<4'}

    def test_within_bounds(self):
        for k, v in self.WITHIN_BOUNDS_INPUTS.items():
            self.assertTrue(PermissionBase.total_matches_within_bounds(m=v, occ_str=k))

    def test_out_of_bounds(self):
        for k, v in self.OUT_OF_BOUNDS_INPUTS.items():
            self.assertFalse(PermissionBase.total_matches_within_bounds(m=v, occ_str=k),
                             msg='m: {}, Pattern: {}'.format(v, k))

    def test_invalid_input(self):
        for i in self.INVALID_INPUTS:
            from random import randint
            self.assertRaises(UnexpectedValueError, PermissionBase.total_matches_within_bounds, randint(1, 1000), i)


class Test__check_duplicates_and_note_new_permission(TestCase):
    def test_duplicate_detected(self):
        PermissionBase(compile(r'1'))
        self.assertRaises(UnexpectedValueError, PermissionBase, compile(r'1'))

    def test_noted_new_permission(self):
        inst = PermissionBase(compile(r'x'))
        # Must be in either key or val
        keys_and_vals = list(CUSTOM_PERMISSIONS.keys()) + list(CUSTOM_PERMISSIONS.values())
        self.assertIn(inst, keys_and_vals)


# ---------------------------------------------------------------------------------
class TestPermissionBase(TestCase):
    def test_str_not_accepted(self):
        self.assertRaises(UnexpectedValueError, PermissionBase, r'\d+')
        self.assertRaises(UnexpectedValueError, PermissionBase, '\d+')


class TestEachPermission(TestCase):
    # Fullmatch
    def _fullmatch_base_(self, lst_of_strs, permission, _y_n):
        assert_func = self.assertTrue if (_y_n == 'y') else self.assertFalse
        for s in lst_of_strs:
            assert_func(permission.fullmatch(s),
                        '{} not found in: {}'.format(permission.compile_obj.pattern, s))

    def _does_fullmatch(self, lst_of_strs, permission):
        return self._fullmatch_base_(lst_of_strs=lst_of_strs, permission=permission, _y_n='y')

    def _does_not_fullmatch(self, lst_of_strs, permission):
        return self._fullmatch_base_(lst_of_strs=lst_of_strs, permission=permission, _y_n='n')

    # Findall
    def _findall_base(self, occ_str_to_m_found_map, permission, _y_n):
        assert_func = self.assertTrue if (_y_n == 'y') else self.assertFalse
        for occ_str, expr in occ_str_to_m_found_map.items():
            assert_func(permission.findall(expr=expr, occ_str=occ_str),
                        'Pattern: {} not found in: {} as many times as defined by: {}'.format(
                            permission.compile_obj.pattern, expr, occ_str))

    def _does_findall(self, occ_str_to_m_found_map, permission):
        return self._findall_base(occ_str_to_m_found_map=occ_str_to_m_found_map, permission=permission, _y_n='y')

    def _does_not_findall(self, occ_str_to_m_found_map, permission):
        return self._findall_base(occ_str_to_m_found_map=occ_str_to_m_found_map, permission=permission, _y_n='n')

    # TEMPLATE: fullmatch
    """
    # ?
    def test_fullmatch_?(self):
        self._does_fullmatch(lst_of_strs=[?],
                             permission=permitted_patterns.?)

    def test_not_fullmatch_?(self):
        self._does_not_fullmatch(lst_of_strs=[?],
                                 permission=permitted_patterns.?)

    """

    # TEMPLATE: findall
    """

    def test_findall_?(self):
        self._does_findall(occ_str_to_m_found_map=?,
                           permission=permitted_patterns.?)

    def test_not_findall_?(self):
        self._does_not_findall(occ_str_to_m_found_map=?,
                               permission=permitted_patterns.?)

    """

    # integer
    def test_fullmatch_integer(self):
        self._does_fullmatch(lst_of_strs=['123', '-24', '0', '-0', '+0', '+2'],
                             permission=permitted_patterns.integer)

    def test_not_fullmatch_integer(self):
        self._does_not_fullmatch(lst_of_strs=['93.2', '2.0', '.4', '-1/3', '-2x', '4*2'],
                                 permission=permitted_patterns.integer)

    def test_findall_integer(self):
        dct = {
            'm>1': '-270/45',
            'm<3': '-270/45',
            'm==2': '-270/45',
            '2<m<=6': '-270/45+1',
            '20>m>=1': '-270/45+1',
            'm!=1': '0+6',
            '1<m!=1': '0+6',
        }
        self._does_findall(occ_str_to_m_found_map=dct,
                           permission=permitted_patterns.integer)

    def test_not_findall_integer(self):
        dct = {
            'm>2': '-270/45',
            'm<2': '-270/45',
            'm==7': '-270/45',
            '4<m<=6': '-270/45+1',
            '2>m>=1': '-270/45+1',
            'm!=2': '0+6',
            '1<m!=2': '0+6',
        }
        self._does_not_findall(occ_str_to_m_found_map=dct,
                               permission=permitted_patterns.integer)

    # decimal
    def test_fullmatch_decimal(self):
        self._does_fullmatch(lst_of_strs=['1.3', '0.004', '-1888.2', '+488.2', '0.0', '-0.0', '+0.0'],
                             permission=permitted_patterns.decimal)

    def test_not_fullmatch_decimal(self):
        self._does_not_fullmatch(lst_of_strs=['1', '1422', '0', '.4', '4.', '4.2*x', '4.2-3.1', '0x'],
                                 permission=permitted_patterns.decimal)


