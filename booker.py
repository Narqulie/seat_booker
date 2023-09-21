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

# Read config.json for cookie, floor and seat:
with open("config.json", "r") as config_file:
    config = json.load(config_file)
    my_floor = config["floor"]
    my_seat = config["seat"]
    cookie = config["cookie"]


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
    response = requests.post(url, headers=headers, json=data)
    logging.info(f"Response: {response.status_code}")

    if response.status_code == 200:
        logging.info("Seat succesfully booked")
    if response.status_code == 401:
        logging.error("Unauthorized, check your cookies")

    else:
        logging.error("Failed to book seat, status code:"
                      f"{response.status_code}, response: {response.text}")


# Run the script:
if __name__ == "__main__":
    reserve_spot(cookie, my_floor, my_seat)
