import unittest
from util_funcs import *

class TestAnkiUtils(unittest.TestCase):

    def setUp(self):
        self.character_tests = []

    def test_has_hanzi(self):
        self.assertFalse(has_hanzi("\n ads;k flj"))
        self.assertFalse(has_hanzi("yuán"))

        self.assertTrue(has_hanzi("a98'ff \t -=+公 rH")) # simplified
        self.assertTrue(has_hanzi("f視98lnasf'")) # traditional

    def test_is_single_syl(self):
        self.assertFalse(is_single_syl("\n"))
        self.assertFalse(is_single_syl("a "))
        self.assertFalse(is_single_syl("\ta"))
        self.assertFalse(is_single_syl("yuán "))
        self.assertFalse(is_single_syl("gongyuán"))
        self.assertFalse(is_single_syl("gōng yuán"))
        self.assertFalse(is_single_syl("gōngyuán"))
        self.assertFalse(is_single_syl("公园"))
        self.assertFalse(is_single_syl("視？"))
        self.assertFalse(is_single_syl("殺，"))

        self.assertTrue(is_single_syl(" "))
        self.assertTrue(is_single_syl("a"))
        self.assertTrue(is_single_syl("78"))
        self.assertTrue(is_single_syl("yuán"))
        self.assertTrue(is_single_syl("公"))
        self.assertTrue(is_single_syl("視"))
        self.assertTrue(is_single_syl("？"))
        self.assertTrue(is_single_syl(".f"))
        self.assertTrue(is_single_syl("。。。"))

if __name__ == "__main__":
    unittest.main()