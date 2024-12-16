import os
import csv
from datetime import datetime
from publisher import Publisher
from receiver import Receiver

DATA_FOLDER = "./air_quality/"
current_station = "Da'an"  

def handle_message(msg):
    global current_station  

    if msg.isalpha(): 
        current_station = msg
        print(f"Updated current station to: {current_station}")
        return

    if is_number(msg):
        pm25_value = msg.strip()
        print(f"Received PM2.5 value: {pm25_value} for station: {current_station}")
        handle_realtime_data(current_station, pm25_value)
        return

    if "," in msg:
        parts = msg.split(",", 1)
        if len(parts) == 2:
            station_name = parts[0].strip()
            pm25_value = parts[1].strip()
            current_station = station_name if station_name else "Da'an"
            print(f"Updated station to {current_station} and received PM2.5: {pm25_value}")
            handle_realtime_data(current_station, pm25_value)
            return

def handle_realtime_data(station_name, pm25_value):
    if not os.path.exists(DATA_FOLDER):
        os.makedirs(DATA_FOLDER)

    file_path = os.path.join(DATA_FOLDER, f"{station_name}.csv")
    file_exists = os.path.exists(file_path)

    now = datetime.now().strftime("%Y/%m/%d %H:%M")
    aqi = "N/A"
    with open(file_path, "a", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        if not file_exists:
            writer.writerow(["Station", "Date", "AQI", "PM2.5"])
        writer.writerow([station_name, now, aqi, pm25_value])

    print(f"Data saved for {station_name}: PM2.5 = {pm25_value}")
    pub.send_message(f"Data for {station_name} updated: {pm25_value}")

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

if __name__ == "__main__":
    pub = Publisher()
    receiver = Receiver(on_message_callback=handle_message)
    print("Main program running... Waiting for messages.")
    receiver.start()
