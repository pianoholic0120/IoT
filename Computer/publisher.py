import paho.mqtt.client as mqtt

# MQTT settings
broker_address = "172.20.10.2"  # Replace with broker's IP or hostname
topic = "hello/group1"  # Topic to publish to

# File containing air quality data (replace with actual file path)
file_path = "./air_quality/combined.csv"  # File with air quality data (e.g., CSV or plain text)

# Function to read the last line of a file
def read_last_line(file_path):
    with open(file_path, "r") as file:
        lines = file.readlines()
        if lines:
            return lines[-1].strip()  # Return the last line
        else:
            return None

# Callback function for MQTT connection
def on_connect(client, userdata, flags, rc):
    print(f"Connected to broker with result code {rc}")
    send_latest_data(client)

# Function to send the latest air quality data
def send_latest_data(client):
    last_data = read_last_line(file_path)
    if last_data:
        print(f"Sending latest data: {last_data}")
        client.publish(topic, last_data)
    else:
        print("No data to send.")

# Create MQTT client and set callback
client = mqtt.Client()
client.on_connect = on_connect

# Connect to broker
client.connect(broker_address)

# Start MQTT loop to maintain connection
client.loop_start()

# Send latest data periodically (e.g., every 10 seconds)
import time
while True:
    send_latest_data(client)
    time.sleep(10)  # Adjust the time interval as needed
