from enum import Enum


class Path(Enum):
    BASE = "/home/mkhawar/adhan-clock"
    VENV = "/home/mkhawar/adhan-clock/venv/bin/python"
    LIBRARY = "/home/mkhawar/adhan-clock/library"
    COMMANDS = "/home/mkhawar/adhan-clock/commands"

    def __str__(self):
        return self.value


class Command(Enum):
    SOUND = "XDG_RUNTIME_DIR=/run/user/1000"
    CHECK_BLUETOOTH = "check_bluetooth.py"
    CLEAR_CRON = "clear_cron.py"
    PLAY_ADHAN = "play_adhan.py"
    PLAY_FAJR_ADHAN = "play_fajr_adhan.py"
    PLAY_BAQARAH_FAST = "play_baqarah_fast.py"
    PLAY_DAROOD = "play_darood.py"
    PLAY_REHMAN = "play_rehman.py"

    def __str__(self):
        return self.value


class Library(Enum):
    ADHAN = "basit_adhan.wav"
    FAJR_ADHAN = "fajr_adhan.wav"
    BAQARAH = "baqarah.mp3"
    REHMAN = "rehman.wav"
    DAROOD_SHARIF_313 = "darood_sharif_313.mp3"

    def __str__(self):
        return self.value
