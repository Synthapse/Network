from torch_geometric.utils import from_networkx
import torch
from Graph.graph_generator import generate_nepal_graph
import random
import torch.nn.functional as F
from torch_geometric.nn import GCNConv
from torch_geometric.loader import DataLoader
import matplotlib.pyplot as plt
import networkx as nx

import torch_geometric

# Convert the NetworkX graph to a PyTorch Geometric graph

nepal_graph = generate_nepal_graph()

data = from_networkx(nepal_graph)

num_nodes = data.num_nodes
data.x = torch.eye(num_nodes)

print(data)
# Data(edge_index=[2, 434], num_nodes=217, x=[217, 217])

#The graph has 217 nodes. (217 Access points (routers) - in 3 lvl hierarchy


# for definition

# Current load (amount of data)
# Capacity - Maximum Data the node can handle
# Latency requirements

# random for now - its necessary some historical data (and well designed modeling)
num_nodes = data.num_nodes
features = torch.tensor(
    [[random.uniform(0, 1), random.uniform(0, 1)] for _ in range(num_nodes)])

# Example features: [load, capacity]

data.x = features

# target bandwidth allocation
# home WI-FI: 20 or 40 MHz

data.y = torch.tensor([random.uniform(0, 1) for _ in range(num_nodes)])  # Example: Bandwidth target


# Internet Maximum bandwidth 100 Mbps, using 50 Mbps (50%)


# Equally:
# Total bandwidth: 100 Mbps
#  100 / 217 = 0.46Mbps per node

# 10 000 GB per month
# 333.33 GB per day
# 13.89 GB per hour

# Data per node
# 46 GB/ month
# 1.54 GB//day
# 64 MB/ hour

class BandwidthGNN(torch.nn.Module):
    def __init__(self, input_dim, hidden_dim, output_dim):
        super().__init__()
        self.conv1 = GCNConv(input_dim, hidden_dim)
        self.conv2 = GCNConv(hidden_dim, output_dim)

    def forward(self, data):
        x, edge_index = data.x, data.edge_index
        x = F.relu(self.conv1(x, edge_index))
        x = self.conv2(x, edge_index)
        return x

# Define the model
model = BandwidthGNN(input_dim=2, hidden_dim=16, output_dim=1)  # 2 input features -> 1 output prediction
optimizer = torch.optim.Adam(model.parameters(), lr=0.01)
loss_fn = torch.nn.MSELoss()

# Training loop
model.train()
for epoch in range(100):
    optimizer.zero_grad()
    out = model(data)
    loss = loss_fn(out, data.y.unsqueeze(1))  # Match output to labels
    loss.backward()
    optimizer.step()
    print(f"Epoch {epoch+1}, Loss: {loss.item():.4f}")



model.eval()
predictions = model(data)
print("Predicted Bandwidth Allocations:", predictions)
# Features: The information provided in the textbook (inputs to learn from).
# Labels: The answers at the back of the book (targets to match during training).


# prediction usage - based on monthly data.