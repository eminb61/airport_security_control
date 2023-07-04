import simpy
import numpy as np
from logger import Logger
from passenger_arrival_process import PassengerArrivalProcess

# Parameters
# INTERARRIVAL_MEAN = 60.0
SERVICE_MEAN_TRAY = 38 # seconds
SERVICE_MEAN_XRAY = 30
SERVICE_MEAN_BODYSCREEN = 30

NUM_CONTROL_AREAS = 6
# Number of servers
NUM_TRAY_AREAS = 4*NUM_CONTROL_AREAS
NUM_XRAYS = 4*NUM_CONTROL_AREAS
NUM_BODYSCREENS = 3*NUM_CONTROL_AREAS
# Queues
TRAY_CAPACITY = 4*NUM_TRAY_AREAS
XRAY_CAPACITY = 1*NUM_XRAYS
BODYSCREEN_CAPACITY = 1*NUM_BODYSCREENS

# Waiting Rooms
BODYSCREEN_WAITING_CAPACITY = 5*NUM_BODYSCREENS

INPUT_PATH = 'inputs/passenger_arrival_process.csv'

class AirportSecurityControl:
    def __init__(self, env, logger):
        self.env = env
        self.tray_server = simpy.Resource(env, TRAY_CAPACITY)
        self.xray_server = simpy.Resource(env, XRAY_CAPACITY)
        self.bodyscreen_server = simpy.Resource(env, BODYSCREEN_CAPACITY)
        self.pre_bodyscreen_waiting_area = simpy.Container(env, BODYSCREEN_WAITING_CAPACITY, init=0)
        self.bodyscreen_waiting_area = simpy.Container(env, BODYSCREEN_WAITING_CAPACITY, init=0)
        self.logger = logger

        # Create lists to hold arrival and departure times
        self.tray_arrival_times = {}
        self.tray_departure_times = {}
        self.xray_arrival_times = {}
        self.xray_departure_times = {}
        self.bodyscreen_arrival_times = {}
        self.bodyscreen_departure_times = {}

    def tray_process(self, passenger):
        arrival = self.env.now
        # Record arrival time
        self.tray_arrival_times[passenger.id] = arrival
        self.logger.log(f'Passenger {passenger.id} arrived at tray area at {arrival:.2f}.')
        yield self.pre_bodyscreen_waiting_area.put(1)
        # Request a server
        with self.tray_server.request() as req:
            yield req
            yield self.env.timeout(np.random.exponential(SERVICE_MEAN_TRAY))
            # Record departure time after process completion
            self.tray_departure_times[passenger.id] = self.env.now
            self.logger.log(f'Passenger {passenger.id} completed tray process at {self.env.now:.2f}.')
            # Start post tray process
            yield self.env.process(self.post_tray_process(passenger))

    def post_tray_process(self, passenger):
        self.env.process(self.xray_process(passenger))
        # Wait until there's a free spot in the waiting area of the body screen area
        yield self.bodyscreen_waiting_area.put(1)
        self.env.process(self.bodyscreen_process(passenger))

    def xray_process(self, passenger):
        arrival = self.env.now
        # Record arrival time
        self.xray_arrival_times[passenger.id] = arrival
        self.logger.log(f"Passenger {passenger.id}'s luggage entered the x-ray at {arrival:.2f}.")
        # Request a server
        with self.xray_server.request() as req:
            yield req
            # Service time at the xray
            yield self.env.timeout(np.random.exponential(SERVICE_MEAN_XRAY))
            # Record departure time after process completion
            self.xray_departure_times[passenger.id] = self.env.now
            self.logger.log(f"Passenger {passenger.id}'s luggage left the x-ray at {self.env.now:.2f}.")

    def bodyscreen_process(self, passenger):
        arrival = self.env.now
        # Record arrival time
        self.bodyscreen_arrival_times[passenger.id] = arrival
        self.logger.log(f'Passenger {passenger.id} arrived at body screen at {arrival:.2f}.')
        # Request a server
        with self.bodyscreen_server.request() as req:
            yield req
            yield self.pre_bodyscreen_waiting_area.get(1)
            yield self.bodyscreen_waiting_area.get(1)
            yield self.env.timeout(np.random.exponential(SERVICE_MEAN_BODYSCREEN))
            # Record departure time after process completion
            self.bodyscreen_departure_times[passenger.id] = self.env.now
            self.logger.log(f'Passenger {passenger.id} left body screen at {self.env.now:.2f}.')


# Create environment and start processes
env = simpy.Environment()
logger = Logger(env=env, output_folder_path='../logs')
airport_security_control = AirportSecurityControl(env, logger)
passenger_arrival = PassengerArrivalProcess(env=env, airport_security_control=airport_security_control, logger=logger, file_path=INPUT_PATH)

# Execute!
env.run()
