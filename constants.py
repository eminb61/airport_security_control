# Constants
SERVICE_MEAN_TRAY = 120  # seconds
SERVICE_MEAN_XRAY = 45
SERVICE_MEAN_BODYSCREEN = 15

NUM_CONTROL_AREAS = 5

# ------- OLD SYSTEM -------------
# TRAY_CAPACITY = 4 * 4 * NUM_CONTROL_AREAS # 80
# XRAY_CAPACITY = 2 * 4 * NUM_CONTROL_AREAS # 40
# BODYSCREEN_CAPACITY = 1 * 2 * NUM_CONTROL_AREAS # 10
# NUM_BODYSCREENS = 2 * NUM_CONTROL_AREAS # 10

# ---------------------------------
# NUM_TRAY_AREAS = 4 * NUM_CONTROL_AREAS
# NUM_XRAYS = 4 * NUM_CONTROL_AREAS
# NUM_BODYSCREENS = 2 * NUM_CONTROL_AREAS

# # TRAY_CAPACITY = 4 * NUM_TRAY_AREAS
# # XRAY_CAPACITY = 3 * NUM_XRAYS
# # BODYSCREEN_CAPACITY = 1 * NUM_BODYSCREENS
# ---------------------------------

# NEW SYSTEM
TRAY_CAPACITY = 8 * 4 * NUM_CONTROL_AREAS # 160
XRAY_CAPACITY = 2 * 4 * NUM_CONTROL_AREAS # 40
BODYSCREEN_CAPACITY = 1 * 3 * NUM_CONTROL_AREAS # 15
NUM_BODYSCREENS = 3 * NUM_CONTROL_AREAS # 15

# ---------------------------------
# # NUM_TRAY_AREAS = 4 * NUM_CONTROL_AREAS
# # NUM_XRAYS = 4 * NUM_CONTROL_AREAS
# # NUM_BODYSCREENS = 3 * NUM_CONTROL_AREAS

# # TRAY_CAPACITY = 8 * NUM_TRAY_AREAS
# # XRAY_CAPACITY = 3 * NUM_XRAYS
# # BODYSCREEN_CAPACITY = 1 * NUM_BODYSCREENS
# ---------------------------------

BODYSCREEN_WAITING_CAPACITY = 10 * NUM_BODYSCREENS
INPUT_PATH = None #'inputs/passenger_arrival_process.csv'
OUTPUT_PATH = '../outputs/'
LOG_PATH = '../logs/'
PAX_CONFIG = {
    'num_pax': 10800,
    'lambda': 1
}