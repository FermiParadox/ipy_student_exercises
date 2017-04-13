import re
import operator


from arbitrary_pieces import UnexpectedValueError, print_delimiter

CUSTOM_PERMISSIONS = {}


class PermissionBase(object):
    _ALLOWED_OCCURRENCES_OPS = {
        r'==': operator.eq,
        r'!=': operator.ne,
        r'>': operator.gt,
        r'>=': operator.ge,
        r'<': operator.lt,
        r'<=': operator.le,
    }
    PLUS_OR_MINUS_PATT = r'(?:\+|-)?'

    def __init__(self, compile_obj, include_sign=False):
        """
        Instances of this class contain the patterns
        that are allowed or disallowed as an answer.

        :param include_sign: If True, will ALSO match expressions starting with a '+' or '-' followed by the pattern.
        """
        if not hasattr(compile_obj, 'pattern'):
            raise UnexpectedValueError('Expecting a `re.compile` object. Most likely you did not provide one.')
        if include_sign:
            self.compile_obj = re.compile(PermissionBase.PLUS_OR_MINUS_PATT + compile_obj.pattern)
        else:
            self.compile_obj = compile_obj
        PermissionBase._check_duplicates_and_note_new_permission(self)

    @staticmethod
    def total_matches_within_bounds(m, occ_str):
        """
        Checks if total matches found meet the criteria of `occ_str`.

        :param occ_str: Expresses bounds of total matches found (must contain 'm').
            eg. 'm>2', 'm!=3', '2<=m<3'
        :return:
        """
        for k in PermissionBase._ALLOWED_OCCURRENCES_OPS:
            match = re.fullmatch('m({})(\d+)'.format(k), occ_str)
            if match:
                op, num = match.group(1), int(match.group(2))
                return PermissionBase._ALLOWED_OCCURRENCES_OPS[op](m, num)
        for k1 in PermissionBase._ALLOWED_OCCURRENCES_OPS:
            for k2 in PermissionBase._ALLOWED_OCCURRENCES_OPS:
                match = re.fullmatch('(\d+)({k1})m({k2})(\d+)'.format(k1=k1, k2=k2), occ_str)
                if match:
                    num1, op1, op2, num2 = int(match.group(1)), match.group(2), match.group(3), int(match.group(4))
                    within_1st_bound = PermissionBase._ALLOWED_OCCURRENCES_OPS[op1](num1, m)
                    within_2nd_bound = PermissionBase._ALLOWED_OCCURRENCES_OPS[op2](m, num2)
                    return within_1st_bound and within_2nd_bound
        else:
            raise UnexpectedValueError('Occurrence string {} not matching requirements.'.format(occ_str))

    @staticmethod
    def _check_duplicates_and_note_new_permission(obj):
        compile_obj = obj.compile_obj
        pattern = compile_obj.pattern
        existing_patterns = [i for i in CUSTOM_PERMISSIONS.keys()]
        if pattern in existing_patterns:
            raise UnexpectedValueError('Following pattern exists more than once: {}'.format(pattern))
        else:
            CUSTOM_PERMISSIONS.update({pattern: obj})

    def fullmatch(self, expr):
        return bool(re.fullmatch(self.compile_obj, expr))

    def findall(self, expr, occ_str):
        matches = re.findall(self.compile_obj, expr)
        tot_matches_found = len(matches)
        return PermissionBase.total_matches_within_bounds(m=tot_matches_found, occ_str=occ_str)



# TEMPLATE
"""
? = PermissionBase(re.compile(r'\'))
"""


# Using `re.compile` for visibility provided by IDE
integer = PermissionBase(re.compile(r'\d+'), include_sign=True)
decimal = PermissionBase(re.compile(r'\d+\.\d+'), include_sign=True)
div_excluding_fraction = PermissionBase(re.compile(r'(?:\D+/\D+)|(?:\D+/\d+)|(?:\d+/\D+)'), include_sign=True)
fraction = PermissionBase(re.compile(r'(?:\d+/\d+)|(?:\d+/\(-\d+)'))


if __name__ == '__main__':

    print_delimiter()
    print('PATTERNS AND OBJ:\n')
    for k, v in CUSTOM_PERMISSIONS.items():
        print('{}\n{}\n'.format(k, v))

    print_delimiter()
    print(integer.fullmatch('-2'))
    print(integer.fullmatch('-2.4'))
