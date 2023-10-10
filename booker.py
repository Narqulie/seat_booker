import requests
from datetime import datetime
import logging
import os
import json
import tkinter as tk
from tkinter import messagebox

home_dir = os.path.dirname(os.path.abspath(__file__))

# Logging: #
log_to_terminal = True
# Define the logging format
log_format = '%(asctime)s %(levelname)s %(message)s'

# File handler
logfile_path = os.path.join(home_dir, "booker.log")
file_handler = logging.FileHandler(logfile_path)
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(logging.Formatter(log_format))

# Add the file handler
root_logger = logging.getLogger()
root_logger.setLevel(logging.INFO)
root_logger.addHandler(file_handler)

# Stream handler (if log_to_terminal is True)
if log_to_terminal:
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(logging.Formatter(log_format))
    root_logger.addHandler(stream_handler)


# Variable setup:
today = datetime.today().strftime("%Y-%m-%dT07:45:00%z")
logging.info(f"Today: {today}")
end_of_today = datetime.today().strftime("%Y-%m-%dT16:30:00%z")
logging.info(f"End of today: {end_of_today}")


# Class to store configuration:
class Configuration:
    def __init__(self, floor, seat, cookie):
        self.floor = floor
        self.seat = seat
        self.cookie = cookie


# Read config.json and return the values:
def load_config():
    try:
        with open(os.path.join(home_dir, "config.json"), "r") as config_file:
            data = json.load(config_file)
            logging.info("Config file read successfully")
            logging.info(f"Floor: {data['floor']}, Seat: {data['seat']}")
            return Configuration(data["floor"], data["seat"], data["cookie"])
    except Exception as e:
        logging.error(f"Failed to read config.json: {e}")
        return None


def display_error(message):
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    messagebox.showerror("Error", message)
    root.destroy()


# Function to reserve a spot:
def reserve_spot(cookie, floor, spot):
    url = "https://worksense.optimaze.net/api/v1/workstationreservations"
    headers = {
        "cookie": cookie
        }
    data = {
        "floorId": floor,
        "capacityObjectId": spot,
        "startTime": today,
        "endTime": end_of_today,
        "isPrivate": False
    }

    logging.info(f"Sending request: {data}")
    try:
        response = requests.post(url, headers=headers, json=data)
    except Exception as e:
        logging.error(f"Failed to send request: {e}")
        return

    logging.info(f"Response: {response.status_code}")

    if response.status_code == 200:
        logging.info("Seat succesfully booked")
        display_error("Seat succesfully booked")
    elif response.status_code == 401:
        logging.error("Unauthorized, check your cookies")
        display_error(f"Booking failed, status code:{response.status_code}"
                      f"\n response: {response.text}")
    else:
        logging.error("Failed to book seat, status code:"
                      f"{response.status_code}, response: {response.text}")
        display_error(f"Booking failed, status code:{response.status_code}\n"
                      f"response: {response.text}")


# Run the script:
if __name__ == "__main__":
    config = load_config()
    if config:
        reserve_spot(config.cookie, config.floor, config.seat)
    else:
        logging.error("Configuration missing. Exiting.")
