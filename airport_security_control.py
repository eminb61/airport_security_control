import simpy
import numpy as np
from constants import *
from utils.helpers import is_time_overlapping

class AirportSecurityControl:
    def __init__(self, env, logger, logging=True):
        self.env = env
        self.tray_server = simpy.Resource(env=env, capacity=TRAY_CAPACITY)
        self.xray_server = simpy.Resource(env=env, capacity=XRAY_CAPACITY)
        self.bodyscreen_server = simpy.Resource(env, capacity=BODYSCREEN_CAPACITY)
        self.bodyscreen_waiting_area = simpy.Container(env=env, capacity=BODYSCREEN_WAITING_CAPACITY, init=0)
        self.logger = logger
        self.logging = logging
        self.initialize_trackers()

    def initialize_trackers(self):
        tracker_names = [
            'tray_arrival_times',
            'tray_process_times',
            'tray_queue_waiting_times',
            'tray_process_end_times',
            'tray_departure_times',
            'tray_queue_lengths',
            'xray_arrival_times',
            'xray_queue_waiting_times',
            'xray_process_times',
            'xray_departure_times',
            'xray_queue_lengths',
            'bodyscreen_arrival_times',
            'bodyscreen_queue_waiting_times',
            'bodyscreen_entrance_waiting_times',
            'bodyscreen_process_times',
            'bodyscreen_departure_times',
            'bodyscreen_queue_lengths',
            'bodyscreen_waiting_area_count',
            'total_system_times'
        ]

        for name in tracker_names:
            if name in ['bodyscreen_waiting_area_count', 
                        'tray_queue_lengths', 
                        'xray_queue_lengths']:
                setattr(self, name, {self.env.now: 0})
            else:
                setattr(self, name, {})

        self.trackers = {name: getattr(self, name) for name in tracker_names}        

    def tray_process(self, passenger):
        arrival = self.env.now
        # Record arrival time
        self.trackers['tray_arrival_times'][passenger.id] = arrival
        if self.logging:
            self.logger.log(f'Passenger {passenger.id} arrived at tray area at {arrival:.2f}.')
   
        # Request a server
        tray_request = self.tray_server.request()
        # Save the queue length
        time = is_time_overlapping(time=self.env.now, tracker=self.trackers['tray_queue_lengths'])
        self.trackers['tray_queue_lengths'][time] = len(self.tray_server.queue)
        yield tray_request
        # Record tray waiting time
        self.trackers['tray_queue_waiting_times'][passenger.id] = self.env.now - arrival
        if self.logging:
            self.logger.log(f'Passenger {passenger.id} entered tray area at {self.env.now:.2f}.')
        # Service time at the tray area
        tray_process_time = round(np.random.exponential(SERVICE_MEAN_TRAY), 2)
        yield self.env.timeout(tray_process_time)

        # Save tray process end time
        tray_end_time = self.env.now
        self.trackers['tray_process_end_times'][passenger.id] = tray_end_time

        # Record tray process time
        self.trackers['tray_process_times'][passenger.id] = tray_process_time  
        
        # Start the xray process
        # yield self.env.process(self.initial_xray_process(passenger, tray_request))  
        yield self.env.process(self.initial_xray_process(passenger, tray_request))
    
    def initial_xray_process(self, passenger, tray_request):
        arrival = self.env.now
        # Record arrival time
        self.trackers['xray_arrival_times'][passenger.id] = arrival
        # Request a server
        xray_request = self.xray_server.request()
        # Save the queue length
        time = is_time_overlapping(time=self.env.now, tracker=self.trackers['xray_queue_lengths'])
        self.trackers['xray_queue_lengths'][time] = len(self.xray_server.queue)
        yield xray_request

        xray_request_end_time = self.env.now

        # Record xray waiting time
        self.trackers['xray_queue_waiting_times'][passenger.id] = xray_request_end_time - arrival

        if self.logging:
            self.logger.log(f"Passenger {passenger.id}'s luggage entered the x-ray at {arrival:.2f}.")

        # Wait until there's a free spot in the waiting area of the body screen area
        yield self.bodyscreen_waiting_area.put(1)
        time = is_time_overlapping(time=self.env.now, tracker=self.trackers['bodyscreen_waiting_area_count'])
        self.trackers['bodyscreen_waiting_area_count'][time] = self.bodyscreen_waiting_area.level
        self.trackers['bodyscreen_entrance_waiting_times'][passenger.id] = self.env.now - xray_request_end_time

        # Release tray server
        self.tray_server.release(tray_request)

        # ------
        # Record departure time after process completion
        self.trackers['tray_departure_times'][passenger.id] = self.env.now
        if self.logging:
            self.logger.log(f'Passenger {passenger.id} completed tray process at {self.env.now:.2f}.')

        # # Start post tray process
        self.env.process(self.xray_process(passenger, xray_request))
        self.env.process(self.bodyscreen_process(passenger))   

    def xray_process(self, passenger, xray_request):
        # Service time at the xray
        xray_process_time = round(np.random.exponential(SERVICE_MEAN_XRAY), 2)
        yield self.env.timeout(xray_process_time)

        # Record xray process time
        self.trackers['xray_process_times'][passenger.id] = xray_process_time

        # Release xray server
        self.xray_server.release(xray_request)

        # Record departure time after process completion
        self.trackers['xray_departure_times'][passenger.id] = self.env.now
        if self.logging:
            self.logger.log(f"Passenger {passenger.id}'s luggage left the x-ray at {self.env.now:.2f}.")

    def bodyscreen_process(self, passenger):
        arrival = self.env.now
        # Record arrival time
        self.trackers['bodyscreen_arrival_times'][passenger.id] = arrival
        if self.logging:
            self.logger.log(f'Passenger {passenger.id} arrived at body screen at {arrival:.2f}.')
        # Request a server
        bodyscreen_request = self.bodyscreen_server.request()
        # Save the queue length
        time = is_time_overlapping(time=self.env.now, tracker=self.trackers['bodyscreen_queue_lengths'])
        self.trackers['bodyscreen_queue_lengths'][time] = len(self.bodyscreen_server.queue)
        yield bodyscreen_request

        # Record bodyscreen waiting time
        self.trackers['bodyscreen_queue_waiting_times'][passenger.id] = self.env.now - arrival
        yield self.bodyscreen_waiting_area.get(1)

        time = is_time_overlapping(time=self.env.now, tracker=self.trackers['bodyscreen_waiting_area_count'])
        self.trackers['bodyscreen_waiting_area_count'][time] = self.bodyscreen_waiting_area.level

        # Service time at the bodyscreen
        bodyscreen_process_time = round(np.random.exponential(SERVICE_MEAN_BODYSCREEN), 2)
        yield self.env.timeout(bodyscreen_process_time)

        # Record bodyscreen process time
        self.trackers['bodyscreen_process_times'][passenger.id] = bodyscreen_process_time

        # Release bodyscreen server
        self.bodyscreen_server.release(bodyscreen_request)

        # Record departure time after process completion
        self.trackers['bodyscreen_departure_times'][passenger.id] = self.env.now
        if self.logging:
            self.logger.log(f'Passenger {passenger.id} left body screen at {self.env.now:.2f}.')

    def calculate_total_system_time(self):
        for passenger_id in self.trackers['tray_arrival_times'].keys():
            tray_process_time = self.trackers['tray_departure_times'][passenger_id] - self.trackers['tray_arrival_times'][passenger_id]
            bodyscreen_process_time = self.trackers['bodyscreen_departure_times'][passenger_id] - self.trackers['bodyscreen_arrival_times'][passenger_id]
            tray_and_xray_process_time = self.trackers['xray_departure_times'][passenger_id] - self.trackers['tray_arrival_times'][passenger_id]

            total_time = max(tray_process_time + bodyscreen_process_time, tray_and_xray_process_time)
            self.trackers['total_system_times'][passenger_id] = total_time
            self.logger.log(f'Passenger {passenger_id} spent a total time of {total_time:.2f} in the system.')