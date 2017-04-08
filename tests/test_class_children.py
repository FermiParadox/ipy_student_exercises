from unittest import TestCase

from arbitrary_pieces import class_children


class Test_class_children(TestCase):

    def test_class_children(self):
        class A(object): pass
        class B1(A): pass
        class B2(A): pass
        class C(B1): pass
        class MultInhC(B1, B2): pass
        self.assertSetEqual({B1, B2, C, MultInhC}, class_children(A))

    def test_parent_is_not_child(self):
        class A(object): pass
        class B1(A): pass
        self.assertNotIn(A, class_children(A))
