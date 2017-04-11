import re
import operator


from arbitrary_pieces import UnexpectedValueError, print_delimiter

CUSTOM_RESTRICTIONS = {}


class RestrictionBase(object):
    _ALLOWED_OCCURRENCES_OPS = {
        '==': operator.eq,
        '!=': operator.ne,
        '>': operator.gt,
        '>=': operator.ge,
        '<': operator.lt,
        '<=': operator.le,
    }

    def __init__(self, compile_obj, occurrence_str='>0'):
        """
        Instances of this class contain the patterns
        that are allowed or disallowed in answers.

        :param occurrence_str: How many times the pattern must occur in order to trigger the restriction.
            eg. '>=2', '<4', '==2'
        """
        if not hasattr(compile_obj, 'pattern'):
            raise UnexpectedValueError('Expecting a `re.compile` object. Most likely you did not provide one.')
        self.compile_obj = compile_obj
        self.occurrence_op, self.occurrence_num = RestrictionBase._occurrence_op_and_num(occurrence_str)
        RestrictionBase._check_duplicates_and_note_new_restriction(self)

    @staticmethod
    def _occurrence_op_and_num(occ_str):
        for k in RestrictionBase._ALLOWED_OCCURRENCES_OPS:
            match = re.fullmatch('({})(\d+)'.format(k), occ_str)
            if match:
                op, num = match.group(1), match.group(2)
                RestrictionBase._prohibit_nonsensical_occurrence_op_and_num(op=op, num=num)
                return op, num
        else:
            raise UnexpectedValueError('Occurrence string not matching requirements.')

    @staticmethod
    def _prohibit_nonsensical_occurrence_op_and_num(op, num):
        if op == '>=' and num == 0:
            raise UnexpectedValueError('>=0 would match everything.')

    @staticmethod
    def _check_duplicates_and_note_new_restriction(obj):
        compile_obj = obj.compile_obj
        pattern = compile_obj.pattern
        existing_patterns = [i for i in CUSTOM_RESTRICTIONS.keys()]
        if pattern in existing_patterns:
            raise UnexpectedValueError('Following pattern exists more than once: {}'.format(pattern))
        else:
            CUSTOM_RESTRICTIONS.update({pattern: obj})


# TEMPLATE
"""
 = RestrictionBase(re.compile(r''))
"""

# Using `re.compile` for visibility
integer = RestrictionBase(re.compile(r'^\d+$'))
decimal = RestrictionBase(re.compile(r'^\d+(?:\.\d+)?$'))
div_excluding_fraction = RestrictionBase(re.compile(r'(?:\D/\D)|(?:\D/\d)|(?:\d/\D)'))
fraction = RestrictionBase(re.compile(r'^(?:\d/\d)|(?:\d/\(-\d)$'))


if __name__ == '__main__':
    print_delimiter()
    print('PATTERNS AND OBJ:\n')
    for k, v in CUSTOM_RESTRICTIONS.items():
        print('{}\n{}\n'.format(k, v))
