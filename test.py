import re
from more_itertools import collapse
from utils import *

def is_single_syl(s):
    if len(re.findall("\s", s)) > 0:
        return False
    s_pin = (s in pin_all_syl)
    s_contains_pin = (sum([len(re.findall(syl, s)) for syl in pin_all_syl]) == 0)
    return s_pin or s_contains_pin

def break_simple(s: str):
    # return if already a single syllable
    if is_single_syl(s):
        return [s]
    
    # break up by whitespace if you can
    s_split = re.findall(r'\S+', s)
    if len(s_split) > 1:
        return s_split
    
    # otherwise, split up by pinyin syllables
    for syl in pin_all_syl:
        if syl in s:
            s_split = [t.strip() for t in re.split(f"({syl})", s) if t.strip() != ""]
            s_split = list(collapse(s_split))
            break
    return s_split

def break_pinyin(s):
    s_list = [s]
    is_broken = False
    while not is_broken: 
        s_list = [break_simple(s) for s in collapse(s_list)]
        s_list = list(collapse(s_list))
        is_broken = all([is_single_syl(s) for s in s_list])
    return s_list

# s_list = [["gōngyuán zhuáng qiánzhuáng"], "44 zhuáng AD"]
