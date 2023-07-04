import numpy as np
import pandas as pd
from utils.read_file import read_input_file
from pathlib import Path

def create_arrival_times(df):
    all_times = []
    for i in range(len(df) - 1):
        start_time = df.iloc[i]['time_sec']
        end_time = df.iloc[i + 1]['time_sec']
        num_passengers = df.iloc[i]['total_passengers']

        # Check if there are passengers
        if num_passengers == 0:
            continue

        # Specify the parameters for the normal distribution
        mean = (start_time + end_time) / 2  # Mean is the mid-point of the interval
        std_dev = (end_time - start_time) / 4  # Standard deviation is a quarter of the interval

        # Generate the arrival times
        arrival_times = np.round(np.random.normal(loc=mean, scale=std_dev, size=num_passengers))
        arrival_times[0] = start_time  # Set the first passenger's arrival time to the start time
        arrival_times = np.sort(arrival_times)  # Sort the arrival times

        # Check if any times are beyond the end time and correct them
        arrival_times = np.where(arrival_times > end_time, end_time, arrival_times)
        arrival_times = np.where(arrival_times < start_time, start_time, arrival_times)

        all_times.extend(arrival_times)

    return all_times

def create_pax_arr_process(arrival_times):
    ids = list(range(len(arrival_times)))
    df = pd.DataFrame(ids, columns=['passenger_id'])
    df['arrival_time'] = arrival_times
    # Add interarrival times
    df['interarrival_time'] = df['arrival_time'].diff()
    df['interarrival_time'].iloc[0] = 0
    return df

def create_pax_arrival_process(file_path):
    df = read_input_file(file_path)
    arrival_times = create_arrival_times(df)
    pax_arr_process = create_pax_arr_process(arrival_times)
    # Save the dataframe to a csv file
    pax_arr_process.to_csv(Path(file_path).parent / 'passenger_arrival_process.csv', index=False)


