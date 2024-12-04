import os
import pandas as pd

def merge_and_sort_csv_with_timestamp_assignment():
    folder_path = input("Choose the directory containing files to merge: ").strip()

    if not folder_path or not os.path.exists(folder_path):
        print("Invalid directory. Exiting...")
        return

    data_list = []

    for file_name in os.listdir(folder_path):
        if file_name.endswith('.csv'):
            file_path = os.path.join(folder_path, file_name)
            try:
                df = pd.read_csv(file_path)

                if 'timestamp' in df.columns and 'heart_rate' in df.columns:
                    data_list.append(df[['timestamp', 'heart_rate']])
                else:
                    print(f"File {file_name} lacks 'timestamp' or 'heart_rate', skipping...")
            except Exception as e:
                print(f"Can't read file {file_name}, Error: {e}")

    if not data_list:
        print("No valid csv files found. Exiting...")
        return

    # Combine all valid data
    merged_data = pd.concat(data_list, ignore_index=True)

    # Convert 'timestamp' to datetime and sort
    merged_data['timestamp'] = pd.to_datetime(merged_data['timestamp'], errors='coerce')
    merged_data = merged_data.sort_values(by='timestamp')

    # Assign missing timestamps for rows with valid heart_rate
    filled_data = []
    last_valid_timestamp = None

    for index, row in merged_data.iterrows():
        if pd.notnull(row['timestamp']):
            last_valid_timestamp = row['timestamp']
            filled_data.append(row)
        elif pd.notnull(row['heart_rate']) and last_valid_timestamp is not None:
            # Assign a timestamp by incrementing the last valid timestamp
            last_valid_timestamp += pd.Timedelta(minutes=1)
            filled_row = row.copy()
            filled_row['timestamp'] = last_valid_timestamp
            filled_data.append(filled_row)

    # Convert back to DataFrame
    filled_data = pd.DataFrame(filled_data)

    # Remove rows that do not have both 'timestamp' and 'heart_rate'
    filled_data = filled_data.dropna(subset=['timestamp', 'heart_rate'])

    # Output the merged and cleaned data
    output_path = os.path.join(folder_path, 'merged_and_sorted_with_filled_timestamps.csv')
    filled_data.to_csv(output_path, index=False)
    print(f"Combination, sorting, and cleaning are finished. The result has been saved at {output_path}")

if __name__ == "__main__":
    merge_and_sort_csv_with_timestamp_assignment()