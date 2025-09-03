from PIL import Image, ImageTk
import tkinter as tk
from constants import DIMENSION, ColorPallet, UI_LOGO, GIF_LIMIT, ANIMATION_DELAY, UI_LOADING_GIF


class CustomImage:
    def __init__(self, master, file_path, width, height):
        self.master = master
        self.file_path = file_path
        self.width = width
        self.height = height
        self.label = tk.Label(self.master, border=0)

    def image(self):
        image = Image.open(self.file_path).resize((self.width, self.height))
        image = ImageTk.PhotoImage(image=image)
        self.label.photo = image
        self.label.config(image=image, bg=ColorPallet.MAIN_COLOR)

        return self.label


class LogoImage(CustomImage):
    def __init__(self, master):
        super().__init__(master, UI_LOGO, DIMENSION, int(DIMENSION / 2))


class Gif(CustomImage):
    def __init__(self, master):
        CustomImage.__init__(self, master, UI_LOADING_GIF, DIMENSION, int(DIMENSION / 2))
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

    def image(self):
        info = Image.open(self.file_path)
        frames = info.n_frames

        self.photoimage_objects = []
        for i in range(frames):
            obj = tk.PhotoImage(file=self.file_path, format=f"gif -index {i}")
            self.photoimage_objects.append(obj)

        self.animate(0)

        return self.label
