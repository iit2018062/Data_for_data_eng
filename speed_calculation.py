import pandas as pd
from datetime import datetime

def calculate_speed(df):
    # Calculate TIMESTAMP
    df['TIMESTAMP'] = pd.to_datetime(df['OPD_DATE'], errors='coerce', format='%d%b%Y:%H:%M:%S') + pd.to_timedelta(df['ACT_TIME'], unit='s')

    # Calculate dMETERS and dTIMESTAMP
    df['dMETERS'] = df.groupby(['VEHICLE_ID'])['METERS'].diff()
    df['dTIMESTAMP'] = df.groupby(['VEHICLE_ID'])['TIMESTAMP'].diff()

    # Calculate SPEED
    df['SPEED'] = df['dMETERS'] / df['dTIMESTAMP'].dt.total_seconds()

    # Drop intermediate columns
    df = df.drop(columns=['dMETERS', 'dTIMESTAMP'])

    return df

# Read CSV data
filename = '/Users/manishakumari/Desktop/Data_for_data_eng/Data/2024-05-18/2024-05-18.csv'  # Update with your CSV filename
df = pd.read_csv(filename)

# Calculate speed
df_with_speed = calculate_speed(df)

# Write to new CSV file with speed column
output_filename = '/Users/manishakumari/Desktop/Data_for_data_eng/Data/2024-05-18/2024-05-18_speed.csv'
df_with_speed.to_csv(output_filename, index=False)

print(f"DataFrame with speed column written to '{output_filename}'.")
