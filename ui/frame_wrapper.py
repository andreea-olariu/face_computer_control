import tkinter as tk

from constants import DIMENSION, ColorPallet


class CustomFrame(tk.Frame):
    def __init__(self, parent, width, height, bg, rows=1, columns=1):
        tk.Frame.__init__(self, parent, width=width, height=height, bg=bg)

        for i in range(rows + 1):
            self.rowconfigure(i, weight=1)

        for i in range(columns + 1):
            self.columnconfigure(i, weight=1)

    def clear_all_inside_frame(self):

        for widget in self.winfo_children():
            widget.destroy()


class FirstEpisodeFrame(CustomFrame):
    def __init__(self, parent):
        CustomFrame.__init__(self, parent, width=DIMENSION, height=DIMENSION, rows=4, columns=1,
                             bg=ColorPallet.MAIN_COLOR)


class SecondEpisodeFrame(CustomFrame):
    def __init__(self, parent):
        CustomFrame.__init__(self, parent, width=DIMENSION, height=DIMENSION, rows=5, columns=3,
                             bg=ColorPallet.MAIN_COLOR)


class ThirdEpisodeFrame(CustomFrame):
    def __init__(self, parent):
        CustomFrame.__init__(self, parent, width=DIMENSION, height=DIMENSION, rows=5, columns=3,
                             bg=ColorPallet.MAIN_COLOR)
