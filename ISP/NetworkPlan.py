from django.db import models
import random

class ServicePlanManagement(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('canceled', 'Canceled'),
    ]

    plan_name = models.CharField(max_length=200, default="Basic Plan")
    speed = models.PositiveIntegerField(help_text="Speed in Mbps")
    data_limit = models.PositiveIntegerField(help_text="Data limit in GB")
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(max_length=200, null=False, blank=True)
    status = models.CharField(max_length=200, choices=STATUS_CHOICES, default='inactive')


class NetworkProvider():
    def __init__(self):
        self.credit = 0
    # it can be in debt - doesn't matter - entire world is in debt...
    # the idea also is not paying money for internet - but in something like "Social Credit" but it's near for china dystopia...
    def buy_transfer_giga_bytes(self, data_in_GB):
        # Mobile Phone Monthly Plan with Calls and 10GB+ Data    ~689.40 N₨
        cost = data_in_GB * 68.94 # potential cost per GB in ruppes (USD 0.50)
        self.credit -= cost
        return data_in_GB

    def charge_network(self, G):

        # how many internet to buy for this hour for 4 tribes (?)...
        gb_available = random.uniform(1, 100)  # Available GB from 1 GB to 100 GB
        GBs = self.buy_transfer_giga_bytes(gb_available)

        for id in G.nodes():
            mb_available = GBs * 1000  # Convert GB to MB
            # Random usage in the last quarter, between 0 and 50 GB
            mb_usage_last_quarter = random.uniform(0, 50) * 1000  # GBs -> MBs
            mb_usage_last_two_quarter = random.uniform(0, 50) * 1000  # GBs -> MBs
            mb_usage_last_three_quarter = random.uniform(0, 50) * 1000  # GBs -> MBs
            # Random bandwidth (Mbps), from 10 Mbps to 100 Mbps
            bandwidth = random.uniform(10, 100)
            # Random latency (ms), between 1 ms and 100 ms
            latency = random.uniform(1, 100)

            from ISP.NetworkPoint import NetworkPoint
            # Create a NetworkPoint instance and store it in the node's 'data' attribute
            G.nodes[id]['data'] = NetworkPoint(id, mb_usage_last_quarter, mb_available, bandwidth, latency, False, mb_usage_last_two_quarter, mb_usage_last_three_quarter)

    def charge_single_point(self, G, id):
        # Retrieve the NetworkPoint instance for the given node (id)

        GBs = self.buy_transfer_giga_bytes(10)
        node_data = G.nodes[id]['data']
        node_data.mb_available += GBs*1000


# 1$ -> 137.93 NPR

# Use spectrum in efficient way

# flip asymetry
# who gets? when? how fast?

#Network efficiencies

# 250 Mbps -> 1 Month 1,450 NPR, 3 Month 3,600 NPR, 12 Month 12,600 NPR
# 300 Mbps -> 1 Month 1,550 NPR, 3 Month 3,600 NPR, 12 Month 13,800 NPR

# in over 10,000 locations throughout Nepal. Currently, there are over 14,000 of these Wi-Fi hotspots across Nepal.

# also the data amount is not everything - there are still speed, latency and bandwidth

# Fulfill the network - some kind of transaction
# pay ~136,379 NPR (100$) for 100TB  (100 000 GB) (100 000 000 MB) to redistribute

# 1 PB -> 1024 TB (PetaBytes to TeraBytes)