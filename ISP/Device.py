# Mobile is just particular one person device -which gets data from NetworkPoint
from confluent_kafka import Producer, Consumer, KafkaError
import time
import json
import threading

kafka_broker_address = "localhost:9092"
class UserDevice:

    def __init__(self, id, name, interface_type, parent_node):
        self.id = id
        self.name = name  # Interface name (e.g., eth0, wlan0)
        self.interface_type = interface_type  # Ethernet, Wi-Fi, etc.
        self.parent_node = parent_node
        self.producer = Producer({'bootstrap.servers': kafka_broker_address})
        self.consumer = Consumer({
            'bootstrap.servers': kafka_broker_address,
            'group.id': f'group_{self.id}',
            'auto.offset.reset': 'earliest'
        })
        self.available_mb = 0
        self.response_topic = f'responses_{self.id}'


    def send_data_claim(self, amount_mb):
        topic = f'node_{self.parent_node}_messages'

        message = {
            "device_id": self.id,
            "amount_mb": amount_mb,
        }

        print(f"Node {self.id} sent message to Node {self.parent_node}: {message}")
        self.producer.produce(topic, value=json.dumps(message).encode('utf-8'))
        self.producer.flush()


    def start_sending_claims(self):
        """Periodically send claims every 1 minute."""
        self.send_data_claim(20)
        time.sleep(60)  # Wait for 1 minute before sending the next claim

    def listen_for_response(self):
        # Subscribe to the unique response topic
        self.consumer.subscribe([self.response_topic])
        print(f"Subscribed to topics: {self.consumer.subscription()}")

        while True:
            message = self.consumer.poll(1.0)
            if message is None:
                continue
            if message.error():
                print(f"Consumer error: {message.error()}")
                continue

        # look for network point decision
            response = json.loads(message.value().decode('utf-8'))
            print(f"Device {self.device_id} received response: {response}")

def simulate_device_traffic():
    devices = [
        UserDevice(
            id = "1",
            name="eth0",
            interface_type="Ethernet",
            parent_node ="Kathmandu"
        ),
        UserDevice(
            id = "2",
            name="wlan0",
            interface_type="Wi-Fi",
            parent_node = "Kathmandu",
        ),
        UserDevice(
            id = "3",
            name="lo",
            interface_type="Loopback",
            parent_node="Kathmandu",
        ),
        UserDevice(
            id = "4",
            name="vpn0",
            interface_type="VPN",
            parent_node="Kathmandu"
        )
    ]

    # Start the sending process for each device in a separate thread
    threads = []
    for device in devices:
        thread = threading.Thread(target=device.start_sending_claims)
        thread.start()
        threads.append(thread)

    # Join threads to keep the main process alive
    for thread in threads:
        thread.join()
