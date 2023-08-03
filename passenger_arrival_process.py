from utils.read_file import read_input_file
from passenger import Passenger
import numpy as np
import pandas as pd

class PassengerArrivalProcess:
    def __init__(self, env, airport_security_control, logger, file_path, pax_config):
        self.env = env
        self.airport_security_control = airport_security_control
        self.logger = logger
        self.pax_config = pax_config
        if file_path:
            self.pax_arrival_process = get_passenger_arrival_process_from_file(file_path)
        else:
            self.pax_arrival_process = create_passenger_arrival_process(self.pax_config)
        self.env.process(self.create_passenger_arrival())

    def create_passenger_arrival(self):
        for idx, row in self.pax_arrival_process.iterrows():
            yield self.env.timeout(row['interarrival_time'])
            arrival_time = self.env.now
            passenger = self.create_passenger(id=int(row['passenger_id']), 
                                              arrival_time=arrival_time)
            
            self.env.process(self.airport_security_control.tray_process(passenger))

    def create_passenger(self, id, arrival_time):
        return Passenger(id, arrival_time)

def create_passenger_arrival_process(pax_config):
    interarrival_times = np.arange(0, pax_config['num_pax'], pax_config['lambda'])
    return pd.DataFrame({
        'passenger_id': range(len(interarrival_times)),
        # 'interarrival_time': np.random.exponential(scale=pax_config['lambda'], 
        #                                            size=pax_config['num_pax'])
        'interarrival_time': interarrival_times
    }
    )

def get_passenger_arrival_process_from_file(file_path):
    return read_input_file(file_path)