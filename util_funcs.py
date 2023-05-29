import regex
from pinyin_tone_converter.pinyin_tone_converter import PinyinToneConverter
from utils import *

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

def num_to_pinyin(s: str) -> str:
    return PinyinToneConverter().convert_text(s)

def add_color_pinyin(s: str) -> str:
    s_full_split = add_color_prelim(s)
    s_colored = tag_split(s_full_split)
    return s_colored

def add_color_hanzi(s: str, c: str) -> str:
    try:
        s_full_split = add_color_prelim(s)
        c_full_split = add_color_prelim(c)
        assert(len(s_full_split) == len(c_full_split))

        c_full_split = [(c_full_split[i][0], s_full_split[i][1]) for i in range(len(s_full_split))]
        c_colored = tag_split(c_full_split)
    except:
        c_colored = c + " (color error)"
    return c_colored

def get_silhouette(c: str) -> str:
    c_out = regex.sub(HANZI_RE, " _ ", c)
    c_out = regex.sub(SPACE_RE, " ", c_out)
    c_out = c_out.strip()
    return c_out
