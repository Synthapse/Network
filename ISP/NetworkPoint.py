import traceback
from GNN.Graph.graph_generator import generate_nepal_graph

class NetworkPoint:
    def __init__(self, data_usage, bandwidth, latency):
        """
        Initialize the NetworkPoint with essential properties.

        :param data_usage: Amount of data used by this node (e.g., in GB).
        :param bandwidth: The available bandwidth (e.g., in Mbps).
        :param latency: Latency to neighbors (e.g., in ms).
        """

        # redefine if those data per node is ok
        self.data_usage = data_usage  # Data usage in GB
        self.bandwidth = bandwidth  # Bandwidth in Mbps
        self.latency = latency  # Latency in ms
        self.neighbors = []  # List of neighbors (to be managed by NetworkX graph)

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
    for node_id in G.nodes():
        # Here you can decide how to assign properties (e.g., based on node_id or other logic)
        data_usage = 50  # Example data usage in GB
        bandwidth = 100  # Example bandwidth in Mbps
        latency = 10  # Example latency in ms

        # Create a NetworkPoint instance and store it in the node's 'data' attribute
        G.nodes[node_id]['data'] = NetworkPoint(data_usage, bandwidth, latency)
    # Now define neighbors based on the edges in the graph
    for node_id in G.nodes():
        node_data = G.nodes[node_id]['data']
        # For each edge, add the connected node as a neighbor
        for neighbor_id in G.neighbors(node_id):
            neighbor_data = G.nodes[neighbor_id]['data']
            node_data.add_neighbor(neighbor_data)


# Example Usage:
# Create a NetworkX graph with nodes and edges (this would be the imported graph in real use)

def display_node_details(nepal_graph):
    # Iterate through all nodes in the graph
    for node_id in nepal_graph.nodes:
        # Ensure the 'data' attribute exists for the node
        if 'data' in nepal_graph.nodes[node_id]:
            node_data = nepal_graph.nodes[node_id]['data']
            print(f"Node {node_id} Info: {node_data.get_info()}")
        else:
            print(f"Node {node_id} has no data!")

def seed_network_nodes():
    try:
        nepal_graph = generate_nepal_graph()

        # Add properties to the graph's nodes
        add_properties_to_existing_graph(nepal_graph)

        # Display the details of all nodes
        display_node_details(nepal_graph)


    except Exception as ex:
        # Print a detailed error message along with the stack trace
        print(f"An error occurred: {ex}")
        # Print the detailed traceback
        traceback.print_exc()