import PySimpleGUI as sg
from get import Word
from read import get_data
import webbrowser
from track import Tracker
import random

class Application:
    style_args = {
        "font": ("Helvetica", 24)
    }
    def __init__(self):
        self.tracker=Tracker(get_data())

        sg.theme('Default1')
        layout = [  
            [sg.Text(size=(40,1), key='front', **self.style_args)],
            [sg.Button('Show', 	expand_x=True, **self.style_args), sg.Button('Page', **self.style_args)],
            [sg.Text(size=(40,7), key='back', auto_size_text=True, **self.style_args)],
            [sg.Button('Known', 	expand_x=True, **self.style_args), sg.Button('Unknown', 	expand_x=True, **self.style_args)] 
        ]
        self.window = sg.Window('Window Title', layout, finalize=True, return_keyboard_events=True) # , no_titlebar=True
        self.update_word(known=None)

    def update_word(self, known=None):
        hanzi, self.details = self.tracker.advance(known)
        self.word = Word(hanzi)
        if random.random() < 0.5:
            front, back = self.word.hanzi, self.word.definitions
        else:
            front, back = self.word.definitions, self.word.hanzi
        print(front)
        if self.word.yb_exists:
            self.full_description = \
f"""{back}
Pinyin: {self.word.pinyin} 
{"Notes:" if self.details else ""}
{self.details}
"""
        else:
            self.full_description = str(self.details)
        self.window['back'].update("")
        self.showing = False
        self.window['front'].update(front)

    def run(self):
        while True:
            event, values = self.window.read()
            if event == sg.WIN_CLOSED: # if user closes window or clicks cancel
                break
            if event in ["Show", "b"]:
                if not self.showing:
                    self.window['back'].update(a.full_description if a.full_description else "No Details Available")
                    self.showing = True
                elif event == "b":
                    self.update_word(True)
            if event in ["Known", "n"]:
                self.update_word(True)
            if event in ["Unknown", "m"]:
                self.update_word(False)
            if event == "Page":
                webbrowser.open(a.word.url)
        self.window.close()

a = Application()
a.run()
