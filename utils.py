import os
import re
import regex
import zhon
from pinyin_tone_converter.pinyin_tone_converter import PinyinToneConverter
from utils import *
from gtts import gTTS

SPACE_RE = regex.compile(r"(\s+)")
HANZI_RE = regex.compile(r"([\u4e00-\u9fff])")
PINYIN_RE = regex.compile(zhon.pinyin.syllable, regex.I)

span_1 = "<span class = 'tone1'>"
span_2 = "<span class = 'tone2'>"
span_3 = "<span class = 'tone3'>"
span_4 = "<span class = 'tone4'>"
span_5 = "<span class = 'tone5'>"
end_span = "</span>"

def get_tone(syl: str) -> tuple:
    if len(regex.findall(r"(ā|ē|ī|ō|ū|ǖ)", syl)) == 1:
        return (syl, 1)
    elif len(regex.findall(r"(á|é|í|ó|ú|ǘ)", syl)) == 1:
        return (syl, 2)
    elif len(regex.findall(r"(ǎ|ě|ǐ|ǒ|ǔ|ǚ)", syl)) == 1:
        return (syl, 3)
    elif len(regex.findall(r"(à|è|ì|ò|ù|ǜ)", syl)) == 1:
        return (syl, 4)
    syl_stripped = syl.strip()
    if syl_stripped in ["1", "3", "7", "8"]:
        return (syl, 1)
    elif syl_stripped in ["0"]:
        return (syl, 2)
    elif syl_stripped in ["5", "9"]:
        return (syl, 3)
    elif syl_stripped in ["2", "4", "6"]:
        return (syl, 4)
    else:
        return (syl, 5)

def replace_special_char(s: str) -> str:
    s_out = (s.replace("v", "ü")
              .replace("。", ".")
              .replace("，", ",")
              .replace("？", "?")
              .replace("《", "\"")
              .replace("》", "\"")
              .replace("（", "(")
              .replace("）", ")")
              .replace("；", ";")
              .replace("：", ":")
              .replace("‘", "'")
              .replace("“", "\"")
              .replace("、", "\\")
              .replace("【", "[")
              .replace("】", "]")
              .replace("——", "_")
              .replace("……", "^")
              .replace("！", "!")
              .replace("·", "`"))
    return s_out

def full_split(s: str, delim: str = "|") -> list:
    """Takes a delimited string and breaks it into syllable pairs."""
    return [get_tone(syl) for syl in s.split(delim)]

def simplify_split(s_split: list) -> list:
    s_split_simp = []
    for i in range(0, len(s_split)):
        syl = s_split[i]
        if  i == 0:
            in_process_syl = syl
        elif (in_process_syl[1] == syl[1]) or (syl[0] == " "):
            in_process_syl = (in_process_syl[0] + syl[0], in_process_syl[1])
        else:
            s_split_simp.append(in_process_syl)
            in_process_syl = syl
        if i == len(s_split) - 1:
            s_split_simp.append(in_process_syl)
    return s_split_simp

def tag_split(s_split: list) -> str:
    s_split = simplify_split(s_split)
    return "".join([span_1 + s[0] + end_span if s[1] == 1
                        else span_2 + s[0] + end_span if s[1] == 2
                        else span_3 + s[0] + end_span if s[1] == 3
                        else span_4 + s[0] + end_span if s[1] == 4
                        else span_5 + s[0] + end_span
                        for s in s_split])

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

def add_color_hanzi(s_split: str, c_split: str) -> str:
    try:
        assert(len(s_split) == len(c_split))
        c_split = [(c_split[i][0], s_split[i][1]) for i in range(len(s_split))]
        c_colored = tag_split(c_split)
    except:
        c_colored = "(color error)"
    return c_colored

def get_silhouette(c: str) -> str:
    c_out = regex.sub(HANZI_RE, " _ ", c)
    c_out = regex.sub(SPACE_RE, " ", c_out)
    c_out = c_out.strip()
    return c_out

def save_audio(s: str, dir: str, save: bool = True) -> str:
    out_path = os.path.join(dir, f"{s}.mp3")
    if save and not os.path.isfile(out_path):
        try:
            gTTS(s, lang = "zh-CN").save(out_path)
        except:
            return "FAILED WRITING: " + s
    return f"[sound:{s}.mp3]"
