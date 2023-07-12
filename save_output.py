from utils.helpers import save_tracker_dicts

def save_output(trackers, output_path):
    save_tracker_dicts(trackers, output_path)


# import csv

# class SaveOutput:
#     def __init__(self):
#         pass

#     def save_dict_to_csv(self, dict_data, filename):
#         with open(filename, mode='w', newline='') as file:
#             writer = csv.writer(file)
#             for key, value in dict_data.items():
#                 writer.writerow([key, value])
