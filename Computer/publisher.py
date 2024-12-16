import paho.mqtt.client as mqtt

broker_address = "192.168.0.197"  
publish_topic = "hello/group1/pc2rpi"  

class Publisher:
    def __init__(self, broker=broker_address, topic=publish_topic):
        self.client = mqtt.Client()
        self.client.connect(broker)
        self.client.loop_start()
        self.topic = topic

    def send_message(self, msg):
        self.client.publish(self.topic, msg)
        print(f"Published message to {self.topic}: {msg}")