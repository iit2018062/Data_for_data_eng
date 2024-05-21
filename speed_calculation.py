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
filename = '/Users/manishakumari/Desktop/Data_for_data_eng/final_csv/2024-05-20.csv'  # Update with your CSV filename
df = pd.read_csv(filename)

# Handle missing values and convert columns to appropriate types
df['EVENT_NO_TRIP'] = df['EVENT_NO_TRIP'].astype(str)
df['EVENT_NO_STOP'] = df['EVENT_NO_STOP'].astype(str)
df['OPD_DATE'] = df['OPD_DATE'].astype(str)
df['VEHICLE_ID'] = pd.to_numeric(df['VEHICLE_ID'], errors='coerce').fillna(0).astype(int)
df['METERS'] = pd.to_numeric(df['METERS'], errors='coerce').fillna(0)
df['ACT_TIME'] = pd.to_numeric(df['ACT_TIME'], errors='coerce').fillna(0)
df['GPS_LONGITUDE'] = pd.to_numeric(df['GPS_LONGITUDE'], errors='coerce').fillna(0)
df['GPS_LATITUDE'] = pd.to_numeric(df['GPS_LATITUDE'], errors='coerce').fillna(0)
df['GPS_SATELLITES'] = pd.to_numeric(df['GPS_SATELLITES'], errors='coerce').fillna(0)
df['GPS_HDOP'] = pd.to_numeric(df['GPS_HDOP'], errors='coerce').fillna(0)

# Calculate speed
df_with_speed = calculate_speed(df)

# Write to new CSV file with speed column
output_filename = '/Users/manishakumari/Desktop/Data_for_data_eng/final_csv/2024-05-20.csv'
df_with_speed.to_csv(output_filename, index=False)

print(f"DataFrame with speed column written to '{output_filename}'.")
