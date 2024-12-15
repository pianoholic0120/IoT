import paho.mqtt.client as mqtt

# MQTT settings
broker_address = "172.20.10.2"  # Replace with broker's IP or hostname
topic = "hello/group1"  # Topic to subscribe to

# Callback function for when a message is received
def on_message(client, userdata, msg):
    latest_data = msg.payload.decode("utf-8")
    print(f"Received latest air quality data: {latest_data}")

# Create MQTT client and set callback
client = mqtt.Client()
client.on_message = on_message

# Connect to broker
client.connect(broker_address)

# Subscribe to the topic
client.subscribe(topic)

# Start the MQTT loop
print("Waiting for latest air quality data...")
client.loop_forever()
