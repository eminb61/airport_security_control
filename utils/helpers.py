import json
from typing import Dict

def seconds_to_hms(seconds):
    hours = seconds // 3600
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60
    return "%02d:%02d:%02d" % (hours, minutes, seconds)


def save_tracker_dicts(trackers, output_path):
    for key, dictionary in trackers.items():
        filename = f"{output_path}/{key}.json"
        save_dict_to_file(dictionary, filename)


def save_dict_to_file(dict_data, filename):
    with open(filename, 'w') as f:
        json.dump(dict_data, f)


def is_time_overlapping(time: int, tracker: Dict = None) -> int:
    if len(tracker) == 0:
        return round(time, 3)
    if time not in list(tracker.keys()):
        return round(time, 3)
    time += 0.001
    return is_time_overlapping(time=time, tracker=tracker)