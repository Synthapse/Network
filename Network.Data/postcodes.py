import pandas as pd
import time
import networkx as nx
import matplotlib.pyplot as plt
from geopy.geocoders import Nominatim
from geopy.distance import geodesic

print("Starting script...")

# Initialize geolocator
geolocator = Nominatim(user_agent="postcode_mapper")

# Initialize NetworkX graph
G = nx.Graph()

def get_coordinates(postcode):
    """Fetch latitude & longitude for a given postcode"""
    try:
        location = geolocator.geocode(postcode)
        if location:
            print(f"Postcode: {postcode} -> Lat: {location.latitude}, Lon: {location.longitude}")
            return location.latitude, location.longitude
    except Exception as e:
        print(f"Error fetching {postcode}: {e}")
    return None, None

print("Input file...")

# Load postcodes from CSV
input_file = "performance_postcode_files/202105_fixed_pc_performance_r01_AB.csv"
output_file = "postcode_coordinates.csv"

print("Reading DF...")

df = pd.read_csv(input_file)

# Limit number of records to process
num_records = 50
df_subset = df.loc[:num_records - 1, "postcode"]

# Fetch coordinates
coords = list(zip(*df_subset.apply(get_coordinates)))  
df.loc[:num_records - 1, "Latitude"] = coords[0]  
df.loc[:num_records - 1, "Longitude"] = coords[1]  

# Add nodes to NetworkX graph
for idx, row in df.loc[:num_records - 1].iterrows():
    if pd.notna(row["Latitude"]) and pd.notna(row["Longitude"]):
        G.add_node(row["postcode"], pos=(row["Longitude"], row["Latitude"]))  # Longitude first for plotting

# Connect nearby nodes (Optional: Based on distance threshold)
distance_threshold_km = 50  # Set max distance between connected nodes (adjust as needed)

postcodes = df.loc[:num_records - 1, ["postcode", "Latitude", "Longitude"]].dropna().values
for i in range(len(postcodes)):
    for j in range(i + 1, len(postcodes)):
        loc1 = (postcodes[i][1], postcodes[i][2])
        loc2 = (postcodes[j][1], postcodes[j][2])
        distance = geodesic(loc1, loc2).km  # Calculate real-world distance in km
        if distance < distance_threshold_km:
            G.add_edge(postcodes[i][0], postcodes[j][0], weight=distance)

# Plot the graph based on real-world coordinates
plt.figure(figsize=(8, 6))

# Extract positions
pos = nx.get_node_attributes(G, "pos")

# Draw graph with real-world latitude and longitude
nx.draw(G, pos, with_labels=True, node_size=500, node_color="skyblue", edge_color="gray", font_size=8, font_weight="bold")

plt.xlabel("Longitude")
plt.ylabel("Latitude")
plt.title("Postcode Network Based on Location")
plt.grid()
plt.show()

# Save results
df.to_csv(output_file, index=False)
print(f"Saved coordinates to {output_file}")
