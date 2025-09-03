import tkinter as tk

from constants import DIMENSION, APP_TITLE, ColorPallet
from frame_wrapper import FirstEpisodeFrame, SecondEpisodeFrame
from button_wrapper import StartButton, StopButton
from image_wrapper import LogoImage, Gif
from text_wrapper import WaitingMessage, ThirdEpisode
from frame_wrapper import ThirdEpisodeFrame


class UI:
    def __init__(self):
        self.current_frame = None
        self.main_window = None
        self.dimensions = DIMENSION
        self.current_frame = None

    def start(self):
        if self.main_window:
            return

        self.main_window = tk.Tk(screenName="App")
        self.main_window.geometry(f"{self.dimensions}x{self.dimensions}")
        self.main_window.title(APP_TITLE)
        self.main_window.rowconfigure(0, weight=1)
        self.main_window.columnconfigure(0, weight=1)
        self.main_window.config(bg=ColorPallet.MAIN_COLOR)
        self.create_first_episode()
        self.main_window.mainloop()

        self.current_frame = None

    def create_episode(self):
        if self.current_frame:
            self.current_frame.clear_all_inside_frame()

    def create_first_episode(self):
        self.create_episode()

        current_frame = FirstEpisodeFrame(parent=self.main_window)
        current_frame.grid(row=0, column=0)

        logo = LogoImage(master=current_frame)
        logo.image().grid(row=1, column=0)

        start_button = StartButton(master=current_frame, func=self.create_second_frame)
        start_button.grid(row=2, column=0)

        self.current_frame = current_frame

    def create_second_frame(self):
        self.create_episode()

        current_frame = SecondEpisodeFrame(parent=self.main_window)
        current_frame.grid(row=0, column=0)

        gif = Gif(master=current_frame)
        gif.image().grid(row=2, column=1)

        waiting_message = WaitingMessage(master=current_frame)
        waiting_message.grid(row=3, column=1)

        stop_button = StopButton(master=current_frame, func=self.create_third_episode)
        stop_button.grid(row=4, column=1)

        self.current_frame = current_frame

    def create_third_episode(self):
        self.create_episode()

        current_frame = ThirdEpisodeFrame(parent=self.main_window)
        current_frame.grid(row=0, column=0)

        text = ThirdEpisode(master=current_frame)
        text.grid(row=3, column=1)
        text.change_text(0)

        self.current_frame = current_frame


ui = UI()
ui.start()
