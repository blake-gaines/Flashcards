import pandas as pd
import random
import datetime
import os

class Tracker:
    def __init__(self, data, save_dir, load_dir=None):
        self.data = data
        self.data["Known Count"] = 0
        self.data["Unknown Count"] = 0
        self.data["Total"] = 0
        self.data["Last Seen"] = None
        self.data["Last Status"] = None
        if load_dir is not None and os.path.exists(load_dir):
            self.load(load_dir)
        self.save_dir = save_dir
        self.counter = 0
        self.pickers = [self.random_word]
        self.picker_weights = [1]

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

    def record(self, index, known=None):
        self.data.at[index, "Total"] += 1
        if known is None:
            self.data.at[index, "Last Status"] = "Skipped"
        if known == True: 
            self.data.at[index, "Known Count"] += 1
            self.data.at[index, "Last Status"] = "Known"
        elif known == False: 
            self.data.at[index, "Unknown Count"] += 1
            self.data.at[index, "Last Status"] = "Unknown"
        self.data.at[index, "Last Seen"] = datetime.datetime.now()

    def random_word(self):
        return self.data.sample()

    def advance(self, index=None, known = None):
        self.counter += 1
        
        if index is not None: self.record(index, known)
            
        # Pick and return new word

        picker ,= random.choices(self.pickers, weights=self.picker_weights)
        row = picker()

        return row.index.item(), row.squeeze()

        # assert self.word
        # return self.word, self.data["Details"][self.word]