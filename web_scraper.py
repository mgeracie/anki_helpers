# for scraping single character data from http://hanzidb.org/character-list/by-frequency

# %%
import os
import pandas as pd
from datetime import date
from string import Template
from collections import namedtuple
from opencc import OpenCC

# setup
timestamp = date.today().strftime("%Y%m%d")
out_path = os.path.join("input", f"single_character_{timestamp}.csv")

page_nums = range(4,10)
url_template = Template('http://hanzidb.org/character-list/by-frequency?page=${page_num}')

Columns = namedtuple("Columns", "simp_col, trad_col, pin_col, mean_col")
cols = Columns(simp_col = "Simp", trad_col = "Trad", pin_col = "Pinyin", mean_col = "Meaning")
cols_ordered = cols._asdict().values()
rename_dict = {"Unnamed: 0": cols.simp_col, "Definition": cols.mean_col, "Pinyin": cols.pin_col}

# pull data
urls = [url_template.substitute(page_num = num) for num in page_nums]
df = (pd.concat([pd.read_html(url)[0] for url in urls])
        .rename(columns = rename_dict)
        [rename_dict.values()])

# format data
df[cols.trad_col] = df[cols.simp_col].apply(OpenCC('s2t').convert)
df[cols.mean_col] = df[cols.mean_col].astype(str).apply(lambda x : x.replace(", ", "; "))
df = df[cols_ordered]

# write out
df.to_csv(out_path, index = False, header = False)


# %%
