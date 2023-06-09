# for pleco export
import os
import pandas as pd
from datetime import date
from pinyin_tone_converter.pinyin_tone_converter import PinyinToneConverter
from utils import *

delim = "|"
timestamp = date.today().strftime("%Y%m%d")
in_path = os.path.join("input", "pleco_export_20230529.txt")
out_path = os.path.join("input", f"pleco_{timestamp}.csv")
df = pd.read_csv(in_path, sep = "\t",  header = None)
df.columns = ["Hanzi", "Pinyin", "Meaning"]
ptc = PinyinToneConverter()
df["Pinyin"] = df["Pinyin"].apply(replace_special_char).apply(ptc.convert_text)

df[["Simp", "Trad"]] = df["Hanzi"].str.replace("]", "").str.split("[", expand = True)

df = df[["Simp", "Trad", "Pinyin", "Meaning"]]
df.to_csv(out_path, index = None)
