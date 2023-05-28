import regex
from more_itertools import collapse
from utils import *

SPACE_RE = regex.compile(r"(\s+)")
PUNCT_RE = regex.compile(r"(\p{Punctuation})")
HANZI_RE = regex.compile(r"([\u4e00-\u9fff])")

PINYIN_RE = regex.compile(
        r"((?:[jqx])(?:iong[1-5]?|iōng|ióng|iǒng|iòng))|"
        r"((?:[gkh]|zh|ch|sh)(?:uang[1-5]?|uāng|uáng|uǎng|uàng))|"
        r"((?:[nljqx])(?:iang[1-5]?|iāng|iáng|iǎng|iàng))|" # most recent
        r"((?:[mdx])(?:ianr[1-5]?|iānr|iánr|iǎnr|iànr))|"
        r"((?:[bgw])(?:anr[1-5]?|ānr|ánr|ǎnr|ànr))|"
        r"((?:[bpmfdtnlgkhzcsry]|zh|ch|sh)(?:ang[1-5]?|āng|áng|ǎng|àng))|"
        r"((?:[bpmdtnljqx])(?:iao[1-5]?|iāo|iáo|iǎo|iào))|"
        r"((?:[bpmdtnljqx])(?:ian[1-5]?|iān|ián|iǎn|iàn))|"
        r"((?:[bpmdtnljqxy])(?:ing[1-5]?|īng|íng|ǐng|ìng))|"
        r"((?:[bpmfdtnlgkhzcsrw]|zh|ch|sh)(?:eng[1-5]?|ēng|éng|ěng|èng))|"
        r"((?:[dtnlgkhzcsry]|zh|ch)(?:ong[1-5]?|ōng|óng|ǒng|òng))|"
        r"((?:[gkh]|zh|ch|sh)(?:uai[1-5]?|uāi|uái|uǎi|uài))|"
        r"((?:[dtnlgkhzcsrjqxy]|zh|ch|sh)(?:uan[1-5]?|uān|uán|uǎn|uàn))|"
        r"((?:[bpmdtnlgkhzcsry]|zh|ch|sh)(?:ao[1-5]?|āo|áo|ǎo|ào))|"
        r"((?:[bpmdtnlgkhzcsw]|zh|ch|sh)(?:ai[1-5]?|āi|ái|ǎi|ài))|"
        r"((?:[bpmfdtnlgkhzcsry]|zh|ch|sh)(?:an[1-5]?|ān|án|ǎn|àn))|"
        r"((?:[bpmfdngkhzcsrw]|zh|ch|sh)(?:en[1-5]?|ēn|én|ěn|èn))|"
        r"((?:[bpmfdtnlgkhzsw]|zh|sh)(?:ei[1-5]?|ēi|éi|ěi|èi))|"
        r"((?:[dljqx])(?:ia[1-5]?|iā|iá|iǎ|ià))|"
        r"((?:[bpmdtnljqx])(?:ie[1-5]?|iē|ié|iě|iè))|"
        r"((?:[mdnljqx])(?:iu[1-5]?|iū|iú|iǔ|iù))|"
        r"((?:[bpmnljqxy])(?:in[1-5]?|īn|ín|ǐn|ìn))|"
        r"((?:[p]|sh)(?:ir[1-5]?|īr|ír|ǐr|ìr))|"
        r"((?:[pmfdtnlgkhzcsry]|zh|ch|sh)(?:ou[1-5]?|ōu|óu|ǒu|òu))|"
        r"((?:[gkhr]|zh|ch|sh)(?:ua[1-5]?|uā|uá|uǎ|uà))|"
        r"((?:[dtnlgkhzcsr]|zh|ch|sh)(?:uo[1-5]?|uō|uó|uǒ|uò))|"
        r"((?:[dtgkhzcsr]|zh|ch|sh)(?:ui[1-5]?|uī|uí|uǐ|uì))|"
        r"((?:[jqxy])(?:ue[1-5]?|uē|ué|uě|uè))|"
        r"((?:[dtnlgkhzcsrjqxy]|zh|ch|sh)(?:un[1-5]?|ūn|ún|ǔn|ùn))|"
        r"((?:[nl])(?:üe[1-5]?|ve[1-5]?|ǖe|ǘe|ǚe|ǜe))|"
        r"((?:[bpmfdtnlgkhzcswy]|zh|ch|sh)(?:a[1-5]?|[āáǎà]))|"
        r"((?:[mdtnlgkhzcsry]|zh|ch|sh)(?:e[1-5]?|[ēéěè]))|"
        r"((?:[bpmdtnlzcsrjqyx]|zh|ch|sh)(?:i[1-5]?|[īíǐì]))|"
        r"((?:[bpmow])(?:o[1-5]?|[ōóǒò]))|"
        r"((?:[bpmfdtnlgkhzcsrjqxwy]|zh|ch|sh)(?:u[1-5]?|[ūúǔù]))|"
        r"((?:[nl])(?:ü[1-5]?|v[1-5]?|[ǖǘǚǜ]))|"
        r"(wang[1-5]?|āng|áng|ǎng|àng)|"
        r"(eng[1-5]?|ēng|éng|ěng|èng)|"
        r"(ai[1-5]?|āi|ái|ǎi|ài)|"
        r"(wan[1-5]?|ān|án|ǎn|àn)|"
        r"(ao[1-5]?|āo|áo|ǎo|ào)|"
        r"(ei[1-5]?|ēi|éi|ěi|èi)|"
        r"(er[1-5]?|ēr|ér|ěr|èr)|"
        r"((en[1-5]?|ēn|én|ěn|èn))|"
        r"(ou[1-5]?|ōu|óu|ǒu|òu)|"
        r"(a[1-5]?|[āáǎà])|"
        r"(e[1-5]?|[ēéěè])|"
        r"(o[1-5]?|[ōóǒò])"
        , regex.I
    )
