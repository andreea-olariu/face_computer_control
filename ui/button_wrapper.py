import tkinter as tk
from constants import START_BUTTON_BG_COLOR, MAIN_FONT_NAME, DARK_CONTRAST, START_BUTTON_TEXT, \
    END_BUTTON_TEXT, MAIN_COLOR


class CustomButton(tk.Button):
    def __init__(self, master, command, text, bg, activeforeground, highlightbackground, font, height, width):
        tk.Button.__init__(self, master=master, text=text, command=command, justify="center", cursor="hand1",
                           activeforeground=activeforeground, highlightbackground=highlightbackground, bg=bg, font=font,
                           height=height, width=width)


class StartButton(CustomButton):
    def __init__(self, parent, func):
        CustomButton.__init__(self, master=parent, text=START_BUTTON_TEXT, command=func, bg=START_BUTTON_BG_COLOR,
                              activeforeground=DARK_CONTRAST, highlightbackground=MAIN_COLOR,
                              font=(MAIN_FONT_NAME, 20), height=2, width=20)


class StopButton(CustomButton):
    def __init__(self, master, func):
        CustomButton.__init__(self, master=master, text=END_BUTTON_TEXT, command=func, bg=START_BUTTON_BG_COLOR,
                              activeforeground=DARK_CONTRAST, highlightbackground=MAIN_COLOR,
                              font=(MAIN_FONT_NAME, 20), height=2, width=20)
