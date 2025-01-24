import traceback
from GNN.Graph.graph_generator import generate_nepal_graph
from confluent_kafka import Producer, Consumer, KafkaError

#Producer: This sends messages to a Kafka topic.
# Consumer: This receives messages from a Kafka topic.

kafka_broker_address = "localhost:9092"

# Each node can be a Kafka producer (sending messages) and consumer (receiving messages)
class NetworkPoint:
    def __init__(self, id, data_usage, bandwidth, latency):
        """
        Initialize the NetworkPoint with essential properties.

        :param data_usage: Amount of data used by this node (e.g., in GB).
        :param bandwidth: The available bandwidth (e.g., in Mbps).
        :param latency: Latency to neighbors (e.g., in ms).
        """


        self.id = id
        # redefine if those data per node is ok
        self.data_usage = data_usage  # Data usage in GB
        self.bandwidth = bandwidth  # Bandwidth in Mbps
        self.latency = latency  # Latency in ms
        self.neighbors = []  # List of neighbors (to be managed by NetworkX graph)

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

    def create_consumer(self):
        """Create a Kafka consumer for the node."""
        config = {
            'bootstrap.servers': kafka_broker_address,  # Change to your Kafka broker address
            'group.id': f'group_{self.id}',
            'auto.offset.reset': 'earliest'
        }
        consumer = Consumer(config)
        consumer.subscribe([f'node_{self.id}_messages'])  # Subscribe to its own topic
        print(f"Added Kafka consumer with id {self.id}")
        return consumer

    def send_message(self, message, neighbor_id):
        """Send a message to a specific neighbor via Kafka."""
        topic = f'node_{neighbor_id}_messages'  # Kafka topic for the neighbor
        self.producer.produce(topic, value=message)
        self.producer.flush()
        print(f"Node {self.id} sent message to Node {neighbor_id}: {message}")

    def consume_messages(self):
        """Consume messages from Kafka for this node."""
        while True:
            msg = self.consumer.poll(timeout=1.0)  # Adjust timeout as needed
            if msg is None:
                continue
            if msg.error():
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    continue
                else:
                    print(f"Consumer error: {msg.error()}")
                    break
            else:
                print(f"Node {self.id} received message: {msg.value().decode('utf-8')}")

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
        return f"Data Usage = {self.data_usage} GB, Bandwidth = {self.bandwidth} Mbps, " \
               f"Latency = {self.latency} ms, Neighbors = {len(self.neighbors)}"

    def update_usage(self, additional_usage):
        """
        Update the data usage for this node.

        :param additional_usage: Amount of additional data used by the node (e.g., in GB).
        """
        self.data_usage += additional_usage


# Function to add properties to the nodes of an existing NetworkX graph
def add_properties_to_existing_graph(G):
    """
    Add data usage, bandwidth, and latency properties to each node of the existing graph.

    :param G: The NetworkX graph to update.
    """
    # Iterate through each node and add properties (e.g., random values for this example)
    for id in G.nodes():
        # Here you can decide how to assign properties (e.g., based on id or other logic)
        data_usage = 50  # Example data usage in GB
        bandwidth = 100  # Example bandwidth in Mbps
        latency = 10  # Example latency in ms

        # Create a NetworkPoint instance and store it in the node's 'data' attribute
        G.nodes[id]['data'] = NetworkPoint(id, data_usage, bandwidth, latency)

    # Now define neighbors based on the edges in the graph
    for id in G.nodes():
        node_data = G.nodes[id]['data']
        # For each edge, add the connected node as a neighbor
        for neighbor_id in G.neighbors(id):
            neighbor_data = G.nodes[neighbor_id]['data']
            node_data.add_neighbor(neighbor_data)


def seed_network_nodes():
    try:
        nepal_graph = generate_nepal_graph()

        # Add properties to the graph's nodes
        add_properties_to_existing_graph(nepal_graph)

        # Display the details of all nodes
        # Sending messages

        nodes = nepal_graph.nodes.items()

        # Print all nodes and their data
        for node_id, node_data in nodes:
            print(f"Node ID: {node_id}")
            print(f"Node Data: {node_data}")
            if 'data' in node_data:
                print(f"Data Usage: {node_data['data'].data_usage} GB")
                print(f"Bandwidth: {node_data['data'].bandwidth} Mbps")
                print(f"Latency: {node_data['data'].latency} ms")
            print("---------")


        # Get Country Capital -> Kathmandu

        node_1 = nepal_graph.nodes['Kathmandu']

        for neighbor in node_1['data'].neighbors:
            print(f"Sending message to {neighbor}")
            node_1['data'].send_message("Hello, neighbor!", neighbor.id)

        node_1['data'].consume_messages()



    except Exception as ex:
        # Print a detailed error message along with the stack trace
        print(f"An error occurred: {ex}")
        # Print the detailed traceback
        traceback.print_exc()