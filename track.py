import pandas as pd
import random
import datetime
import os

class Tracker:
    def __init__(self, data, save_dir="./tracker.pkl"):
        if type(data) == pd.DataFrame and not os.path.exists(save_dir):
            self.data = data
            self.data["Known"] = 0
            self.data["Unknown"] = 0
            self.data["Total"] = 0
            self.data["Last Seen"] = None
        else:
            self.load(save_dir)
        self.save_dir = save_dir
        self.counter = 0

    def save(self, save_dir=None):
        if not save_dir:
            save_dir = self.save_dir
        print(f"Saving tracker to {save_dir}")
        self.data.to_pickle(save_dir)

    def load(self, save_dir=None):
        if not save_dir:
            save_dir = self.save_dir
        print(f"Loading tracker from {save_dir}")
        self.data = pd.read_pickle(save_dir)

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

        if self.counter % 10 == 0:
            self.save(self.save_dir)

        # Pick and return new word
        self.word = random.choice(self.data.index)
        assert self.word
        return self.word, self.data["Details"][self.word]