import tkinter as tk
from PIL import ImageTk, Image


class UIConstants:
    BG_COLOR = '#d9b5ff'
    START_BUTTON_TEXT = "START"
    END_BUTTON_TEXT = "STOP"
    START_BUTTON_BG_COLOR = '#b196ff'
    DARK_CONTRAST = '#5e06d1'
    MAIN_FONT_NAME = 'Marker Felt'
    UI_LOGO = './assets/images/logo3-removebg-preview.png'
    UI_LOADING_GIF = './assets/images/spinner2.gif'
    WAITING_MESSAGES = ['Analyzing all details...', "Doing complex smart stuff", "Is that you? You look good today!"]


def create_frame(parent_frame, styles, rows=1, columns=1):
    frame = tk.Frame(parent_frame, **styles)

    for i in range(rows + 1):
        frame.rowconfigure(i, weight=1)

    for i in range(columns + 1):
        frame.columnconfigure(i, weight=1)

    return frame


def create_image_in_label(frame, file_path: str, format: str = None):
    image = Image.open(file_path).resize((400, 220))

    extra = {}
    if format:
        extra['format'] = format

    image = ImageTk.PhotoImage(image=image, **extra)

    styles = {
        "border": 0,
        "bg": UIConstants.BG_COLOR
    }

    label = tk.Label(frame, **styles)
    label.photo = image
    label.config(image=image)

    return label


def clear_all_inside_frame(frame):
    for widget in frame.winfo_children():
        widget.destroy()


def animation_gif(gif_label: tk.Label, index: int, photoimage_objects: list, main_frame: tk.Frame, limit: int = 30,
                  animation_delay: int = 50):
    image = photoimage_objects[index]

    gif_label.photo = image
    gif_label.config(image=image)
    current_frame = index + 1

    if current_frame == limit:
        current_frame = 0

    main_frame.after(animation_delay,
                     lambda: animation_gif(gif_label, current_frame, photoimage_objects, main_frame))


def display_gif(main_frame: tk.Frame, gif_label: tk.Label, file_path: str):
    # display first frame
    info = Image.open(file_path)
    frames = info.n_frames

    photoimage_objects = []
    for i in range(frames):
        obj = tk.PhotoImage(file=file_path, format=f"gif -index {i}")
        photoimage_objects.append(obj)

    # animate by changing the frame
    animation_gif(gif_label, 0, photoimage_objects, main_frame)


def change_text(main_frame: tk.Frame, current_index: int, label: tk.Label, delay_change: int = 1000):
    if current_index == len(UIConstants.WAITING_MESSAGES):
        current_index = 0

    label["text"] = UIConstants.WAITING_MESSAGES[current_index]
    current_index += 1

    main_frame.after(delay_change, lambda: change_text(main_frame, current_index, label))


def create_app_button(frame: tk.Frame, func, text: str):
    styles = {
        "text": text,
        "bg": UIConstants.START_BUTTON_BG_COLOR,
        "activeforeground": UIConstants.DARK_CONTRAST,
        "highlightbackground": UIConstants.BG_COLOR,
        "font": (UIConstants.MAIN_FONT_NAME, 20),
        "height": 2,
        "justify": "center",
        "width": 10,
        "cursor": "hand1",
        "command": func
    }

    return tk.Button(frame, **styles)


class UI:
    def __init__(self, controller, backend_stop):
        self.main_window = None
        self.controller = controller
        self.first_episode_frame = None
        self.second_episode_frame = None
        self.dimensions = 400
        self.backend_stop = backend_stop

    def start(self):
        self.main_window = tk.Tk(screenName="App")
        self.main_window.geometry(f"{self.dimensions}x{self.dimensions}")
        self.main_window.title("My App :)")
        self.main_window.config(bg=UIConstants.BG_COLOR)
        self.main_window.rowconfigure(0, weight=1)
        self.main_window.columnconfigure(0, weight=1)

        self.create_first_frame()

        self.main_window.mainloop()

    def create_first_frame(self):
        self.first_episode_frame = create_frame(self.main_window, {"width": self.dimensions, "height": self.dimensions,
                                                                   "bg": UIConstants.BG_COLOR}, rows=3, columns=2)

        self.first_episode_frame.grid(row=0, column=0)

        start_button = self.create_start_button(self.first_episode_frame)
        logo = create_image_in_label(self.first_episode_frame, UIConstants.UI_LOGO)

        logo.grid(row=1, column=1)
        start_button.grid(row=2, column=1)

    def create_second_frame(self):
        clear_all_inside_frame(self.first_episode_frame)

        self.second_episode_frame = create_frame(self.main_window, {"width": self.dimensions, "height": self.dimensions,
                                                                    "bg": UIConstants.BG_COLOR}, rows=5, columns=3)
        self.second_episode_frame.grid(row=0, column=0)

        gif_label = tk.Label(self.second_episode_frame, image="", border=0)
        gif_label.grid(row=2, column=1)
        display_gif(self.second_episode_frame, gif_label, UIConstants.UI_LOADING_GIF)

        text_styles = {
            "text": "",
            "bg": UIConstants.BG_COLOR,
            "fg": UIConstants.DARK_CONTRAST,
            "activebackground": UIConstants.BG_COLOR,
            "highlightbackground": UIConstants.BG_COLOR,
            "font": (UIConstants.MAIN_FONT_NAME, 20, 'bold')

        }
        text_label = tk.Label(self.second_episode_frame, **text_styles)
        text_label.grid(row=3, column=1)
        change_text(main_frame=self.second_episode_frame, current_index=0, label=text_label)

        stop_button = self.create_stop_button(self.second_episode_frame)
        stop_button.grid(row=4, column=1)

    def create_stop_button(self, frame):
        def helper():
            self.backend_stop()

        return create_app_button(frame, helper, UIConstants.END_BUTTON_TEXT)

    def create_start_button(self, frame):
        def helper():
            self.controller()
            self.create_second_frame()

        return create_app_button(frame, helper, UIConstants.START_BUTTON_TEXT)
