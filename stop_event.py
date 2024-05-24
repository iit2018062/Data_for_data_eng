import csv
import json
import logging
import requests
import threading
from bs4 import BeautifulSoup
from typing import Dict, Any, List

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Set to store processed vehicle IDs
processed_vehicle_ids = set()
all_events = []  # List to store events for all vehicles

def chunk_list(lst, chunk_size):
    for i in range(0, len(lst), chunk_size):
        yield lst[i: i + chunk_size]

def get_response_details(vehicle_num: str) -> (int, List[Dict[str, Any]]):
    """Fetches stop events data for a specific vehicle number from the bus data API.

    Args:
        vehicle_num (str): The number of the vehicle.

    Returns:
        tuple: A tuple containing the HTTP status code and the list of parsed event data.
    """
    url = f"https://busdata.cs.pdx.edu/api/getStopEvents?vehicle_num={vehicle_num}"
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise exception for non-2xx responses

        soup = BeautifulSoup(response.content, 'html.parser')

        # Extract date and PDX_TRIP information
        date_info = soup.find('h1').get_text().split()[-1]
        trip_info = soup.find('h2').get_text().split()[-1]

        # Extract all tables
        tables = soup.find_all('table')
        events = []

        for table in tables:
            # Extract table rows
            rows = table.find_all('tr')

            # Extract table headers
            headers = [header.get_text() for header in rows[0].find_all('th')]
            headers.extend(['Date', 'PDX_TRIP'])  # Add additional columns for date and PDX_TRIP

            # Write data to events (skipping the first row which contains headers)
            for row in rows[1:]:
                data = [td.get_text() for td in row.find_all('td')]
                data.extend([date_info, trip_info])
                events.append(dict(zip(headers, data)))

        return response.status_code, events
    except requests.RequestException as e:
        logger.error(f"Error fetching data for vehicle number {vehicle_num}: {e}")
        return None, None

def save_to_csv(events: List[Dict[str, Any]]):
    """Saves the event data to a CSV file.

    Args:
        events (List[Dict[str, Any]]): The list of event data.
    """
    if not events:
        return

    csv_filename = "all_vehicles_events.csv"
    fieldnames = events[0].keys()

    try:
        with open(csv_filename, mode='w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(events)
        logger.info(f"Saved all events to {csv_filename}")
    except IOError as e:
        logger.error(f"Error saving data to CSV: {e}")

def process_vehicle(vehicle_num: str):
    if vehicle_num in processed_vehicle_ids:
        logger.info(
            f"Data for vehicle number {vehicle_num} has already been processed. Skipping."
        )
        return

    status_code, content = get_response_details(vehicle_num)
    if status_code == 200 and content:
        logger.info(f"Vehicle number: {vehicle_num}, Response Status: {status_code}")
        all_events.extend(content)
        processed_vehicle_ids.add(vehicle_num)  # Mark vehicle number as processed
    else:
        logger.warning(
            f"Failed to fetch data for vehicle number {vehicle_num}. Status Code: {status_code}"
        )

def main():
    # Define the list of vehicle numbers
    vehicle_nums = [
        'x', '3137', '3513', '3905', '3220', '3415', '3157', '3732', '3543', '4035', '3924', '3540', '3227',
        '4237', '4039', '3247', '3166', '3209', '3722', '3950', '3925', '3512', '3956', '3560', '2909', '2933',
        '3235', '3261', '3556', '4050', '3241', '3749', '3154', '3959', '3149', '3143', '3237', '3017', '2910',
        '3511', '3571', '3954', '4516', '3055', '3625', '3907', '4518', '3946', '3729', '3634', '3952', '3918',
        '3527', '3728', '3410', '3719', '3254', '3516', '3508', '3928', '3028', '3707', '4525', '3549', '3741',
        '4001', '3529', '3915', '3322', '3040', '2926', '3510', '3943', '3957', '3562', '3702', '3039', '3648',
        '3909', '3505', '3226', '3134', '3216', '3120', '3020', '3620', '4028', '2908', '3731', '3320', '3401',
        '3617', '3101', '3921', '4522', '2901', '3727', '3605', '3746', '4210'
    ]

    if not vehicle_nums:
        logger.warning("No vehicle numbers found in the list.")
        return

    threads = []
    for vehicle_num in vehicle_nums:
        thread = threading.Thread(target=process_vehicle, args=(vehicle_num,))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    # Save all collected events to a single CSV file
    save_to_csv(all_events)

if __name__ == "__main__":
    main()
