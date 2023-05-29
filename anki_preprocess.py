# for anki note output
import os
import pandas as pd
import regex
from datetime import date
from utils import SPACE_RE

timestamp = date.today().strftime("%Y%m%d")
in_path = os.path.join("input", "Retired__Chinese Recognition.txt")
out_path = os.path.join("input", f"Retired_Chinese_{timestamp}.csv")
df = pd.read_csv(in_path, sep = "\t",  header = None)
df = df.applymap(lambda s : regex.sub(SPACE_RE, " ", str(s)).strip())
df = df.applymap(lambda s : regex.sub("<br />", " ", str(s)).strip())
df = df[[0,2]]
df.columns = ["Hanzi", "Meaning"]
df.to_csv(out_path, index = None)