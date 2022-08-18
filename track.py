import pandas as pd
import random
import datetime
import os

class Tracker:
    def __init__(self, data=None, save_dir="./tracker.pkl"):
        if data is not None:
            self.data = data
            self.data["Known"] = 0
            self.data["Unknown"] = 0
            self.data["Total"] = 0
            self.data["Last Seen"] = None
        if os.path.exists(save_dir):
            self.load(save_dir)
        self.counter = 0

    def save(self, save_dir):
        print(f"Saving tracker to {save_dir}")
        self.data.to_pickle(save_dir)

    def load(self, load_dir):
        print(f"Loading tracker from {load_dir}")
        loaded_data = pd.read_pickle(load_dir)
        assert type(loaded_data) == pd.DataFrame
        print(len(self.data))

        if self.data is not None:
            self.data = pd.concat([loaded_data, self.data.loc[~self.data.index.isin(loaded_data.index)]])
        else:
            self.data = loaded_data
        print(len(self.data))
        print(self.data)
        return self.data

    def __len__(self):
        return len(self.data)

    def record(self, word, known=True):
        self.data.at[word, "Total"] += 1
        if known: self.data.at[word, "Known"] += 1
        else: self.data.at[word, "Unknown"] += 1
        self.data.at[word, "Last Seen"] = datetime.datetime.now()

    def advance(self, known = None):
        self.counter += 1
        
        if known is not None:
            self.record(self.word, known)

        # Pick and return new word
        self.word = random.choice(self.data.index)
        assert self.word
        return self.word, self.data["Details"][self.word]