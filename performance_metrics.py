import json
import numpy as np

def load_data(filename):
    with open(f'../outputs/{filename}', 'r') as f:
        data = json.load(f)
    return data

def print_average(data, name, unit='time'):
    vals = np.array(list(data.values()))
    avgerage = np.mean(vals)
    print(f'Average {name} {unit}: {avgerage:.2f}')

def compute_performance_metrics():
    tracker_names = [
        'tray_waiting_times',
        'tray_queue_lengths',
        'xray_waiting_times',
        'xray_queue_lengths',
        'bodyscreen_waiting_times',
        'bodyscreen_waiting_area_count',
        'pre_bodyscreen_waiting_area_count',
        'total_system_times'
    ]

    # Load data from JSON files and print average times
    for name in tracker_names:
        data = load_data(f'{name}.json')
        unit = 'time'
        if name.endswith('_queue_lengths') or name.endswith('_waiting_area_count'):
            unit = 'length' if name.endswith('_queue_lengths') else 'count'
        print_average(data, name, unit)
    

def main():
    compute_performance_metrics()

if __name__ == '__main__':
    main()

