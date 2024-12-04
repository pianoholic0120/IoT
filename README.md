# Virtual Environment

    source ./final/bin/activate

# Converting Garmin FIT to CSV 

First, install `fitparse`

    sudo pip3 install fitparse

Then you can execute 

    python3 fit_to_csv.py

This will create a bunch of CSVs for all of your workouts in that directory (You will be asked to enter the directory in terminal after running fit_to_csv.py). The files will be stored in the directory you designate. 

# Parsing data from Garmin Account Management

Execute

    python3 parse_and_sort_data.py

This will create a csv file, 'merged_and_sorted_with_filled_timestamps.csv',containing the corresponding data (heart_rate and timestamp) from csv files in the user-designated directory. The parsed file contains two columns, heart_rate and timestamp, where the data is presented in sequence following the timestamp chronologically.