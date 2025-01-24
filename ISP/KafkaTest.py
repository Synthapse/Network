from confluent_kafka import Consumer, KafkaException, KafkaError

# Configuration for the consumer
conf = {
    'bootstrap.servers': 'localhost:9092',  # Kafka broker address
    'group.id': 'my-consumer-group',        # Consumer group ID
    'auto.offset.reset': 'earliest'         # Start from the beginning if no offset is saved
}

# Create Consumer instance
consumer = Consumer(conf)

# Subscribe to the topic
consumer.subscribe(['test-topic'])

try:
    while True:
        # Poll for a message
        msg = consumer.poll(timeout=1.0)

        if msg is None:
            # No message available within timeout
            continue
        if msg.error():
            # Error in fetching message
            if msg.error().code() == KafkaError._PARTITION_EOF:
                print('End of partition reached {0}/{1}'.format(msg.topic(), msg.partition()))
            else:
                raise KafkaException(msg.error())
        else:
            # Successfully received message
            print(f"Received message: {msg.value().decode('utf-8')}")

except KeyboardInterrupt:
    print("Consuming interrupted")

finally:
    # Close consumer gracefully
    consumer.close()