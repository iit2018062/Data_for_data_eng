import os
import json

def get_value_ranges(directory):
    value_ranges = {}
    files_processed = 0

    # Loop through each file in the directory
    for filename in os.listdir(directory):
        filepath = os.path.join(directory, filename)

        # Check if the file is a JSON file
        if filename.endswith('.json'):
            with open(filepath, 'r') as file:
                try:
                    data = json.load(file)
                    files_processed += 1

                    # Handle both list and dictionary types
                    if isinstance(data, list):
                        for item in data:
                            update_value_ranges(value_ranges, item)
                    elif isinstance(data, dict):
                        update_value_ranges(value_ranges, data)
                    else:
                        print(f"Ignored unsupported JSON format in file: {filepath}")
                except json.JSONDecodeError:
                    print(f"Error decoding JSON in file: {filepath}")

    if files_processed == 0:
        print("No JSON files found in the directory.")
    else:
        print("Value ranges for each key:")
        for key, range_info in value_ranges.items():
            print(f"{key}: {range_info['min']} - {range_info['max']}")

def update_value_ranges(value_ranges, data):
    # Update value ranges for each key
    for key, value in data.items():
        if isinstance(value, (int, float)):
            if key not in value_ranges:
                value_ranges[key] = {'min': value, 'max': value}
            else:
                value_ranges[key]['min'] = min(value_ranges[key]['min'], value)
                value_ranges[key]['max'] = max(value_ranges[key]['max'], value)

# Example usage:
directory_path = "/Users/manishakumari/Desktop/Data_for_data_eng/Data/2024-05-12"  # Change this to your directory path
get_value_ranges(directory_path)
