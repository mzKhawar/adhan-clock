from typing import Tuple


def to_time_tuple(time: str) -> Tuple[str, str]:
    time_array = time.split(":")
    hour = time_array[0]
    minute = time_array[1]
    return hour, minute


# TODO: fix sub > 60 min bug
def subtract_minutes(sub_min: int, time: str) -> str:
    hour, minute = to_time_tuple(time)
    minute_int = int(minute)
    hour_int = int(hour)
    minute_int = minute_int - sub_min
    if minute_int < 0:
        hour_int = hour_int - 1
        minute_int = minute_int % 60
    hour_int = hour_int % 24
    hour = str(hour_int)
    minute = str(minute_int)
    time = f"{hour}:{minute}"
    return time

# TODO: fix add > 60 min bug
def add_minutes(adl_min: int, time: str) -> str:
    hour, minute = to_time_tuple(time)
    minute_int = int(minute)
    hour_int = int(hour)
    minute_int = minute_int + adl_min
    if minute_int > 59:
        hour_int = hour_int + 1
        minute_int = minute_int % 60
    hour_int = hour_int % 24
    hour = str(hour_int)
    minute = str(minute_int)
    time = f"{hour}:{minute}"
    return time
