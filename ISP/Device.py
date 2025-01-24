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
        self.producer = Producer({
                'bootstrap.servers': kafka_broker_address,
                'client.id': f'device_{self.id}'
             })
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
        time.sleep(5)  # Wait for 5 sec before sending the next claim

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
    devices = []

    # Create 1000 devices (which comunicate with single node...)
    for i in range(1, 1001):

        id = i
        device = UserDevice(
            id=str(id),  # Device id is a string of the form "1", "2", ..., "1000"
            name=f"device{i}",  # Dynamic name like "device1", "device2", ..., "device1000"
            interface_type="Ethernet" if i % 2 == 0 else "Wi-Fi",  # Alternate between Ethernet and Wi-Fi
            parent_node="Kathmandu"
        )
        devices.append(device)

    print(devices)
    # Start the sending process for each device in a separate thread
    threads = []
    threads = []
    for device in devices:
        thread = threading.Thread(target=device.start_sending_claims)
        thread.daemon = True  # Make the thread a daemon so it doesn't block the main program exit
        thread.start()
        threads.append(thread)

    # Instead of joining threads here, just keep the program alive.
    while True:
        time.sleep(60)  # The main thread will sleep forever so that all threads keep running