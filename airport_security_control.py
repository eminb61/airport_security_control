import simpy
import numpy as np
from constants import *


class AirportSecurityControl:
    def __init__(self, env, logger):
        self.env = env
        self.tray_server = simpy.Resource(env=env, capacity=TRAY_CAPACITY)
        self.xray_server = simpy.Resource(env=env, capacity=XRAY_CAPACITY)
        self.bodyscreen_server = simpy.Resource(env, capacity=BODYSCREEN_CAPACITY)
        self.pre_bodyscreen_waiting_area = simpy.Container(env=env, capacity=BODYSCREEN_WAITING_CAPACITY, init=0)
        self.bodyscreen_waiting_area = simpy.Container(env=env, capacity=BODYSCREEN_WAITING_CAPACITY, init=0)
        self.logger = logger

        # Create lists to hold arrival and departure times
        self.tray_arrival_times = {}
        self.tray_entrance_times = {}
        self.tray_waiting_times = {}
        self.tray_departure_times = {}
        self.xray_arrival_times = {}
        self.xray_waiting_times = {}
        self.xray_departure_times = {}
        self.bodyscreen_arrival_times = {}
        self.bodyscreen_waiting_times = {}
        self.bodyscreen_departure_times = {}
        self.bodyscreen_waiting_area_count = {self.env.now: 0}

        self.trackers = {
            'tray_arrival_times': self.tray_arrival_times,
            'tray_entrance_times': self.tray_entrance_times,
            'tray_waiting_times': self.tray_waiting_times,
            'tray_departure_times': self.tray_departure_times,
            'xray_arrival_times': self.xray_arrival_times,
            'xray_waiting_times': self.xray_waiting_times,
            'xray_departure_times': self.xray_departure_times,
            'bodyscreen_arrival_times': self.bodyscreen_arrival_times,
            'bodyscreen_departure_times': self.bodyscreen_departure_times,
            'bodyscreen_waiting_times': self.bodyscreen_waiting_times,
            'bodyscreen_waiting_area_count': self.bodyscreen_waiting_area_count
        }

    def tray_process(self, passenger):
        arrival = self.env.now
        # Record arrival time
        self.trackers['tray_arrival_times'][passenger.id] = arrival
        self.logger.log(f'Passenger {passenger.id} arrived at tray area at {arrival:.2f}.')
        # Wait until there's a free spot in the waiting area of the body screen area
        yield self.pre_bodyscreen_waiting_area.put(1)
        # Request a server
        with self.tray_server.request() as req:
            yield req
            # Record tray area acceptance time
            self.trackers['tray_entrance_times'][passenger.id] = self.env.now
            # Record tray waiting time
            self.trackers['tray_waiting_times'][passenger.id] = self.env.now - arrival
            self.logger.log(f'Passenger {passenger.id} entered tray area at {self.env.now:.2f}.')
            # Service time at the tray area
            yield self.env.timeout(round(np.random.exponential(SERVICE_MEAN_TRAY), 2))
            # Record departure time after process completion
            self.tray_departure_times[passenger.id] = self.env.now
            self.logger.log(f'Passenger {passenger.id} completed tray process at {self.env.now:.2f}.')
            # Start post tray process
            yield self.env.process(self.post_tray_process(passenger))

    def post_tray_process(self, passenger):
        self.env.process(self.xray_process(passenger))
        # Wait until there's a free spot in the waiting area of the body screen area
        yield self.bodyscreen_waiting_area.put(1)
        self.bodyscreen_waiting_area_count[self.env.now] = self.bodyscreen_waiting_area.level
        self.env.process(self.bodyscreen_process(passenger))

    def xray_process(self, passenger):
        arrival = self.env.now
        # Record arrival time
        self.xray_arrival_times[passenger.id] = arrival
        self.logger.log(f"Passenger {passenger.id}'s luggage entered the x-ray at {arrival:.2f}.")
        # Request a server
        with self.xray_server.request() as req:
            yield req
            # Record xray waiting time
            self.xray_waiting_times[passenger.id] = self.env.now - arrival
            # Service time at the xray
            yield self.env.timeout(round(np.random.exponential(SERVICE_MEAN_XRAY), 2))
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
            # Record bodyscreen waiting time
            self.bodyscreen_waiting_times[passenger.id] = self.env.now - arrival
            yield self.pre_bodyscreen_waiting_area.get(1)
            yield self.bodyscreen_waiting_area.get(1)
            self.bodyscreen_waiting_area_count[self.env.now + 0.0001] = self.bodyscreen_waiting_area.level
            yield self.env.timeout(round(np.random.exponential(SERVICE_MEAN_BODYSCREEN), 2))
            # Record departure time after process completion
            self.bodyscreen_departure_times[passenger.id] = self.env.now
            self.logger.log(f'Passenger {passenger.id} left body screen at {self.env.now:.2f}.')

    def calculate_total_system_time(self):
        self.total_system_times = {}
        for passenger_id in self.tray_arrival_times:
            tray_process_time = self.tray_departure_times[passenger_id] - self.tray_arrival_times[passenger_id]
            bodyscreen_process_time = self.bodyscreen_departure_times[passenger_id] - self.bodyscreen_arrival_times[passenger_id]
            xray_process_time = self.xray_departure_times[passenger_id] - self.tray_arrival_times[passenger_id]

            total_time = max(tray_process_time + bodyscreen_process_time, xray_process_time)
            self.total_system_times[passenger_id] = total_time
            self.logger.log(f'Passenger {passenger_id} spent a total time of {total_time:.2f} in the system.')