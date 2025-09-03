import tkinter as tk

from constants import ColorPallet, DARK_CONTRAST, MAIN_FONT_NAME, WAITING_MESSAGES


class CustomText(tk.Label):
    def __init__(self, master, texts, **kwargs):
        self.master = master
        self.texts = texts
        tk.Label.__init__(self, master=master, **kwargs)

    def change_text(self, idx=0):
        if idx == len(self.texts):
            idx = 0

        self['text'] = self.texts[idx]
        idx += 1

        self.master.after(1000,
                          lambda: self.change_text(idx))


class WaitingMessage(CustomText):
    def __init__(self, master):
        CustomText.__init__(self, master=master, texts=WAITING_MESSAGES, bg=ColorPallet.MAIN_COLOR, fg=DARK_CONTRAST,
                            highlightbackground=ColorPallet.MAIN_COLOR, font=(MAIN_FONT_NAME, 20, 'bold'))


class ThirdEpisode(CustomText):
    def __init__(self, master):
        CustomText.__init__(self, master=master, texts=WAITING_MESSAGES, bg=ColorPallet.MAIN_COLOR, fg=DARK_CONTRAST,
                            activebackground=ColorPallet.MAIN_COLOR, highlightbackground=ColorPallet.MAIN_COLOR,
                            font=(MAIN_FONT_NAME, 20, 'bold'))
