import os
import django

# Step 1: Set the DJANGO_SETTINGS_MODULE environment variable
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "isp_management_api.settings")

# Step 2: Initialize Django
django.setup()

# Step 3: Import your functions after setting up Django
from Network.NetworkPoint import seed_network_nodes
from ISP.Device import simulate_device_traffic
from GNN.GNN import train_model

# Now you can call your functions

#train_model()

seed_network_nodes()
simulate_device_traffic("Kathmandu")
simulate_device_traffic("Janakpur")
simulate_device_traffic("Gandaki")