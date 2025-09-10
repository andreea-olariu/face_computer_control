import os.path
from abc import ABC, abstractmethod
import subprocess

import numpy as np
import sounddevice as sd
from pydub import AudioSegment
import webbrowser
from enum import Enum

from contants import ENABLE_FOCUS_COMMAND_NAME, DISABLE_FOCUS_COMMAND_NAME, ELEVATOR_MUSIC_SOUND, YOUTUBE_URL


class Act(Enum):
    Focus = 1
    Screen = 2
    Music = 3
    Youtube = 4


class Actionable:
    def __init__(self):
        pass

    def start(self, action: Act):
        if action == Act.Focus:
            ElevatorMusicPlayerAction().stop()
            FocusModeAction().start()

        if action == Act.Screen:
            ScreenSaverAction().start()

        if action == Act.Music:
            FocusModeDisableAction().start()
            ElevatorMusicPlayerAction().start()

        if action == Act.Youtube:
            StartYoutubeAction().start()


class Action(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def start(self):
        pass


class ShortcutsController:

    def __init__(self):
        pass

    @staticmethod
    def run_command(commands: list[str] = None):
        if not commands:
            return
        subprocess.run(commands)


class FocusModeController:

    @staticmethod
    def enable():
        ShortcutsController.run_command(commands=["shortcuts", "run", ENABLE_FOCUS_COMMAND_NAME])

    @staticmethod
    def disable():
        ShortcutsController.run_command(commands=["shortcuts", "run", DISABLE_FOCUS_COMMAND_NAME])


class FocusModeAction(Action):
    def __init__(self):
        super().__init__()

    def start(self):
        FocusModeController.enable()


class FocusModeDisableAction(Action):
    def __init__(self):
        super().__init__()

    def start(self):
        FocusModeController.disable()


class ScreenSaverAction(Action):
    def __init__(self):
        super().__init__()

    def start(self):
        ShortcutsController.run_command(['open', '-a', 'ScreenSaverEngine'])


class Player:
    def __int__(self):
        pass

    def __convert_sound_to_numpy(self, sound_path: str):
        song = AudioSegment.from_mp3(sound_path)

        song = np.array(song.get_array_of_samples())

        return song

    def play(self, sound_path: str):
        if not os.path.exists(sound_path):
            return False

        sound_array = self.__convert_sound_to_numpy(sound_path)

        sd.play(sound_array)
        sd.wait()

        return True

    def stop(self):
        sd.stop()


class ElevatorMusicPlayerAction(Action):
    def __init__(self):
        super().__init__()
        self.player = Player()

    def start(self):
        self.player.play(ELEVATOR_MUSIC_SOUND)

    def stop(self):
        self.player.stop()


class StartYoutubeAction(Action):
    def start(self):
        webbrowser.get('safari').open_new(YOUTUBE_URL)
