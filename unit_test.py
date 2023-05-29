import unittest
from util_funcs import *

class TestAnkiUtils(unittest.TestCase):

    def setUp(self):
        self.s1 = "hello， 园there？。。\n。"
        self.s2 = "gōng yuán, 78 \n公圆" 
        self.s3 = "gōngyuánqián 78 nián" 
        self.c3 = "公元前78年" 

    def add_color(self):
        self.assertEqual(add_color(self.s1),"hi")

if __name__ == "__main__":
    unittest.main()