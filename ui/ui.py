import tkinter as tk

import cv2
from PIL import Image

from constants import DIMENSION, APP_TITLE, MAIN_COLOR
from backend.controller import Act, Actionable
from frame_wrapper import FirstEpisodeFrame, SecondEpisodeFrame, FinalEpisodeFrame
from button_wrapper import StartButton, StopButton
from image_wrapper import LogoImageWrapper, LoadingGifWrapper, CameraImageWrapper
from text_wrapper import WaitingMessage, PredictionText
from frame_wrapper import ThirdEpisodeFrame
from camera_handler import CameraHandler
from utils import send_frame_to_api


class UI:
    def __init__(self):
        self.current_video_frame = None
        self.main_window = None
        self.dimensions = DIMENSION
        self.current_frame = None
        self.camera_handler = CameraHandler()
        self.show_camera = False

    def start(self):
        if self.main_window:
            return

        self.main_window = self.init_window()
        self.create_first_episode()
        self.main_window.mainloop()
        self.current_frame = None

    def init_window(self):
        main_window = tk.Tk(screenName="App")
        main_window.geometry(f"{self.dimensions}x{self.dimensions}")
        main_window.title(APP_TITLE)
        main_window.rowconfigure(0, weight=1)
        main_window.columnconfigure(0, weight=1)
        main_window.config(bg=MAIN_COLOR)

        return main_window

    def clear_window(self):
        if self.current_frame:
            self.current_frame.clear_all_inside_frame()

    def create_first_episode(self):
        self.clear_window()
        current_frame = FirstEpisodeFrame(parent=self.main_window)
        current_frame.grid(row=0, column=0)

        logo = LogoImageWrapper(parent=current_frame)
        logo.image.grid(row=1, column=0)

        start_button = StartButton(parent=current_frame, func=self.create_second_frame)
        start_button.grid(row=2, column=0)

        self.current_frame = current_frame

    def capture_camera(self, current_frame):
        ret, current_video_frame = self.camera_handler.capture_frame()
        self.current_video_frame = current_video_frame

        if ret:
            current_video_frame = cv2.cvtColor(current_video_frame, cv2.COLOR_BGR2RGB)
            current_video_frame = cv2.flip(current_video_frame, 1)
            current_video_frame = Image.fromarray(current_video_frame)
            current_image = CameraImageWrapper(parent=current_frame, image=current_video_frame)

            widget = current_frame.grid_slaves(row=1, column=1)
            if len(widget) > 0:
                widget[0].grid_forget()

            current_image.image.grid(row=1, column=1)

            if self.show_camera:
                current_frame.after(5, self.capture_camera, current_frame, )

    def create_second_frame(self):
        self.clear_window()

        current_frame = SecondEpisodeFrame(parent=self.main_window)
        current_frame.grid(row=0, column=0)

        self.show_camera = True
        self.capture_camera(current_frame)

        gif = LoadingGifWrapper(master=current_frame)
        gif.image.grid(row=1, column=1)

        stop_button = StopButton(master=current_frame, func=self.create_third_episode)
        stop_button.grid(row=4, column=1)

        self.current_frame = current_frame

    def create_third_episode(self):
        self.clear_window()
        self.show_camera = False

        current_frame = ThirdEpisodeFrame(parent=self.main_window)
        current_frame.grid(row=0, column=0)

        text = WaitingMessage(master=current_frame)
        text.grid(row=3, column=1)

        result = send_frame_to_api(self.current_video_frame)

        self.current_frame = current_frame

        self.create_final_episode(result)

    def create_final_episode(self, result: str):
        if result.strip() == "person":
            Actionable().start(Act.Youtube)

        self.clear_window()
        current_frame = FinalEpisodeFrame(parent=self.main_window)

        current_frame.grid(row=0, column=0)
        text = PredictionText(master=current_frame, text=result)
        text.grid(row=1, column=1)

        self.current_frame = current_frame
