import PySimpleGUI as sg
from get import Word
from read import get_data
import webbrowser
from track import Tracker
import random
import sys

class Application:
    style_args = {
        "font": ("Helvetica", 24)
    }
    def __init__(self):
        self.tracker=Tracker(get_data(), save_dir="./tracker.pkl", load_dir="./tracker.pkl")
        # print(self.tracker.data.loc[self.tracker.data[["Known", "Unknown"]].any(axis=1)])
        # sys.exit(0)

        sg.theme('Default1')
        layout = [  
            [sg.Text(size=(40,1), key='front', auto_size_text=True, **self.style_args)],
            [sg.Button('Show', 	expand_x=True, **self.style_args), sg.Button('Page', **self.style_args)],
            [sg.Text(size=(100,30), key='back', expand_x=True, font="Helveteca12")],
            [sg.Button('Known', 	expand_x=True, **self.style_args), sg.Button('Unknown', 	expand_x=True, **self.style_args)] 
        ]
        self.window = sg.Window('Window Title', layout, finalize=True, return_keyboard_events=True) # , no_titlebar=True
        self.index = None
        self.update_word(known=None)

    def update_word(self, known=None):
        self.index, self.row = self.tracker.advance(index=self.index, known=known)
        print("HANZI", self.row["Hanzi"])
        self.word = Word(self.row["Hanzi"])
        self.front_choice = "English" if (random.random() < 0.5) else "Chinese"
        self.full_description = ""
        if self.word.yb_exists:
            if self.front_choice == "Chinese":
                self.full_description = "Pinyin: {}\nDefinition: {}".format(self.word.pinyin, self.word.definitions)
            elif self.front_choice == "English":
                self.full_description = f"{self.word.hanzi} ({self.word.pinyin})"
            if self.word.pos:
                self.full_description += "\nPart of Speech: {}".format(self.word.pos)
            if self.word.examples:
                self.full_description += "\nExamples:\n\t" + "\n\t".join([example["English"]+"\n\t"+example["Chinese"] for example in self.word.examples])
        if self.row["Details"]: self.full_description += "\nNotes:" + self.row["Details"]

        self.window['back'].update("")
        self.showing = False
        if self.front_choice == "Chinese":
            self.window['front'].update(self.word.hanzi)
        elif self.front_choice == "English":
            self.window['front'].update(self.word.definitions)

    def run(self):
        while True:
            event, values = self.window.read()
            if event == sg.WIN_CLOSED: # if user closes window or clicks cancel
                self.tracker.save("./tracker.pkl")
                break
            if event in ["Show", "b"]:
                if not self.showing:
                    self.window['back'].update(a.full_description if a.full_description else "No Details Available")
                    self.showing = True
                else:
                    self.update_word()
            if event in ["Known", "n"]:
                self.update_word(known=True)
            if event in ["Unknown", "m"]:
                self.update_word(known=False)
            if event == "Page":
                webbrowser.open(a.word.url)
        self.window.close()

a = Application()
a.run()
