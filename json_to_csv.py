import os
import json
import csv

def convert_json_to_csv(json_directory, csv_directory):
    # Ensure the JSON directory exists
    if not os.path.isdir(json_directory):
        print(f"The directory {json_directory} does not exist.")
        return

    # Ensure the CSV directory exists
    if not os.path.exists(csv_directory):
        os.makedirs(csv_directory)

    # Get the name of the directory containing JSON files
    directory_name = os.path.basename(json_directory)

    # Define the path for the output CSV file
    csv_file_path = os.path.join(csv_directory, f"{directory_name}.csv")

    # List to store data from JSON files
    data_list = []
    # Set to store all possible fieldnames
    fieldnames_set = set()

    # Read each JSON file in the directory
    for filename in os.listdir(json_directory):
        if filename.endswith(".json"):
            json_file_path = os.path.join(json_directory, filename)
            with open(json_file_path, 'r') as json_file:
                data = json.load(json_file)

                if isinstance(data, list):
                    data_list.extend(data)  # Append all items if data is a list
                else:
                    data_list.append(data)  # Append the item if data is a single dictionary

    # If there are no JSON files, inform the user and exit
    if not data_list:
        print(f"No JSON files found in {json_directory}.")
        return

    # Collect all unique fieldnames
    for data in data_list:
        fieldnames_set.update(data.keys())

    # Convert the set to a sorted list
    fieldnames = sorted(fieldnames_set)

    # Write data to CSV file
    with open(csv_file_path, 'w', newline='') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        for data in data_list:
            writer.writerow(data)

    print(f"CSV file has been created at {csv_file_path}")

# Example usage
json_directory_path ="/Users/manishakumari/Desktop/Data_for_data_eng/Data/2024-05-18" # Replace with your JSON directory path
csv_directory_path = "/Users/manishakumari/Desktop/Data_for_data_eng/CSV"  # Replace with your desired CSV directory path

convert_json_to_csv(json_directory_path, csv_directory_path)
