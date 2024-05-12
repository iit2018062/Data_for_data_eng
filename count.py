import json
import os

def count_arrays_and_size_in_json_files(root_dir):
    directory_info = {}
    total_array_count = 0
    total_size_kb = 0

    for subdir, _, files in os.walk(root_dir):
        directory_size = 0
        file_array_counts = {}
        for file_name in files:
            if file_name.endswith('.json'):
                file_path = os.path.join(subdir, file_name)
                with open(file_path, "r") as json_file:
                    try:
                        data = json.load(json_file)
                    except json.JSONDecodeError as e:
                        print(f"Error reading JSON file {file_path}: {e}")
                        continue

                    array_count = len(data) if isinstance(data, list) else 0
                    total_array_count += array_count  # Adding to total array count
                    file_array_counts[file_path] = array_count
                    # Calculate file size
                    file_size = os.path.getsize(file_path)
                    directory_size += file_size
                    total_size_kb += file_size / 1024  # Adding to total size in KB
        directory_info[subdir] = {'array_counts': file_array_counts, 'size': directory_size}

    return directory_info, total_array_count, total_size_kb

if __name__ == "__main__":
    root_dir = "/Users/manishakumari/Desktop/Data_for_data_eng/Data/2024-05-12"
    directory_info, total_array_count, total_size_kb = count_arrays_and_size_in_json_files(root_dir)

    for directory, info in directory_info.items():
        array_counts = info['array_counts']
        directory_size = info['size']
        print(f"Directory: {directory}, Total Size: {directory_size} bytes")
        for file_path, array_count in array_counts.items():
            print(f"\tFile: {file_path}, Array Count: {array_count}")

    print("\nTotal Array Count for All Files:", total_array_count)
    print("Total Size of All Files (KB):", total_size_kb)