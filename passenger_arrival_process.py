from utils.read_file import read_input_file
from passenger import Passenger

class PassengerArrivalProcess:
    def __init__(self, env, airport_security_control, logger, file_path):
        self.env = env
        self.airport_security_control = airport_security_control
        self.logger = logger
        self.pax_arrival_process = get_passenger_arrival_process(file_path)
        self.env.process(self.create_passenger_arrival())

    def create_passenger_arrival(self):
        for idx, row in self.pax_arrival_process.iloc[:1000].iterrows():
            yield self.env.timeout(row['interarrival_time'])
            arrival_time = self.env.now
            passenger = self.create_passenger(id=int(row['passenger_id']), 
                                              arrival_time=arrival_time)
            
            self.env.process(self.airport_security_control.tray_process(passenger))
            

    def create_passenger(self, id, arrival_time):
        return Passenger(id, arrival_time)


def get_passenger_arrival_process(file_path):
    return read_input_file(file_path)