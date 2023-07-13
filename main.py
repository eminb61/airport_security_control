import simpy
import numpy as np

from airport_security_control import AirportSecurityControl
from logger import Logger
from passenger_arrival_process import PassengerArrivalProcess
from constants import *
from save_output import save_output
from performance_metrics import compute_performance_metrics

np.random.seed(1)
env = simpy.Environment()
logger = Logger(env=env, output_folder_path=LOG_PATH)
airport_security_control = AirportSecurityControl(env, logger)
passenger_arrival = PassengerArrivalProcess(env=env, 
                                            airport_security_control=airport_security_control, 
                                            logger=logger, 
                                            file_path=INPUT_PATH,
                                            pax_config=PAX_CONFIG)

# Execute!
env.run()
airport_security_control.calculate_total_system_time()
save_output(trackers=airport_security_control.trackers, output_path=OUTPUT_PATH)
compute_performance_metrics()