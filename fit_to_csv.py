import os
import csv
from fitparse import FitFile

def convert_fit_to_csv_dynamic(directory):
    """
    Converts all .fit files in the specified directory to .csv files
    with dynamically generated headers based on the fields in each .fit file.
    
    :param directory: Path to the folder containing .fit files
    """
    if not os.path.exists(directory):
        print(f"Error: The directory '{directory}' does not exist.")
        return

    fit_files = [f for f in os.listdir(directory) if f.endswith('.fit')]

    if not fit_files:
        print("No .fit files found in the specified directory.")
        return

    for fit_file in fit_files:
        fit_path = os.path.join(directory, fit_file)
        csv_file_name = os.path.splitext(fit_file)[0] + '.csv'
        csv_path = os.path.join(directory, csv_file_name)

        try:
            fit = FitFile(fit_path)

            headers = set()
            records = []

            for record in fit.get_messages():
                record_data = {}
                for record_field in record:
                    headers.add(record_field.name)
                    record_data[record_field.name] = record_field.value
                records.append(record_data)

            headers = sorted(headers)

            with open(csv_path, mode='w', newline='') as csv_file:
                csv_writer = csv.DictWriter(csv_file, fieldnames=headers)
                csv_writer.writeheader() 
                for record in records:
                    csv_writer.writerow(record)  

            print(f"Converted: {fit_file} -> {csv_file_name}")
        except Exception as e:
            print(f"Failed to convert {fit_file}: {e}")

if __name__ == "__main__":
    print("Welcome to the .fit to .csv converter!")
    directory = input("Please enter the path to the directory containing .fit files: ").strip()
    if os.path.isdir(directory):
        print(f"Processing files in: {directory}")
        convert_fit_to_csv_dynamic(directory)
    else:
        print(f"Error: '{directory}' is not a valid directory. Please try again.")