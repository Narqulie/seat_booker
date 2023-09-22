import requests
from datetime import datetime
import logging
import os
import json

home_dir = os.path.dirname(os.path.abspath(__file__))
logfile_path = os.path.join(home_dir, "booker.log")

# Logging setup:
logging.basicConfig(filename=logfile_path,
                    level=logging.INFO,
                    format='%(asctime)s %(levelname)s %(message)s')

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
    elif response.status_code == 401:
        logging.error("Unauthorized, check your cookies")
    else:
        logging.error("Failed to book seat, status code:"
                      f"{response.status_code}, response: {response.text}")


# Run the script:
if __name__ == "__main__":
    config = load_config()
    if config:
        reserve_spot(config.cookie, config.floor, config.seat)
    else:
        logging.error("Configuration missing. Exiting.")
