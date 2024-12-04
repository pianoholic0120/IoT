import os
import pandas as pd

def interpolate_timestamps(folder_path):
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
                    print(f"File {file_name} does not contain 'timestamp' or 'heart_rate'. Skipping...")
            except Exception as e:
                print(f"Could not read file {file_name}. Error: {e}")

    if not data_list:
        print("No valid CSV files found. Exiting...")
        return

    # Combine all valid data
    merged_data = pd.concat(data_list, ignore_index=True)

    # Convert 'timestamp' to datetime format
    merged_data['timestamp'] = pd.to_datetime(merged_data['timestamp'], errors='coerce')

    # Keep original order
    merged_data.reset_index(drop=True, inplace=True)

    # Create a mask for valid timestamps
    valid_timestamp_mask = merged_data['timestamp'].notna()
    total_rows = len(merged_data)

    # Initialize processed data list
    processed_rows = []

    idx = 0
    while idx < total_rows:
        if valid_timestamp_mask[idx]:
            # Current row has a valid timestamp
            processed_rows.append(merged_data.loc[idx])
            idx += 1
        else:
            # Current row is missing a timestamp, collect all consecutive missing rows
            start_idx = idx
            while idx < total_rows and not valid_timestamp_mask[idx]:
                idx += 1
            end_idx = idx  # idx now points to the next row with a valid timestamp or the end of the data

            # Get the previous valid timestamp
            prev_valid_idx = start_idx - 1
            while prev_valid_idx >= 0 and not valid_timestamp_mask[prev_valid_idx]:
                prev_valid_idx -= 1
            timestamp1 = merged_data.loc[prev_valid_idx, 'timestamp'] if prev_valid_idx >= 0 else None

            # Get the next valid timestamp
            timestamp2 = merged_data.loc[idx, 'timestamp'] if idx < total_rows and valid_timestamp_mask[idx] else None

            num_missing_rows = end_idx - start_idx

            if timestamp1 is not None and timestamp2 is not None:
                # Interpolation possible
                time_delta = (timestamp2 - timestamp1) / (num_missing_rows + 1)
                for i in range(num_missing_rows):
                    if i == 0:
                        # Assign timestamp1 to the first heart_rate in the range
                        interpolated_timestamp = timestamp1
                    else:
                        interpolated_timestamp = timestamp1 + time_delta * i
                    row = merged_data.loc[start_idx + i].copy()
                    row['timestamp'] = interpolated_timestamp
                    processed_rows.append(row)
            elif timestamp1 is not None:
                # No next timestamp, assign timestamp1 to all rows
                for i in range(num_missing_rows):
                    row = merged_data.loc[start_idx + i].copy()
                    row['timestamp'] = timestamp1
                    processed_rows.append(row)
            elif timestamp2 is not None:
                # No previous timestamp, assign timestamp2 to all rows
                for i in range(num_missing_rows):
                    row = merged_data.loc[start_idx + i].copy()
                    row['timestamp'] = timestamp2
                    processed_rows.append(row)
            else:
                # No valid timestamps available, skip these rows
                print(f"Rows from index {start_idx} to {end_idx - 1} have no valid timestamps. Skipping...")
                continue

    # Convert processed data back to DataFrame
    final_data_df = pd.DataFrame(processed_rows)

    # Remove rows without 'heart_rate'
    final_data_df = final_data_df.dropna(subset=['heart_rate'])

    # Format 'timestamp' to "YYYY-MM-DD HH:MM:SS"
    final_data_df['timestamp'] = final_data_df['timestamp'].dt.strftime('%Y-%m-%d %H:%M:%S')

    # Sort by 'timestamp'
    final_data_df = final_data_df.sort_values(by='timestamp').reset_index(drop=True)

    # Output the result
    output_path = os.path.join(folder_path, 'merged_and_sorted_with_filled_timestamps.csv')
    final_data_df.to_csv(output_path, index=False)
    print(f"Combination, interpolation, and sorting completed. The result has been saved at {output_path}")

if __name__ == "__main__":
    folder_path = input("Please enter the directory containing the CSV files: ").strip()
    interpolate_timestamps(folder_path)