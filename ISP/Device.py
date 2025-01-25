from confluent_kafka import Producer, Consumer, KafkaError
import time
import json
from concurrent.futures import ThreadPoolExecutor
import signal
import threading

kafka_broker_address = "localhost:9092"

class UserDevice:
    def __init__(self, id, name, interface_type, parent_node, producer):
        self.id = id
        self.name = name
        self.interface_type = interface_type
        self.parent_node = parent_node
        self.producer = producer
        self.available_mb = 0

    def send_data_claim(self, amount_mb):
        topic = f'node_{self.parent_node}_messages'
        message = {
            "device_id": self.id,
            "amount_mb": amount_mb,
        }
        self.producer.produce(topic, value=json.dumps(message).encode('utf-8'))

    def start_sending_claims(self):
        while True:
            self.send_data_claim(20)
            time.sleep(5)  # Simulate sending data every 5 seconds

    def listen_for_responses(self, consumer):

        while True:
            message = consumer.poll(1.0)
            if message is None:
                continue
            if message.error():
                print(f"Consumer error: {message.error()}")
                continue
            response = json.loads(message.value().decode('utf-8'))
            print(f"Received response: {response}")
            granted_mb = response["data_granted_mb"]
            self.available_mb += granted_mb


def consume_messages_in_thread(node, consumer):
    """Runs consume_messages in a separate thread."""
    node.listen_for_responses(consumer)

def simulate_device_traffic():
    producer = Producer({'bootstrap.servers': kafka_broker_address})
    consumer = Consumer({
        'bootstrap.servers': kafka_broker_address,
        'group.id': 'shared_consumer_group',
        'auto.offset.reset': 'earliest'
    })

    print("Start simulating")

    devices = [
        UserDevice(
            id=str(i),
            name=f"device{i}",
            interface_type="Ethernet" if i % 2 == 0 else "Wi-Fi",
            parent_node="Kathmandu",
            producer=producer,
        )
        for i in range(0, 4)
    ]

    threads = []

    node_1_thread = threading.Thread(target=consume_messages_in_thread, args=(devices[0], consumer))
    node_2_thread = threading.Thread(target=consume_messages_in_thread, args=(devices[1], consumer))
    node_3_thread = threading.Thread(target=consume_messages_in_thread, args=(devices[2], consumer))
    node_4_thread = threading.Thread(target=consume_messages_in_thread, args=(devices[3], consumer))

    node_1_thread.start()
    node_2_thread.start()
    node_3_thread.start()
    node_4_thread.start()

    for i in range (0,4):
        devices[0].send_data_claim(20)
        devices[1].send_data_claim(20)
        devices[2].send_data_claim(20)
        devices[3].send_data_claim(20)

if __name__ == "__main__":
    simulate_device_traffic()
