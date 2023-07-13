from utils.helpers import save_tracker_dicts
import os

def save_output(trackers, output_path):
    if not os.path.exists(output_path):
        os.makedirs(output_path)
    save_tracker_dicts(trackers, output_path)
