import geopandas as gpd
import networkx as nx
from geopy.distance import geodesic
import matplotlib.pyplot as plt

# Load shapefile
gdf = gpd.read_file("kenya_towns/ke_major-towns.shp")

# Create a graph
G = nx.Graph()

# Add nodes (towns)
for index, row in gdf.iterrows():
    town_name = row["TOWN_NAME"]
    lon, lat = row["geometry"].x, row["geometry"].y  # Ensure correct order
    G.add_node(town_name, pos=(lon, lat))

# Add edges based on distance
towns = gdf[["TOWN_NAME", "geometry"]].values

for i in range(len(towns)):
    for j in range(i + 1, len(towns)):
        town1, point1 = towns[i]
        town2, point2 = towns[j]

        coord1 = (point1.y, point1.x)  # Ensure order (latitude, longitude)
        coord2 = (point2.y, point2.x)

        try:
            distance = geodesic(coord1, coord2).kilometers  # Compute distance
            if distance < 200:  # Threshold distance
                G.add_edge(town1, town2, weight=distance)
        except ValueError as e:
            print(f"Error with {town1} - {town2}: {e}")

# Plot the graph
plt.figure(figsize=(10, 8))
pos = nx.get_node_attributes(G, 'pos')
nx.draw(G, pos, with_labels=True, node_size=300, node_color="skyblue", edge_color="gray")
plt.title("Kenya Major Towns Network Graph")
plt.show()
plt.savefig("kenya_towns.png")
