import pandas as pd
import random
import datetime

class Tracker:
    def __init__(self, data, save_dir="./tracker.pkl"):
        if type(data) == pd.DataFrame:
            self.data = data
            self.data["Known"] = 0
            self.data["Unknown"] = 0
            self.data["Total"] = 0
            self.data["Last Seen"] = None
        else:
            self.data = pd.read_pickle(data)

        self.counter = 0

    def save(self):
        self.data.to_pickle(self.save_dir)

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
            print("Saving")
            self.save(self.save_dir)

        # Pick and return new word
        self.word = random.choice(self.data.index)
        return self.word, self.data["Details"][self.word]