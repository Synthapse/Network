# Network
Develop AI-driven tools that improve decentralized network performance and scalability.

Project containing couples of microservices, which may be deployed via Docker or Kubernetes

Instalation:

pip install -r requirements.txt


# Time Series predictive algorithm
SARIMA (Seasonal Autoregressive Integrated Moving Average)
(https://machinelearningmastery.com/sarima-for-time-series-forecasting-in-python/)

https://colab.research.google.com/drive/1MGkMvDWOphm4Iyn8Kwq-_I2LyH07Khv9?usp=sharing#scrollTo=pSjoPXIHn2P7

run in debug mode: 
python3 -m pdb main.py

# GNN (GNN Graph Neutral Network) 
Training model for distribution the network

# ISP
Seeding the every nodes in graph by real internet data
DataStreaming -> Kafka for real time communication with the nodes to the neighbours.
Each node is both producer and the consuer - to raporting about current usage in time interval
(1 month, 1 week, 1 hour, 1 minute)]

# Kafka Broker 
run locally for working communication between network

Go to the official Apache Kafka download page: Kafka Downloads.
https://kafka.apache.org/downloads


1. Start Zookeper (for distributed coordination) (in downloaded folder)
2. Start Kafka Broker

May be installed locally or via docker (docker-compose up)

cd kafka_2.12-3.9.0
bin/zookeeper-server-start.sh config/zookeeper.properties
bin/kafka-server-start.sh config/server.properties

stop: 

rm -rf /tmp/zookeeper
rm -rf /tmp/kafka-logs

bin/kafka-server-stop.sh
bin/zookeeper-server-stop.sh


lsof -i :9092
kill -9 <PID>


open: localhost:9092

Check if topics exists:

bin/kafka-topics.sh --bootstrap-server localhost:9092 --list

Each node try to connect to kafka instance broker:


%3|1737714414.271|FAIL|rdkafka#consumer-316| [thrd:localhost:9092/bootstrap]: localhost:9092/bootstrap: Connect to ipv6#[::1]:9092 failed: Connection refused (after 50ms in state CONNECT)


Node Kathmandu sent message to Node <ISP.NetworkPoint.NetworkPoint object at 0x108f14310>: Hello, neighbor!
Sending message to <ISP.NetworkPoint.NetworkPoint object at 0x1009349b0>

from Kathmandu topics (each node send data to neighbors):

- node_C1_messages
- node_C2_messages
- node_C3_messages
- node_C4_messages
- node_C5_messages
- node_Gandaki_messages
- node_Janakpur_messages

All mesages from begining (for particular topic):
bin/kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic node_Gandaki_messages --from-beginning


KAFKA UI

Logs (Prometheus/Grafana) (?)

brew install confluentinc/tap/ccloud-cli
brew install confluentinc/tap/confluent-platform