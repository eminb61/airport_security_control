import logging
import os
import datetime
from utils.helpers import seconds_to_hms

class CustomFormatter(logging.Formatter):
    def __init__(self, fmt, env):
        super().__init__(fmt)
        self.env = env

    def formatTime(self, record, datefmt=None):
        simulation_time = self.env.now
        return seconds_to_hms(simulation_time)

class Logger:
    def __init__(self, env, output_folder_path=""):
        self.output_folder_path = output_folder_path
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)
        
        # create a file handler
        handler = logging.FileHandler(self.set_logfile_path(__name__))
        handler.setLevel(logging.INFO)

        # add the handlers to the logger
        formatter = CustomFormatter('%(asctime)s [%(levelname)s] - %(message)s', env)
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
        
    def set_logfile_path(self, name):
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        if not os.path.exists(f'{self.output_folder_path}/logs/{name}'):
            os.makedirs(f'{self.output_folder_path}/logs/{name}')
        return f'{self.output_folder_path}/logs/{name}/{name}_{timestamp}.log'

    def log(self, message):
        self.logger.info(message)