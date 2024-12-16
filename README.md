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

# Arduino codes with GP2Y10 data sending to Raspberry Pi 
* using SERIAL_PORT = /dev/ttyACM0
* verify and compile the Arduino code first under the path **./Arduino_pm2.5/Arduino_pm2.5.ino**
* connecting Arduino and Raspberry Pi using usb cable

## Prerequisites

    pip3 install paho-mqtt


## i. Execute the following code on computer

    cd ./Computer/
    python3 main.py

## ii. Send the location to the computer through MQTT with Raspberry Pi

The computer will locate the location and either fetch the data from the backend if available or appending the given data from Raspberry Pi to its database.

    mosquitto_pub -h <your ip(inet)> -d -t hello/group1/rpi2pc -m "<your location>" 

for instance, 

    mosquitto_pub -h 127.0.0.1 -d -t hello/group1/rpi2pc -m "Taipei" 
the procedure is optional, if not provided, the location will utilize Da'an as default.

## iii. Execute the following code on Raspberry Pi

    python3 rpi_pm25_to_pc.py
this will obtain the data from Arduino and send it to the northbound with the computer backend
