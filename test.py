import re
from more_itertools import collapse
from utils import *
from functools import reduce

def get_tone(syl):
    if syl in pin_all_syl:
        if len(re.findall(r"(ā|ē|ī|ō|ū|ǖ)", syl)) == 1:
            return (syl, 1)
        if len(re.findall(r"(á|é|í|ó|ú|ǘ)", syl)) == 1:
            return (syl, 2)
        if len(re.findall(r"(ǎ|ě|ǐ|ǒ|ǔ|ǚ)", syl)) == 1:
            return (syl, 3)
        if len(re.findall(r"(à|è|ì|ò|ù|ǜ)", syl)) == 1:
            return (syl, 4)
    else:
        return (syl, 5)

def is_single_syl(s):
    if s == " ":
        return True
    if len(re.findall("\s", s)) > 0:
        return False
    s_pin = (s in pin_all_syl)
    s_contains_pin = (sum([len(re.findall(syl, s)) for syl in pin_all_syl]) == 0)
    return s_pin or s_contains_pin

def break_simple(s: str):
    s_split = ""
    # return if already a single syllable
    if (is_single_syl(s) or s == " "):
        return [s]
    
    # break up by whitespace if you can
    if s != " ":
        s_split = re.findall(r'\S+', s)
        s_split = [s_split[int(i/2)] if (i % 2) == 0 else " "  for i in range(2 * len(s_split) - 1)]
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
    s_broken = [get_tone(s) for s in s_list]

    output = []
    in_process_syl = ("", 5)
    for i in range(0, len(s_broken)):
        syl = s_broken[i]
        if in_process_syl[0] == "":
            in_process_syl = syl
        elif in_process_syl[1] == syl[1]:
            in_process_syl = (in_process_syl[0] + syl[0], syl[1])
        else:
            output.append(in_process_syl)
            in_process_syl = syl
        if i == len(s_broken) - 1:
            output.append(in_process_syl)

    return output

s1 = "hello there gōngyuán,  44 běi zhuáng - qiánzhuáng3"
s2 = "hello there gōngyuán,  44 běi zhuáng - qiánzhuáng"
