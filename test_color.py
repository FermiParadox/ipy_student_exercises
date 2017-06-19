from unittest import TestCase

from colors import Color


class TestColor(TestCase):
    def test_0_representations_disallowed(self):
        self.assertRaises(ValueError, Color)

    def test_one_representation_doesnt_raise(self):
        self.assertTrue(Color(rgb=(1,1,1)))

    def test_rgb_other_than_3_elements_disallowed(self):
        self.assertRaises(ValueError, Color, None, [1,1])
        self.assertRaises(ValueError, Color, None, [1,1,1,1])

    def test_rgb_list_and_tuple_doesnt_raise(self):
        t = (1,1,1)
        self.assertTrue(Color(rgb=t))
        self.assertTrue(Color(rgb=list(t)))