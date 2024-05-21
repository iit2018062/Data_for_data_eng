import os
import pandas as pd

def process_csv(input_csv, output_directory):
    # Read the CSV file with specifying dtype for the first column
    trip_data = pd.read_csv(input_csv, dtype={'trip_id': str})

    # Select only trip_id and vehicle_id columns
    trip_data_subset = trip_data[['trip_id', 'vehicle_id']]

    # Drop duplicate rows based on trip_id
    trip_data_subset = trip_data_subset.drop_duplicates(subset=['trip_id'])

    # Create the output directory if it doesn't exist
    os.makedirs(output_directory, exist_ok=True)

    # Save the processed data to a new CSV file in the output directory
    output_csv = os.path.join(output_directory, os.path.basename(input_csv))
    trip_data_subset.to_csv(output_csv, index=False)
    print(f"Processed data saved to '{output_csv}'.")

def main(csv_files, output_directory):
    for csv_file in csv_files:
        process_csv(csv_file, output_directory)

if __name__ == "__main__":
    # CSV files directory
    csv_files_directory = "/Users/manishakumari/Desktop/Data_for_data_eng/final_csv"

    # List CSV files in the directory
    csv_files = [os.path.join(csv_files_directory, f) for f in os.listdir(csv_files_directory) if f.endswith('.csv')]

    # Output directory
    output_directory = os.path.join(csv_files_directory, "trip")

    main(csv_files, output_directory)
