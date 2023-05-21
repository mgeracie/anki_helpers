from util_funcs import *

assert(is_single_syl("a"))
assert(is_single_syl("ads;kflj"))
assert(is_single_syl("yuán"))
assert(is_single_syl("公"))
assert(is_single_syl("52"))
assert(is_single_syl(" "))
assert(not is_single_syl("ads; kflj"))
assert(not is_single_syl("园3"))
assert(not is_single_syl("3园"))
assert(not is_single_syl("公园"))
assert(not is_single_syl("公7园"))
assert(not is_single_syl("公 园"))
assert(not is_single_syl("red 园"))
assert(not is_single_syl("gōngyuán"))
assert(not is_single_syl("gyuán"))
assert(not is_single_syl("yuá"))
assert(not is_single_syl("\t"))
assert(not is_single_syl("\n"))
assert(not is_single_syl("    "))

assert(get_tone("a")[1] == 5)
assert(get_tone("aasdf")[1] == 5)
assert(get_tone(" ")[1] == 5)
assert(get_tone("78")[1] == 5)
assert(get_tone("nüē")[1] == 1)
assert(get_tone("zhuáng")[1] == 2)
assert(get_tone("nǚ")[1] == 3)
assert(get_tone("yuàn")[1] == 4)

assert(break_simple("a") == ["a"])
assert(break_simple("aasdf") == ["aasdf"])
assert(break_simple(" ") == [" "])
assert(break_simple("a fd") == ["a", " ", "fd"])
assert(break_simple("a\nf d") == ["a", " ", "f", " ", "d"])
assert(break_simple("a\n fd") == ["a", " ", "fd"])
assert(break_simple("a\n fd") == ["a", " ", "fd"])
assert(break_simple("a\n fd") == ["a", " ", "fd"])
assert(break_simple("gōngyuán") == ["gōng", "yuán"])
assert(break_simple("3gōngready") == ["3", "gōng", "ready"])


s1 = "hello there gōngyuán,  44 běi zhuáng - qiánzhuáng3"
s2 = "hello there gōngyuán,  44 běi zhuáng - qiánzhuáng"

c = "公园"
d = "园3"

c1 = "hello there 公园, 44 北 妆 - 前妆3"
c2 = "hello there 公园, 44 北 妆 - 前妆"


print("NO ERRORS!")