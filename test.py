# rebase needed

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
    if len(re.findall(r"\s", s)) > 0:
        return False
    if len(re.findall(r"[\u4e00-\u9fff]", s)) > 1:
        return False
    if len(re.findall(r"[\u4e00-\u9fff]", s)) == 1 and len(s) > 1:
        return False
    s_pin = (s in pin_all_syl)
    s_contains_pin = (sum([len(re.findall(syl, s)) for syl in pin_all_syl]) == 0)
    return s_pin or s_contains_pin

def break_simple(s, is_char = False):
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
    
    # break up by char
    if is_char:
        s_split = [t.strip() for t in re.split(r"([\u4e00-\u9fff])", s)  if t.strip() != ""]
        s_split = list(collapse(s_split))
    # break up by pinyin
    else:
        for syl in pin_all_syl:
            if syl in s:
                s_split = [t.strip() for t in re.split(f"({syl})", s) if t.strip() != ""]
                s_split = list(collapse(s_split))
                break

    return s_split

def break_string_full(s, is_char = False):
    s_list = [s]
    is_broken = False
    while not is_broken: 
        s_list = [break_simple(s, is_char) for s in collapse(s_list)]
        while (len(s_list) == 1) and (type(s_list[0]) == list):
            s_list = s_list[0]
        s_list = list(collapse(s_list))
        is_broken = all([is_single_syl(s) for s in s_list])
    s_list = [get_tone(s) for s in s_list]
    return s_list

def break_char_string_full(s_char, s_pin):
    s_pin_list = break_string_full(s_pin)
    s_char_list = break_string_full(s_char, True)
    s_char_list = [(s_char_list[i][0], s_pin_list[i][1]) for i in range(len(s_char_list))]
    return s_char_list

def break_string(s, s_char = ""):
    if s_char != "":
        s_broken = break_char_string_full(s_char, s)
    else:
        s_broken = break_string_full(s)
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

def stylize_pinyin(s):
    span_1 = "<span class = 'tone1'>"
    span_2 = "<span class = 'tone2'>"
    span_3 = "<span class = 'tone3'>"
    span_4 = "<span class = 'tone4'>"
    span_5 = "<span class = 'tone5'>"
    end_span = "</span>"
    s_list = break_string(s)
    
    s_out = "".join([span_1 + s[0] + end_span if s[1] == 1
                        else span_2 + s[0] + end_span if s[1] == 2
                        else span_3 + s[0] + end_span if s[1] == 3
                        else span_4 + s[0] + end_span if s[1] == 4
                        else span_5 + s[0] + end_span
                        for s in s_list])
    
    return s_out

s1 = "hello there gōngyuán,  44 běi zhuáng - qiánzhuáng3"
s2 = "hello there gōngyuán,  44 běi zhuáng - qiánzhuáng"

c = "公园"
d = "园3"

c1 = "hello there 公园, 44 北 妆 - 前妆3"
c2 = "hello there 公园, 44 北 妆 - 前妆"