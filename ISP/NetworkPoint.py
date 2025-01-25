import traceback
from GNN.Graph.graph_generator import generate_nepal_graph
from confluent_kafka import Producer, Consumer, KafkaError
import json
from ISP.NetworkPlan import NetworkProvider
import re
import threading

# Needs to improve that Kafka - cause seems - like there is too much consumers/producers
# probbaby not well solution

#Producer: This sends messages to a Kafka topic.
# Consumer: This receives messages from a Kafka topic.


kafka_broker_address = "localhost:9092"

# maybe transformed to differentiate proper topics and consumers (I, II or III level node or maybe device)
def is_valid_json(message_value):
    """Check if a string is valid JSON."""
    try:
        return json.loads(message_value)
    except json.JSONDecodeError:
        return None

# Each node can be a Kafka producer (sending messages) and consumer (receiving messages)
class NetworkPoint:
    def __init__(self, id, mb_usage_last_quarter, mb_available, bandwidth, latency, is_5g_enabled=False):
        """
        Initialize the NetworkPoint with essential properties.

        :param mb_usage_last_quarter: Amount of data used by this node (e.g., in GB).
        :param bandwidth: The available bandwidth (e.g., in Mbps).
        :param latency: Latency to neighbors (e.g., in ms).
        """

        self.id = id
        # redefine if those data per node is ok
        self.mb_usage_last_quarter = mb_usage_last_quarter  # Data usage in MB (usage)
        self.mb_available = mb_available
        self.bandwidth = bandwidth  # Bandwidth in Mbps
        self.latency = latency  # Latency in ms
        self.neighbors = []  # List of neighbors (to be managed by NetworkX graph)

        self.is_5g_enabled = is_5g_enabled
        if self.is_5g_enabled:
            self.bandwidth = 10000  # Example: 10 Gbps for 5G-enabled node
            self.latency = 1  # Example: 1 ms latency for 5G-enabled node

        self.producer = self.create_producer()
        self.consumer = self.create_consumer()

    def create_producer(self):
        """Create a Kafka producer for the node."""
        config = {
            'bootstrap.servers': kafka_broker_address,  # Change to your Kafka broker address
            'client.id': f'node_{self.id}'
        }
        print(f"Added Kafka producer with id {self.id}")
        return Producer(config)

    def can_provide_data(self, amount_mb):
        """Decision logic to evaluate the claim."""
        # Example: Total available bandwidth in MB
        # (It's depends on the network)
        return amount_mb <= self.mb_available


    def create_consumer(self):
        """Create a Kafka consumer for the node."""
        config = {
            'bootstrap.servers': kafka_broker_address,  # Change to your Kafka broker address
            'group.id': f'group_{self.id}',
            'auto.offset.reset': 'earliest'
        }
        consumer = Consumer(config)

        topic = f'node_{self.id}_messages'
        consumer.subscribe([topic])  # Subscribe to its own topic
        print(f"Added Kafka consumer with id {self.id}")
        return consumer

    def send_message(self, message, neighbor_id):
        """Send a message to a specific neighbor via Kafka."""
        topic = f'node_{neighbor_id}_messages'  # Kafka topic for the neighbor
        print(f"Node {self.id} sent message to Node {neighbor_id}: {message}")
        self.producer.produce(topic, value=message)
        self.producer.flush()

    # divide into 2 ways
    # consume from devices
    # consume from other nodes in the network
    def consume_messages(self):
        """Listen for claims and respond accordingly."""
        try:
            is_json = True
            json_message = None
            while True: # Continuous consumption loop
                message = self.consumer.poll(1.0)  # Poll messages with a timeout
                if message is None:
                    continue
                if message.error():
                    print(f"Consumer error: {message.error()}")
                    continue

                # Preprocess: Convert single quotes to double quotes for keys
                claim = message.value()
                if isinstance(claim, bytes):
                    message_value = claim.decode('utf-8')  # Decode bytes to string
                    try:
                        # Preprocess: Replace single quotes with double quotes
                        if message_value.startswith("{") and "'" in message_value:
                            message_value = message_value.replace("'", '"')

                        # Attempt to parse the JSON string
                        is_json = is_valid_json(message_value)

                        if is_json:
                            json_message = json.loads(message_value)
                        else:
                            json_message = message_value
                    except json.JSONDecodeError as e:
                        print(f"Failed to decode JSON: {e}")
                        print(f"Received invalid JSON string: {message_value}")
                print(f"Node {self.id} received claim: {json_message}")

                if is_json:
                    self.allocate_transfer_to_device(json_message)
                else:
                    print(f'Consumer received message: {json_message}')

        except KeyboardInterrupt:
            print("Consumer stopped.")
        finally:
            self.consumer.close()

    def allocate_transfer_to_device(self, json_message):
        # Evaluate the claim and prepare a response
        print("Decision Point - allocate data or not")
        if self.can_provide_data(json_message["amount_mb"]):

            self.mb_available -= json_message["amount_mb"]
            response = {
                "status": "approved",
                "node_id": self.id,
                "data_granted_mb": json_message["amount_mb"],
            }
        else:
            response = {
                "status": "denied",
                "node_id": self.id,
                "reason": "Insufficient resources"
            }

        # Send the response to the appropriate topic
        device_id = json_message["device_id"]
        response_topic = f'responses_{device_id}'
        self.producer.produce(response_topic, value=json.dumps(response).encode('utf-8'))
        self.producer.flush()
        print(f"Node {self.id} sent response: {response} to {response_topic} Transfer Left: {self.mb_available}")

    def add_neighbor(self, neighbor):
        """
        Add a neighboring node to this node.

        :param neighbor: A NetworkPoint object to add as a neighbor.
        """
        if neighbor not in self.neighbors:
            self.neighbors.append(neighbor)

    def get_info(self):
        """
        Get a summary of the node's properties.

        :return: A string summary of the node's properties.
        """
        return f"Data Usage = {self.mb_usage_last_quarter} MB, Available Data[MB] = {self.mb_available} Bandwidth = {self.bandwidth} Mbps, " \
               f"Latency = {self.latency} ms, Neighbors = {len(self.neighbors)}"

    def update_usage(self, additional_usage):
        """
        Update the data usage for this node.

        :param additional_usage: Amount of additional data used by the node (e.g., in GB).
        """
        self.mb_usage_last_quarter += additional_usage


