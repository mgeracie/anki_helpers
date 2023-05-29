import regex
from more_itertools import collapse
from utils import *

SPACE_RE = regex.compile(r"(\s+)")
HANZI_RE = regex.compile(r"([\u4e00-\u9fff])")
HANZI_PINYIN_NUM_RE = regex.compile(
        r"([\u4e00-\u9fff])|"
        r"((?:[jqx])(?:iong[1-5]?|iōng|ióng|iǒng|iòng))|"
        r"((?:[gkh]|zh|ch|sh)(?:uang[1-5]?|uāng|uáng|uǎng|uàng))|"
        r"((?:[nljqx])(?:iang[1-5]?|iāng|iáng|iǎng|iàng))|"
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
        r"(o[1-5]?|[ōóǒò])|"
        r"(\s*\d\s*)"
        , regex.I
    )

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

def add_color_prelim(s: str) -> str:
    s_clean = regex.sub(SPACE_RE, " ", s)
    s_split = [get_tone(e) for e in HANZI_PINYIN_NUM_RE.splititer(s_clean) if e and len(e) > 0]
    return s_split

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
