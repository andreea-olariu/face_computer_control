import tkinter as tk

from constants import DARK_CONTRAST, MAIN_FONT_NAME, WAITING_MESSAGES, MAIN_COLOR


class CustomText(tk.Label):
    def __init__(self, master, text, **kwargs):
        self.master = master
        self.text = text
        tk.Label.__init__(self, master=master, **kwargs)
        self.load_text()

    def load_text(self):
        if type(self.text) == str:
            self['text'] = self.text
        else:
            self.change_text(0)

    def change_text(self, idx=0):
        if idx == len(self.text):
            idx = 0

        self['text'] = self.text[idx]
        idx += 1

        self.master.after(1000, lambda: self.change_text(idx))


class WaitingMessage(CustomText):
    def __init__(self, master):
        CustomText.__init__(self, master=master, text=WAITING_MESSAGES, bg=MAIN_COLOR, fg=DARK_CONTRAST,
                            highlightbackground=MAIN_COLOR, font=(MAIN_FONT_NAME, 20, 'bold'))


class PredictionText(CustomText):
    def __init__(self, master, text):
        CustomText.__init__(self, master=master, text=text, bg=MAIN_COLOR, fg=DARK_CONTRAST,
                            activebackground=MAIN_COLOR, highlightbackground=MAIN_COLOR,
                            font=(MAIN_FONT_NAME, 20, 'bold'))
