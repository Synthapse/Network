
✅ QUIC makes real-time updates much faster & secure
✅ Kafka is still used for logging & ISP messaging
✅ NetworkPoint acts as a QUIC server, while AccessPoint makes direct QUIC requests

`sudo tcpdump -i lo0 udp port 4433 -X`

7 packets captured
552 packets received by filter
0 packets dropped by kernel

`
sudo lsof -iUDP:4433
`
Python  80694 piotrzak    6u  IPv4 0x99cf5bd85ad2ac95      0t0  UDP *:4433


Alternative Without Kafka
- QUIC for real-time requests (e.g., bandwidth updates).
- WebSockets or gRPC for structured communication if needed.
- A simple REST API if you want AccessPoints to request data periodically

Kafka only in Event-driven, scalable system (costly for small projects)

- A Network Point (NP) is a higher-level node that aggregates and manages multiple APs. It acts as a gateway between APs and the ISP/cloud infrastructure.
- An Access Point (AP) is a network device that allows client devices (phones, laptops, IoT devices) to connect to a network. It is typically used in WiFi, 5G, or LoRaWAN networks.


Example Interaction:
- AP detects high traffic → Sends request to NP: "Need 50 Mbps more!"
- NP checks availability → If possible, reallocates bandwidth.
- NP responds to AP → "Here’s 50 Mbps, use it wisely!"
- AP updates latency info → Reports back to NP for monitoring.


AP Requests Bandwidth from NP

If an AP needs more bandwidth, it sends a request to NP.
- NP decides whether to allocate extra bandwidth or deny it.
- NP Monitors & Adjusts Latency

- NP monitors overall network latency and can optimize routing.
It may instruct an AP to adjust settings to reduce delays.
- 
- AP Reports Network Issues to NP

If an AP has high latency or connectivity issues, it informs NP.
- NP aggregates reports and may escalate them to the ISP.


! IMPORTANT ! 
Keys cannot be stored in the repository, but it's PoC, so I will store them here.

New TLS Certificate for QUIC communication:

- Subject Alternative Name (SAN)

openssl req -x509 -newkey rsa:2048 -keyout key.pem -out cert.pem -days 365 -nodes \
-subj "/CN=localhost" -addext "subjectAltName=DNS:localhost,IP:127.0.0.1"


Random logs from device, which communicate with single network point:

{"status": "approved", "node_id": "Kathmandu", "data_granted_mb": 20}
{"status": "denied", "node_id": "Kathmandu", "reason": "Insufficient resources"}

[2025-01-24 21:25:57,842] INFO [GroupMetadataManager brokerId=0] Group group_C1 transitioned to Dead in generation 5 (kafka.coordinator.group.GroupMetadataManager)
[2025-01-24 21:18:54,855] INFO [GroupCoordinator 0]: Group group_C3 with generation 5 is now empty (__consumer_offsets-36) (kafka.coordinator.group.GroupCoordinator)
