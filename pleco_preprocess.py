# for pleco export
import os
import pandas as pd
from datetime import date
from pinyin_tone_converter.pinyin_tone_converter import PinyinToneConverter
from utils import *

timestamp = date.today().strftime("%Y%m%d")
in_path = os.path.join("input", "pleco_export_20230529.txt")
out_path = os.path.join("input", f"pleco_{timestamp}.csv")
df = pd.read_csv(in_path, sep = "\t",  header = None)
df.columns = ["Hanzi", "Pinyin", "Meaning"]
ptc = PinyinToneConverter()
tmp = (
    df["Pinyin"]
    .apply(ptc.convert_text)
    .apply(PINYIN_RE.split)
    # .apply(full_split)
)

df[["Simp", "Trad"]] = df["Hanzi"].str.replace("]", "").str.split("[", expand = True)

df = df[["Simp", "Trad", "Pinyin", "Meaning"]]
df.to_csv(out_path, index = None)