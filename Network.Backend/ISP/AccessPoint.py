
import json
from confluent_kafka import Producer, Consumer

class AccessPoint:
    def __init__(self, id, mb_available, bandwidth, latency, network_type, location, kafka_broker, isp_topic):
        self.id = id
        self.mb_available = mb_available
        self.bandwidth = bandwidth
        self.latency = latency
        self.network_type = network_type  # WiFi, 5G, LoRaWAN, etc.
        self.location = location  # Geographical or logical location
        self.kafka_broker = kafka_broker
        self.isp_topic = isp_topic  # Topic for communicating with the ISP

        self.producer = self.create_producer()
        self.consumer = self.create_consumer()

    def create_producer(self):
        config = {
            'bootstrap.servers': self.kafka_broker,
            'client.id': f'access_point_{self.id}'
        }
        return Producer(config)

    def create_consumer(self):
        config = {
            'bootstrap.servers': self.kafka_broker,
            'group.id': f'group_{self.id}',
            'auto.offset.reset': 'earliest'
        }
        consumer = Consumer(config)
        consumer.subscribe([f'access_point_{self.id}_messages', self.isp_topic])
        return consumer

    def send_message(self, message, target_id):
        topic = f'access_point_{target_id}_messages'
        self.producer.produce(topic, value=json.dumps(message).encode('utf-8'))
        self.producer.flush()
        print(f"Access Point {self.id} sent message to {target_id}: {message}")

    def request_bandwidth_increase(self, additional_bandwidth):
        message = {
            "request": "increase_bandwidth",
            "access_point_id": self.id,
            "additional_bandwidth": additional_bandwidth
        }
        self.producer.produce(self.isp_topic, value=json.dumps(message).encode('utf-8'))
        self.producer.flush()
        print(f"Access Point {self.id} requested {additional_bandwidth} Mbps bandwidth increase from ISP")

    def report_network_issue(self, issue_description):
        message = {
            "report": "network_issue",
            "access_point_id": self.id,
            "description": issue_description
        }
        self.producer.produce(self.isp_topic, value=json.dumps(message).encode('utf-8'))
        self.producer.flush()
        print(f"Access Point {self.id} reported network issue to ISP: {issue_description}")

    def consume_messages(self):
        try:
            while True:
                message = self.consumer.poll(1.0)
                if message is None:
                    continue
                if message.error():
                    print(f"Consumer error: {message.error()}")
                    continue

                received_message = json.loads(message.value().decode('utf-8'))
                print(f"Access Point {self.id} received message: {received_message}")
                self.handle_message(received_message)
        except KeyboardInterrupt:
            print("Consumer stopped.")
        finally:
            self.consumer.close()

    def handle_message(self, message):
        if "response" in message and message["response"] == "increase_bandwidth":
            self.update_bandwidth(message["new_bandwidth"])
        elif "response" in message and message["response"] == "network_issue_ack":
            print(f"ISP acknowledged network issue for Access Point {self.id}")
        else:
            print(f"Handling message at Access Point {self.id}: {message}")

    def can_provide_data(self, amount_mb):
        return self.mb_available >= amount_mb

    def update_bandwidth(self, new_bandwidth):
        self.bandwidth = new_bandwidth
        print(f"Access Point {self.id} updated bandwidth to {self.bandwidth} Mbps")

    def update_latency(self, new_latency):
        self.latency = new_latency
        print(f"Access Point {self.id} updated latency to {self.latency} ms")

    def get_status(self):
        return {
            "id": self.id,
            "network_type": self.network_type,
            "location": self.location,
            "mb_available": self.mb_available,
            "bandwidth": self.bandwidth,
            "latency": self.latency
        }
