import json

# Function to validate breadcrumb
def validate_breadcrumb_1(breadcrumb):
    if "GPS_LATITUDE" not in breadcrumb or "GPS_LONGITUDE" not in breadcrumb:
        return False
    return True
def validate_breadcrumb_2(breadcrumb):
    if "OPD_DATE" not in breadcrumb:
        return False
    return True
# Read JSON file and validate individual breadcrumbs
with open('/Users/manishakumari/Documents/Data_for_data_eng/Data/2024-04-11/2901.json', 'r') as file:
    data = json.load(file)
    for index, breadcrumb in enumerate(data):
        if not validate_breadcrumb_1(breadcrumb):
            print(f"Validation failed for breadcrumb {index + 1}: Missing latitude or longitude coordinates.")
            print("Breadcrumb Data:", breadcrumb)
        if not validate_breadcrumb_2(breadcrumb):
            print(f"Validation failed for breadcrumb {index + 1}: Missing timestamp.")
            print("Breadcrumb Data:", breadcrumb)
