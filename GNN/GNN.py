from torch_geometric.utils import from_networkx
import torch
from GNN.Graph.graph_generator import generate_nepal_graph
import random
import torch.nn.functional as F
from torch_geometric.nn import GCNConv
from ISP.NetworkPlan import NetworkProvider
import h5py
from torch_geometric.loader import DataLoader
import matplotlib.pyplot as plt
import networkx as nx

# Internet Maximum bandwidth 100 Mbps, using 50 Mbps (50%)

#Yes, the Graph Neural Network (GNN) model you’ve built can be adapted to make
# predictions for each node for the next 15 minutes, but it would require a few
# adjustments to incorporate temporal data and make future predictions.


# Data(edge_index=[2, 434], num_nodes=217, x=[217, 217])

#The graph has 217 nodes. (217 Access points (routers) - in 3 lvl hierarchy

# Each node have:

# data_usage = 50  # Example data usage in GB
# bandwidth = 100  # Example bandwidth in Mbps
# latency = 10  # Example latency in ms
# for definition
# Current load (amount of data)
# Capacity - Maximum Data the node can handle
# Latency requirements
# Example features: [load, capacity]
# target bandwidth allocation
# home WI-FI: 20 or 40 MHz

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

import torch_geometric


def save_model_as_h5(model, file_path):
    # First, save the model as a PyTorch .pt or .pth file
    torch.save(model.state_dict(), 'model.pth')  # Save model state_dict

    # Convert .pth file to .h5 format
    # Load the model state_dict
    model_state_dict = torch.load('model.pth')

    # Create an HDF5 file
    with h5py.File(file_path, 'w') as f:
        for key, value in model_state_dict.items():
            # Store the model parameters as datasets in the HDF5 file
            f.create_dataset(key, data=value.numpy())

    print(f"Model saved to {file_path}")

# Convert the NetworkX graph to a PyTorch Geometric graph
class BandwidthGNNWithLSTM(torch.nn.Module):
    def __init__(self, input_dim, hidden_dim):
        super().__init__()
        self.conv1 = GCNConv(input_dim, hidden_dim)
        self.conv2 = GCNConv(hidden_dim, 16)  # Now output 16 features for LSTM
        self.lstm = torch.nn.LSTM(input_size=16, hidden_size=1, num_layers=2, batch_first=True)
        self.fc = torch.nn.Linear(1, 1)  # Output 1 value per node for prediction

    def forward(self, data):
        x, edge_index = data.x, data.edge_index
        x = F.relu(self.conv1(x, edge_index))
        x = self.conv2(x, edge_index)

        # Reshape for LSTM [batch_size, sequence_length, features]
        x = x.unsqueeze(0)  # Add batch dimension (shape: [1, num_nodes, output_dim])

        # Apply LSTM
        lstm_out, _ = self.lstm(x)  # LSTM output shape: [1, num_nodes, 32]

        # Use the last timestep output from the LSTM (shape: [num_nodes, 32])
        lstm_out = lstm_out.squeeze(0)  # Remove the batch dimension (shape: [num_nodes, 32])

        # Apply fully connected layer for prediction
        output = self.fc(lstm_out)  # Shape: [num_nodes, 1]

        return output


def train_model():
    nepal_graph = generate_nepal_graph()

    data = from_networkx(nepal_graph)

    network_provider = NetworkProvider()
    network_provider.charge_network(nepal_graph)

    targets = []
    num_nodes = data.num_nodes
    node_features = []
    for node in nepal_graph.nodes:
        # Example features; you should use the actual values here
        data_usage_last_quarter = nepal_graph.nodes[node]["data"].mb_usage_last_quarter  # in MB
        mb_usage_last_two_quarter = nepal_graph.nodes[node]["data"].mb_usage_last_two_quarter # in MB
        mb_usage_last_three_quarter = nepal_graph.nodes[node]["data"].mb_usage_last_three_quarter  # in Mbps

        # Simulate target usage for the next 15 minutes
        target_usage_next_15_min = random.uniform(10*1000, 100*1000)  # in MB
        # Create the feature vector for each node
        node_features.append([data_usage_last_quarter, mb_usage_last_two_quarter, mb_usage_last_three_quarter])
        targets.append(target_usage_next_15_min)

    # Convert to a tensor
    node_features_tensor = torch.tensor(node_features, dtype=torch.float)
    targets_tensor = torch.tensor(targets, dtype=torch.float)

    data.x = node_features_tensor
    data.y = targets_tensor

    # Normalize features and targets
    x_min = data.x.min(dim=0, keepdim=True)[0]
    x_max = data.x.max(dim=0, keepdim=True)[0]
    data.x = (data.x - x_min) / (x_max - x_min)

    y_min = data.y.min()
    y_max = data.y.max()
    data.y = (data.y - y_min) / (y_max - y_min)

    model = BandwidthGNNWithLSTM(input_dim=3, hidden_dim=16)  # Use 5 as input_dim to match data.x
    optimizer = torch.optim.Adam(model.parameters(), lr=0.001)
    loss_fn = torch.nn.MSELoss()


    model.train()
    for epoch in range(100):
        optimizer.zero_grad()
        out = model(data)
        loss = loss_fn(out, data.y.unsqueeze(1))  # Match output to labels for the next 15 minutes
        loss.backward()
        optimizer.step()
        print(f"Epoch {epoch + 1}, Loss: {loss.item():.4f}")

    model.eval()
    save_model_as_h5(model, 'model.h5')
    predictions = model(data)
    # Denormalize predictions
    predictions_denorm = predictions * (y_max - y_min) + y_min
    print("Predicted Data Usage for Next Quarter (15min) (MB):", predictions_denorm)

    # Visualization
    predictions_np = predictions_denorm.detach().cpu().numpy()
    targets_np = data.y.detach().cpu().numpy()

    plt.scatter(targets_np, predictions_np)
    plt.xlabel('Actual Data Usage (MB)')
    plt.ylabel('Predicted Data Usage (MB)')
    plt.title('Actual vs Predicted Data Usage')
    plt.show()