# Function to add properties to the nodes of an existing NetworkX graph
def define_neighbors_tribes(G):
    """
    Add data usage, bandwidth, and latency properties to each node of the existing graph.
    :param G: The NetworkX graph to update.
    """
    # Iterate through each node and add properties (e.g., random values for this example)
    # Now define neighbors based on the edges in the graph
    for id in G.nodes():
        node_data = G.nodes[id]['data']
        # For each edge, add the connected node as a neighbor
        for neighbor_id in G.neighbors(id):
            neighbor_data = G.nodes[neighbor_id]['data']
            node_data.add_neighbor(neighbor_data)

def consume_messages_in_thread(node):
    """Runs consume_messages in a separate thread."""
    node['data'].consume_messages()

def send_messages_to_neighbors(node):
    """Send messages to the node's neighbors."""
    for neighbor in node['data'].neighbors:
        node['data'].send_message("I have transfer problem", neighbor.id)

def seed_network_nodes():
    try:
        # there are also another countries...
        nepal_graph = generate_nepal_graph()
        # Add properties to the graph's nodes
        network_provider = NetworkProvider()
        network_provider.charge_network(nepal_graph)
        # Extra load the: Kapilavastu (5th province) -> E3 point
        network_provider.charge_single_point(nepal_graph, "E3")
        define_neighbors_tribes(nepal_graph)



        # Display the details of all nodes
        # Sending messages

        nodes = nepal_graph.nodes.items()

        # Print all nodes and their data
        for node_id, node_data in nodes:
            print(f"Node ID: {node_id}")
            print(f"Node Data: {node_data}")
            if 'data' in node_data:
                print(f"Mb Available: {node_data['data'].mb_available} MB")
                print(f"Data usage: {node_data['data'].mb_usage_last_quarter} Mb usage last 15 minutes")
                print(f"Bandwidth: {node_data['data'].bandwidth} Mbps")
                print(f"Latency: {node_data['data'].latency} ms")
            print("---------")

        # producer-consumer pattern:

        # Get Country Capital -> Kathmandu
        node_1 = nepal_graph.nodes['Kathmandu']
        # Kathmandu communicates with Janakpur & Gandaki
        node_2 = nepal_graph.nodes['Janakpur']
        node_3 = nepal_graph.nodes['Gandaki']

        # Since consume_messages is a blocking call (it waits for messages)

        # Start consuming messages in separate threads for node_1, node_2, and node_3
        node_1_thread = threading.Thread(target=consume_messages_in_thread, args=(node_1,))
        node_2_thread = threading.Thread(target=consume_messages_in_thread, args=(node_2,))
        node_3_thread = threading.Thread(target=consume_messages_in_thread, args=(node_3,))

        # Start the threads
        node_1_thread.start()
        node_2_thread.start()
        node_3_thread.start()

        # Now, send messages to neighbors in the main thread
        send_messages_to_neighbors(node_1)
        send_messages_to_neighbors(node_2)
        send_messages_to_neighbors(node_3)

        # Optionally, you can wait for threads to complete if necessary (blocking call)
        #node_1_thread.join()
        #node_2_thread.join()
        #node_3_thread.join()


    except Exception as ex:
        # Print a detailed error message along with the stack trace
        print(f"An error occurred: {ex}")
        # Print the detailed traceback
        traceback.print_exc()