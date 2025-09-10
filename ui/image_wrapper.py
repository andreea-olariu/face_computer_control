from PIL import Image, ImageTk
import tkinter as tk

from constants import DIMENSION, UI_LOGO, GIF_LIMIT, ANIMATION_DELAY, UI_LOADING_GIF, MAIN_COLOR


class ImageWrapper:
    def __init__(self, master, width, height, file_path, image=None):
        self.master = master
        self.label = tk.Label(self.master, border=0)

        self.img = image
        if self.img is None:
            self.img = Image.open(file_path)

        self.img = self.img.resize((width, height))

    @property
    def image(self):
        img = ImageTk.PhotoImage(image=self.img)
        self.label.photo = img
        self.label.config(image=img, bg=MAIN_COLOR)

        return self.label


class LogoImageWrapper(ImageWrapper):
    def __init__(self, parent):
        super().__init__(parent, DIMENSION, int(DIMENSION / 2), UI_LOGO)


class CameraImageWrapper(ImageWrapper):
    def __init__(self, parent, image):
        super().__init__(master=parent, width=200, height=200, file_path='', image=image)


class LoadingGifWrapper(ImageWrapper):
    def __init__(self, master):
        super().__init__(master, DIMENSION, int(DIMENSION / 2), UI_LOADING_GIF)
        self.photoimage_objects = None
        self.animation_delay = ANIMATION_DELAY
        self.limit = GIF_LIMIT

    def animate(self, idx):
        image = self.photoimage_objects[idx]

        self.label.photo = image
        self.label.config(image=image)
        current_frame = idx + 1

        if current_frame == self.limit:
            current_frame = 0

        self.master.after(self.animation_delay,
                          lambda: self.animate(current_frame))

    @property
    def image(self):
        info = Image.open(UI_LOADING_GIF)
        frames = info.n_frames

        self.photoimage_objects = []
        for i in range(frames):
            obj = tk.PhotoImage(file=UI_LOADING_GIF, format=f"gif -index {i}")
            self.photoimage_objects.append(obj)

        self.animate(0)

        return self.label
