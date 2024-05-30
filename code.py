import os
import csv
import pandas as pd
import requests
from datetime import datetime
import json

def get_vehicle_ids_from_csv(filename, column_name):
    df = pd.read_csv(filename)
    vehicle_ids = df[column_name].tolist()
    return vehicle_ids

def get_response_details(vehicle_id):
    url = f"https://busdata.cs.pdx.edu/api/getBreadCrumbs?vehicle_id={vehicle_id}"
    try:
        response = requests.get(url)
        response.raise_for_status()  # This will raise an HTTPError for bad responses
        try:
            content = response.json()
        except json.JSONDecodeError:
            print(f"Vehicle ID: {vehicle_id} - Response content is not in JSON format")
            content = None
    except requests.exceptions.RequestException as e:
        print(f"Vehicle ID: {vehicle_id} - Request failed: {e}")
        content = None
        response = None

    return response.status_code if response else None, content

def save_to_file(vehicle_id, content, status_code):
    today_date = datetime.now().strftime('%Y-%m-%d')
    directory = f'Data/{today_date}'
    if not os.path.exists(directory):
        os.makedirs(directory)
    filename = os.path.join(directory, f"{vehicle_id}.json")

    if content and status_code == 200:
        with open(filename, 'w') as jsonfile:
            json.dump(content, jsonfile, indent=4)
        print(f"Data for Vehicle ID {vehicle_id} saved to file: {filename}")
    else:
        print(f"Data for Vehicle ID {vehicle_id} not saved. Status code: {status_code}")

# Example usage:
filename = 'vehicle_ids - Sheet1.csv'
column_name = 'Giggles'  # Replace with your actual column name
vehicle_ids = get_vehicle_ids_from_csv(filename, column_name)

for vehicle_id in vehicle_ids:
    status_code, content = get_response_details(vehicle_id)
    print(f"Vehicle ID: {vehicle_id}, Response Status: {status_code}")
    print("Response Content:")
    print(content)
    save_to_file(vehicle_id, content, status_code)
    print()
