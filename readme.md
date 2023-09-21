# Seat Booker Script

This Python script allows you to automatically reserve a seat in an office environment using the provided `reserve_spot` function.

## Description

The script utilizes the `requests` library to send a POST request to the `worksense.optimaze.net` website for workstation reservation. It uses a predefined cookie and booking details such as the floor ID, spot ID, and the reservation time. 

Booking details and other information are logged to a file named `booker.log` located in the same directory as the script.

## Requirements

- Python 3.x
- `requests` library (`pip install requests`)

## Usage

1. Set the cookie value in the `cookie` variable.
2. Set your desired floor ID in the `my_floor` variable and spot ID in the `my_seat` variable.
3. Run the script:
   ```
   python <script_name>.py
   ```
4. Check the `booker.log` file for logging information about the booking process.

## Functionality

- Automatically logs the date and booking details.
- Sends a POST request to reserve a spot.
- Logs the response status from the server.
- Handles different response scenarios (successful booking, unauthorized, or any other unexpected responses).

## Important Note

Ensure your cookie value is up to date, as expired or incorrect cookies will result in an unauthorized error (HTTP 401).
