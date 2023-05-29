import unittest
from util_funcs import *

class TestAnkiUtils(unittest.TestCase):

    def setUp(self):
        self.s1 = "hello there gōngyuán,  44 běi zhuáng - qiánzhuáng3"
        self.c1 = "hello there 公园, 44 北 妆 - 前妆3"
        self.s2 = "gōngyuánqián 78 nián" 
        self.c2 = "公元前78年" 
        self.s3 = "hello， 园there？。。\n。"
        self.s4 = "gōng yuán, 78 \n公圆" 

    def test_add_color(self):
        self.assertEqual(add_color_pinyin(self.s1), "<span class = 'tone5'>hello there </span><span class = 'tone1'>gōng</span><span class = 'tone2'>yuán</span><span class = 'tone5'>,</span><span class = 'tone4'> 44 </span><span class = 'tone3'>běi </span><span class = 'tone2'>zhuáng</span><span class = 'tone5'> - </span><span class = 'tone2'>qiánzhuáng</span><span class = 'tone1'>3</span>")
        self.assertEqual(add_color_pinyin(self.s2), "<span class = 'tone1'>gōng</span><span class = 'tone2'>yuánqián</span><span class = 'tone1'> 78 </span><span class = 'tone2'>nián</span>")
        self.assertEqual(add_color_pinyin(self.s3), "<span class = 'tone5'>hello， 园there？。。 。</span>")
        self.assertEqual(add_color_pinyin(self.s4), "<span class = 'tone1'>gōng </span><span class = 'tone2'>yuán</span><span class = 'tone5'>,</span><span class = 'tone1'> 78 </span><span class = 'tone5'>公圆</span>")
        self.assertEqual(add_color_hanzi(self.s1, self.c1), "<span class = 'tone5'>hello there </span><span class = 'tone1'>公</span><span class = 'tone2'>园</span><span class = 'tone5'>,</span><span class = 'tone4'> 44 </span><span class = 'tone3'>北 </span><span class = 'tone2'>妆</span><span class = 'tone5'> - </span><span class = 'tone2'>前妆</span><span class = 'tone1'>3</span>")
        self.assertEqual(add_color_hanzi(self.s2, self.c2), "<span class = 'tone1'>公</span><span class = 'tone2'>元前</span><span class = 'tone1'>78</span><span class = 'tone2'>年</span>")

if __name__ == "__main__":
    unittest.main()