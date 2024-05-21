import csv

def rename_and_validate_speed(csv_file):
    # Define column name mapping
    column_mapping = {
        'TIMESTAMP': 'tstamp',
        'GPS_LATITUDE': 'latitude',
        'GPS_LONGITUDE': 'longitude',
        'SPEED': 'speed',
        'VEHICLE_ID': 'vehicle_id',
        'EVENT_NO_TRIP': 'trip_id'
    }

    # Read the CSV file, rename columns, and keep only specified fields
    with open(csv_file, 'r', newline='') as file:
        reader = csv.DictReader(file)
        fieldnames = [column_mapping.get(col, None) for col in reader.fieldnames]
        fieldnames = [field for field in fieldnames if field is not None]
        rows = [{column_mapping.get(key, None): value for key, value in row.items() if key in column_mapping} for row in reader]

    # Validate and modify the 'SPEED' column
    for row in rows:
        if 'speed' in row and not row['speed']:  # Check if 'speed' column exists and has no value
            row['speed'] = '0'  # Add '0' if no value found

    # Write back to the CSV file
    with open(csv_file, 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

# Example usage
csv_file = '/Users/manishakumari/Desktop/Data_for_data_eng/final_csv/2024-05-20.csv'  # Replace 'example.csv' with your CSV file location
rename_and_validate_speed(csv_file)
