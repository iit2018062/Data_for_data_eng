import csv
from datetime import datetime
import os
# Function to convert timestamp format
# Function to convert timestamp format
# Function to convert timestamp format
def convert_timestamp(timestamp_str):
    if timestamp_str:
        return datetime.strptime(timestamp_str, '%Y-%m-%d %H:%M:%S').strftime('%Y-%m-%d %H:%M:%S')
    else:
        return ''  # Return an empty string if timestamp is empty
# Function to update CSV file
# Function to update CSV file
def update_csv(file_path):
    with open(file_path, 'r+', newline='') as file:
        reader = csv.DictReader(file)
        fieldnames = reader.fieldnames
        rows = list(reader)
        file.seek(0)
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()

        for row in rows:
            if row['tstamp']:
                row['tstamp'] = convert_timestamp(row['tstamp'])
                writer.writerow(row)

# List of filenames to update
filenames = ['2024-04-12.csv', '2024-04-13.csv', '2024-04-14.csv'
             , '2024-04-15.csv', '2024-04-20.csv', '2024-04-21.csv',
             '2024-04-21.csv', '2024-04-22.csv', '2024-04-23.csv',
             '2024-04-24.csv', '2024-04-25.csv', '2024-04-26.csv',
             '2024-04-27.csv', '2024-04-28.csv', '2024-04-30.csv',
             '2024-05-02.csv', '2024-05-03.csv', '2024-05-04.csv',
             '2024-05-05.csv', '2024-05-06.csv', '2024-05-07.csv',
             '2024-05-08.csv', '2024-05-09.csv', '2024-05-10.csv',
             '2024-05-11.csv', '2024-05-12.csv', '2024-05-12.csv',
             '2024-05-13.csv', '2024-05-14.csv', '2024-05-15.csv',
             '2024-05-16.csv', '2024-05-18.csv','2024-05-19.csv']  # Add more filenames if needed

base_dir = '/Users/manishakumari/Desktop/Data_for_data_eng/final_csv/'

# Update each file in the list
for filename in filenames:
    file_path = os.path.join(base_dir, filename)
    update_csv(file_path)