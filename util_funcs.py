import re
from more_itertools import collapse
from utils import *

def is_char_str(s: str) -> bool:
    return len(re.findall(r"[\u4e00-\u9fff]", s)) > 0

def is_single_syl(s: str) -> bool:
    if s == " ":
        return True
    if len(re.findall(r"\s", s)) > 0:
        return False
    if len(re.findall(r"[\u4e00-\u9fff]", s)) > 1:
        return False
    if len(re.findall(r"[\u4e00-\u9fff]", s)) == 1 and len(s) > 1:
        return False
    s_is_pinyin_syl = s in pin_all_syl
    s_no_pinyin = sum([len(re.findall(syl, s)) for syl in pin_all_syl]) == 0
    return s_is_pinyin_syl or s_no_pinyin

def get_tone(syl: str) -> tuple:
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

def break_simple(s: str) -> list:
    """Performs a single step in the process of breaking up a string into its syllables."""
    is_char = is_char_str(s)
    # return if already a single syllable
    if is_single_syl(s):
        return [s]
    # break up by whitespace if you can
    s_split = re.findall(r'\S+', s)
    s_split = [s_split[int(i/2)] if (i % 2) == 0 else " "  for i in range(2 * len(s_split) - 1)]
    if len(s_split) > 1:
        return s_split 
    # break up by char
    elif is_char:
        s_split = [t.strip() for t in re.split(r"([\u4e00-\u9fff])", s) if t.strip() != ""]
        s_split = list(collapse(s_split))
    # break up by pinyin
    else:
        for syl in pin_all_syl:
            if syl in s:
                s_split = [t.strip() for t in re.split(f"({syl})", s) if t.strip() != ""]
                s_split = list(collapse(s_split))
                break
    return s_split

def fully_break_string_prelim(s: str) -> list:
    s_list = [s]
    is_broken = False
    while not is_broken: 
        s_list = [break_simple(s) for s in collapse(s_list)]
        while (len(s_list) == 1) and (type(s_list[0]) == list): s_list = s_list[0]
        s_list = list(collapse(s_list))
        is_broken = all([is_single_syl(s) for s in s_list])
    s_list = [get_tone(s) for s in s_list]
    return s_list

def fully_break_string(s_pin: str, s_char: str = "") -> list:
    """Break a string fully down to it's individual syllables with tone assignments.
    This way can match characters to the tones of pinyin syllables. They will be combined in break_string."""
    s_out = fully_break_string_prelim(s_pin)
    if s_char != "":
        s_char_list = fully_break_string_prelim(s_char)
        s_out = [(s_char_list[i][0], s_out[i][1]) for i in range(len(s_char_list))]
    return s_out

def break_string(s_pin: str, s_char: str = "") -> list:
    s_broken = fully_break_string(s_pin, s_char)
    output = []
    in_process_syl = ("", 5)
    for i in range(0, len(s_broken)):
        syl = s_broken[i]
        if in_process_syl[0] == "":
            in_process_syl = syl
        elif (in_process_syl[1] == syl[1]) or (syl[0] == " "):
            in_process_syl = (in_process_syl[0] + syl[0], in_process_syl[1])
        else:
            output.append(in_process_syl)
            in_process_syl = syl
        if i == len(s_broken) - 1:
            output.append(in_process_syl)

    return output

def stylize_str(s_pin: str, s_char: str = "") -> str:
    span_1 = "<span class = 'tone1'>"
    span_2 = "<span class = 'tone2'>"
    span_3 = "<span class = 'tone3'>"
    span_4 = "<span class = 'tone4'>"
    span_5 = "<span class = 'tone5'>"
    end_span = "</span>"
    s_list = break_string(s_pin, s_char)
    s_out = "".join([span_1 + s[0] + end_span if s[1] == 1
                        else span_2 + s[0] + end_span if s[1] == 2
                        else span_3 + s[0] + end_span if s[1] == 3
                        else span_4 + s[0] + end_span if s[1] == 4
                        else span_5 + s[0] + end_span
                        for s in s_list])
    return s_out

def safe_stylize_hanzi(s_pin: str, s_char: str = "") -> str:
    try:
        out = stylize_str(s_pin, s_char)
    except:
        out = s_char + " (color error)"
    return out

def get_silhouette(s_char: str) -> str:
    s_out = re.sub(r"[\u4e00-\u9fff]", "_ ", s_char)
    s_out = re.sub(r"\s+", " ", s_out)
    s_out = re.sub(r"_ $", "_", s_out)
    return s_out

def strip_html(x: str):
    CLEANR = re.compile(r'<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});')

    while True:
        input = x
        x = x.strip()
        x = re.sub(r"(^<div>|</div>$)", r"", x)
        x = re.sub(r"(<div>|</div>|<br>)", r"\n", x)
        x = re.sub(r"\n\s*\n", r"\n", x)
        x = re.sub(CLEANR, r"", x)
        if x == input:
            break

    while True:
        input = x
        x = re.sub(r"\n", r"<br>", x)
        if x == input:
            break

    return(x)
