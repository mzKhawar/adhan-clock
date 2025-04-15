import requests
from datetime import date
from crontab import CronTab
from typing import Dict, List
from utils.time_utils import to_time_tuple, add_minutes, subtract_minutes
from utils.enums import Path, Command
import sys


class AdhanClock:
    def __init__(self):
        self.CRON = CronTab(user="mkhawar")
        self.CRON.env['PYTHONPATH'] = '/home/mkhawar/adhan-clock'
        self.PARAMS: Dict[str: float | int] = {"latitude": 42.0324, "longitude": -87.7416, "school": 1}
        self.PLAY_AUDIO_FILE: str = f"{Command.SOUND} {Path.VENV} {Path.COMMANDS}/{{}}"
        self.PY_CMD: str = f"{Path.VENV} {Path.COMMANDS}/{{}}"
        self.timings: Dict[str: str] = {}
        self.prayer_times: List[str] = []
        self.sunrise: str | None = None
        self.fajr_time: str | None = None
        self.dhuhr_time: str | None = None
        self.asr_time: str | None = None
        self.maghrib_time: str | None = None
        self.isha_time: str | None = None
        self.today: str = date.today().strftime("%d-%m-%Y")

    def set_prayer_times(self):
        r = requests.get(
            f"https://api.aladhan.com/v1/timings/{self.today}", params=self.PARAMS
        )
        json_data = r.json()
        self.timings = json_data["data"]["timings"]

        self.fajr_time = self.timings["Fajr"]
        self.dhuhr_time = self.timings["Dhuhr"]
        self.asr_time = self.timings["Asr"]
        self.maghrib_time = self.timings["Maghrib"]
        self.isha_time = self.timings["Isha"]

        self.prayer_times = [self.fajr_time, self.dhuhr_time, self.asr_time, self.maghrib_time, self.isha_time]

    def set_cron(
        self, time: str, command: str | Command, play_audio_command: str | Command | None = None
    ):
        hour, minute = to_time_tuple(time)
        if play_audio_command:
            job = self.CRON.new(command=self.PLAY_AUDIO_FILE.format(play_audio_command))
        else:
            job = self.CRON.new(command)

        job.hour.on(hour)
        job.minute.on(minute)
        self.CRON.write()

    def set_prayers_cron(self):
        for prayer_time in self.prayer_times:
            if prayer_time == self.fajr_time:
                self.set_cron(
                    prayer_time, self.PLAY_AUDIO_FILE, Command.PLAY_FAJR_ADHAN
                )
            else:
                self.set_cron(prayer_time, self.PLAY_AUDIO_FILE, Command.PLAY_ADHAN)

    def set_rehman_cron(self):
        self.sunrise = self.timings["Sunrise"]
        times = [
            add_minutes(10, self.sunrise),
            add_minutes(10, self.dhuhr_time),
            add_minutes(10, self.maghrib_time)
        ]
        for time in times:
            self.set_cron(time, self.PLAY_AUDIO_FILE, Command.PLAY_REHMAN)

    def set_baqarah_cron(self):
        time = add_minutes(40, self.sunrise)
        self.set_cron(time, self.PLAY_AUDIO_FILE, Command.PLAY_BAQARAH_FAST)

    def set_darood_cron(self):
        time = subtract_minutes(120, self.fajr_time)
        self.set_cron(time, self.PLAY_AUDIO_FILE, Command.PLAY_DAROOD)

    def set_bt_connect_cron(self):
        bluetooth_connect_times = []
        for i in range(len(self.prayer_times)):
            bluetooth_connect_times.insert(i, subtract_minutes(2, self.prayer_times[i]))

        for time in bluetooth_connect_times:
            self.set_cron(time, self.PY_CMD.format(Command.CHECK_BLUETOOTH))

    def set_clear_cron(self):
        time = "00:01"
        self.set_cron(time, self.PY_CMD.format(Command.CLEAR_CRON))

    def set_all_cron(self):
        self.set_prayers_cron()
        self.set_rehman_cron()
        self.set_baqarah_cron()
        self.set_darood_cron()
        self.set_bt_connect_cron()
        self.set_clear_cron()

    def run(self):
        self.set_prayer_times()
        self.set_all_cron()


if __name__ == "__main__":
    adhan_clock = AdhanClock()
    adhan_clock.run()
    sys.exit()
