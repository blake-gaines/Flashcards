import pandas as pd
import re

def get_data():
    with open("Chinese Words.txt", "r", encoding="utf-8-sig") as f:
        words = pd.Series([line for line in f.readlines() if line.strip()]).str.strip()
        words = words.drop_duplicates()

    parser = re.compile(r"([\u4e00-\u9fff,， \"“”！。]+)[<《]?-?([\S ]*)")

    def format_row(row: str):
        # if len(row) < 3: return
        split = row.split()
        # re.findall(zh_regex)
        line = re.match(parser, row)
        if line:
            combined_words, notes = line.groups()
        else:
            # print(f"Could not parse: {row}")
            return None
        words = re.findall(r"[\u4e00-\u9fff]+", combined_words)
        return combined_words.strip(), notes.strip()

    m = words.map(format_row).dropna(how='all').reset_index(drop=True).fillna("")
    words_df = pd.DataFrame.from_records(m,columns=["Hanzi", "Details"]).drop_duplicates(subset="Hanzi", keep="first")
    print("Number of words:", len(words_df))
    return words_df