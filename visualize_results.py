# import matplotlib.pyplot as plt

# def visualize_results(dict_data, title, x_label, y_label):
#     lists = sorted(dict_data.items())
#     x, y = zip(*lists)
#     plt.figure(figsize=(10,6))
#     plt.scatter(x, y)
#     plt.title(title)
#     plt.xlabel(x_label)
#     plt.ylabel(y_label)
#     plt.show()

# plot_dict(airport_security_control.total_system_times, "Passenger Total Time Spent in the System", "Passenger ID", "Time in System")
# plot_dict(airport_security_control.bodyscreen_waiting_area_count, "Body Screen Waiting Area Count", "Simulation Time", "Count")


import json
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np


def load_data(filename):
    with open(f'../outputs/{filename}', 'r') as f:
        data = json.load(f)
    return data

def plot_histogram(data, title, x_label, y_label):
    plt.figure(figsize=(10,6))
    plt.hist(data, bins=30)
    plt.title(title)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.show()

def plot_scatter_time_series(data, title, x_label, y_label):
    lists = sorted(data.items())
    x, y = zip(*lists)
    plt.figure(figsize=(10,6))
    plt.scatter(x, y)
    plt.title(title)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.show()

def print_avg_times(data, name):
    times = np.array(list(data.values()))
    avg_time = np.mean(times)
    print(f'Average {name} time: {avg_time:.2f}')

def main():
    # Load data from JSON files
    tray_waiting_times = load_data('tray_waiting_times.json')
    xray_waiting_times = load_data('xray_waiting_times.json')
    bodyscreen_waiting_times = load_data('bodyscreen_waiting_times.json')
    total_system_times = load_data('total_system_times.json')
    bodyscreen_waiting_area_count = load_data('bodyscreen_waiting_area_count.json')

    # Generate plots
    plot_histogram(list(tray_waiting_times.values()), 'Tray Waiting Times', 'Time', 'Frequency')
    plot_histogram(list(xray_waiting_times.values()), 'Xray Waiting Times', 'Time', 'Frequency')
    plot_histogram(list(bodyscreen_waiting_times.values()), 'Body Screen Waiting Times', 'Time', 'Frequency')
    plot_histogram(list(total_system_times.values()), 'Total System Times', 'Time', 'Frequency')
    plot_scatter_time_series(bodyscreen_waiting_area_count, 'Body Screen Waiting Area Count Over Time', 'Time', 'Count')

    # Print average times
    print_avg_times(tray_waiting_times, 'tray waiting')
    print_avg_times(xray_waiting_times, 'xray waiting')
    print_avg_times(bodyscreen_waiting_times, 'body screen waiting')
    print_avg_times(total_system_times, 'system')

if __name__ == '__main__':
    main()