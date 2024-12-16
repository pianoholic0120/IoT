import os
import csv
from datetime import datetime
from publisher import Publisher
from receiver import Receiver

DATA_FOLDER = "./air_quality/"

def handle_message(msg):
    if msg == "Zhongzheng" or msg == "Nangang":
        file_path = os.path.join(DATA_FOLDER, f"{msg}.csv")
        last_line = read_last_line(file_path)
        if last_line:
            pub.send_message(last_line)
        # else:
        #     pub.send_message("No data")
        return

    if "," in msg:
        parts = msg.split(",", 1)
        if len(parts) == 2:
            station_name = parts[0].strip()
            pm25_value = parts[1].strip()
            if station_name == "":
                station_name = "Da'an"
        else:
            station_name = ",".join(parts[:-1]).strip() or "Da'an"
            pm25_value = parts[-1].strip()
        
        handle_realtime_data(station_name, pm25_value)
    else:
        if is_number(msg):
            station_name = "Da'an"
            pm25_value = msg
            handle_realtime_data(station_name, pm25_value)
        else:
            station_name = msg
            file_path = os.path.join(DATA_FOLDER, f"{station_name}.csv")
            last_line = read_last_line(file_path)
            if last_line:
                pub.send_message(last_line)
            # else:
            #     pub.send_message("No data")

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

    pub.send_message(f"Data for {station_name} updated: {pm25_value}")

def read_last_line(file_path):
    if not os.path.exists(file_path):
        return None
    with open(file_path, "r", encoding="utf-8") as f:
        lines = f.readlines()
    if len(lines) > 1:
        return lines[-1].strip()
    else:
        return None

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