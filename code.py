import os
import json
import pandas as pd
import requests
from datetime import datetime

def get_vehicle_ids_from_csv(filename, column_name):
    df = pd.read_csv(filename)
    vehicle_ids = df[column_name].tolist()
    return vehicle_ids

def get_response_details(vehicle_id):
    url = f"https://busdata.cs.pdx.edu/api/getBreadCrumbs?vehicle_id={vehicle_id}"
    response = requests.get(url)
    status_code = response.status_code
    content = response.json()
    return status_code, content

def save_to_file(vehicle_id, content):
    today_date = datetime.now().strftime('%Y-%m-%d')
    directory = f'Data/{today_date}'
    if not os.path.exists(directory):
        os.makedirs(directory)
    filename = os.path.join(directory, f"{vehicle_id}.json")
    with open(filename, 'w') as f:
        json.dump(content, f, indent=4)

# Example usage:
filename = 'vehicle_ids - Sheet1.csv'
column_name = 'Giggles'  # Replace with your actual column name
vehicle_ids = get_vehicle_ids_from_csv(filename, column_name)

for vehicle_id in vehicle_ids:
    status_code, content = get_response_details(vehicle_id)
    print(f"Vehicle ID: {vehicle_id}, Response Status: {status_code}")
    print("Response Content:")
    print(content)
    save_to_file(vehicle_id, content)
    print("Data saved to file.\n")