tmp = PINYIN_RE.split("btbasha5ssaā2chāmoa shàiei shenme shéihei chuang1")
# tmp = PINYIN_RE.split("chan nvshén")
[elt for elt in tmp if elt and len(elt) > 0]

# s = "hello， 园there？。。\n。"
# PUNCT_RE.split(s)

def has_hanzi(s: str) -> bool:
    """Check if string contains hanzi."""
    return len(regex.findall(HANZI_RE, s)) > 0

def is_single_syl(s: str) -> bool:
    """Check if a string is a single syllable.
    This is used when breaking up strings with pinyin or hanzi into colored components.
    For this purpose a 'syllable'
        - has no whitespace or is a single space
        - is a single valid pinyin syllable with no extra characters 
        - is a single simplified or traditional chinese character
    Otherwise it is not a syllable."""
    if s == " ":
        return True
    if len(regex.findall(r"\s", s)) > 0:
        return False
    if len(regex.findall(HANZI_RE, s)) > 1:
        return False
    if len(regex.findall(HANZI_RE, s)) == 1 and len(s) > 1:
        return False
    s_is_pinyin_syl = s in pin_all_syl
    s_no_pinyin = sum([len(regex.findall(syl, s)) for syl in pin_all_syl]) == 0
    return s_is_pinyin_syl or s_no_pinyin

def get_tone(syl: str) -> tuple:
    if syl in pin_all_syl:
        if len(regex.findall(r"(ā|ē|ī|ō|ū|ǖ)", syl)) == 1:
            return (syl, 1)
        if len(regex.findall(r"(á|é|í|ó|ú|ǘ)", syl)) == 1:
            return (syl, 2)
        if len(regex.findall(r"(ǎ|ě|ǐ|ǒ|ǔ|ǚ)", syl)) == 1:
            return (syl, 3)
        if len(regex.findall(r"(à|è|ì|ò|ù|ǜ)", syl)) == 1:
            return (syl, 4)
    else:
        return (syl, 5)

def break_simple(s: str) -> list:
    """Performs a single step in the process of breaking up a string into its syllables."""
    # initial whitespace simplification
    s = regex.sub(SPACE_RE, " ", s).strip()
    # return if already a single syllable
    if is_single_syl(s):
        return [s]
    # break by whitespace if you can
    s_split = SPACE_RE.split(s)
    if len(s_split) > 1:
        return s_split 
    # break by punctuation if you can
    s_split = PUNCT_RE.split(s)
    if len(s_split) > 1:
        return s_split 
    # break up by character
    s_split = HANZI_RE.split(s)
    if len(s_split) > 1:
        return s_split 
    # break up by pinyin
    for syl in pin_all_syl:
        SYL_RE = regex.compile(syl)
        # if syl in s:
            # s_split = [t.strip() for t in re.split(f"({syl})", s) if t.strip() != ""]
            # s_split = list(collapse(s_split))
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
    s_out = re.sub(HANZI_RE, "_ ", s_char)
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
