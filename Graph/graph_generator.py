
# This class generate the potential graph representation of Nepal geospatial
# 7 provinces, which are connected
# There are 3 level of hierarchy
#  a) Top Level (Province)
#  b) Intermediate Level (Cities, societal places)
#  c) Leaf Level (Schools, Villages)

import networkx as nx
import matplotlib.pyplot as plt

# Create a graph
G = nx.Graph()

# Top Level: Add provinces
provinces = ["Arun", "Janakpur", "Kathmandu", "Gandaki", "Kapilavastu", "Karnali", "Mahakali"]
G.add_nodes_from(provinces)

# Connect provinces (example connections, modify as needed for real representation)
province_connections = [
    ("Arun", "Janakpur"),
    ("Janakpur", "Kathmandu"),
    ("Kathmandu", "Gandaki"),
    ("Gandaki", "Kapilavastu"),
    ("Kapilavastu", "Karnali"),
    ("Karnali", "Mahakali"),
    ("Mahakali", "Arun")
]


G.add_edges_from(province_connections)

# Intermediate Level: Add cities/societal places for each province
cities = {
    "Arun": ["A1", "A2", "A3", "A4", "A5"],
    "Janakpur": ["B1", "B2", "B3", "B4", "B5"],
    "Kathmandu": ["C1", "C2", "C3", "C4", "C5"],
    "Gandaki": ["D1", "D2", "D3", "D4", "D5"],
    "Kapilavastu": ["E1", "E2", "E3", "E4", "E5"],
    "Karnali": ["F1", "F2", "F3", "F4", "F5"],
    "Mahakali": ["G1", "G2", "G3", "G4", "G5"]
}

# Add provinces and cities to the graph
for province, city_list in cities.items():
    G.add_node(province)  # Add province as a node
    for city in city_list:
        G.add_node(city)  # Add city as a node
        G.add_edge(province, city)  # Connect province to its cities

# Leaf Level: Add 5 points (schools/villages) for each city
schools_villages = {}

# Generate 5 points for each city dynamically
for province, city_list in cities.items():
    for city in city_list:
        schools_villages[city] = [
            f"{city}_Point1",
            f"{city}_Point2",
            f"{city}_Point3",
            f"{city}_Point4",
            f"{city}_Point5",
        ]

# Add schools and villages to the graph
for city, leaf_nodes in schools_villages.items():
    for leaf_node in leaf_nodes:
        G.add_node(leaf_node)  # Add school or village as a node
        G.add_edge(city, leaf_node)  # Connect city to its schools/villages
# Print the graph's nodes and edges
print("Nodes:", G.nodes())
print("Edges:", G.edges())


# Draw the graph
plt.figure(figsize=(25, 15))  # Set the figure size

nx.draw(G, with_labels=True)
# Save the graph to a PNG file
plt.savefig("graph.png")  # Save as a PNG file
plt.close()  # Close the figure to free resources