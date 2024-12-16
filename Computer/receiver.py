import paho.mqtt.client as mqtt

broker_address = "192.168.0.197"  
subscribe_topic = "hello/group1/rpi2pc" 

class Receiver:
    def __init__(self, broker=broker_address, topic=subscribe_topic, on_message_callback=None):
        self.client = mqtt.Client()
        self.on_message_callback = on_message_callback
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.connect(broker)
        self.client.subscribe(topic)

    def on_connect(self, client, userdata, flags, rc):
        print("Receiver connected to broker with result code:", rc)

    def on_message(self, client, userdata, msg):
        data = msg.payload.decode("utf-8")
        print(f"Received message from {msg.topic}: {data}")
        if self.on_message_callback:
            self.on_message_callback(data)

    def start(self):
        self.client.loop_forever()
