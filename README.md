# Network/Energy Optimization Project (IoT)

Develop AI-driven tools that improve decentralized network performance and scalability.

---

## 1. Network Protocols

### TCP Alternatives:

- **HOMA/QUIC** ([Quicly](https://github.com/h2o/quicly/))
- **RINA** (Recursive InterNetwork Architecture) - Future internet architectures
- **NDN** (Named Data Networking) - Future decentralized networking
- **DCCP** (Datagram Congestion Control Protocol) - Video Streaming, Gaming
- **SCTP** (Stream Control Transmission Protocol) - 5G

---

## 2. Optimization Techniques

### AI-Based Optimization:

- **Particle Swarm Optimization (PSO)**
- **Ant Colony Optimization (ACO)**

### Use Cases:

- **Optimizing WiFi Tower Placement** (PSO + GNN)
- **Finding Best Routing Paths for Connectivity** (ACO + GNN)
- **Load Balancing in Networks** (GNN helps ACO/PSO balance traffic)
- **Autonomous Drone-Based Signal Boosting** (ACO finds best signal relay points)

---

## 3. CI/CD for Demonstration

### Components:

- **Zookeeper**
- **Kafka (1 Instance)**
- **Simulator** (API?)
- **UI** (Admin Panel)

### Note for Tomorrow (25.01.2025) - 5 Terminals:

1. ZooKeeper
2. Kafka
3. Prometheus
4. Kafka-Export
5. Grafana

---

## 4. GIS Data & Interference Models (Kenya)

- [GIS Data](https://www.wri.org/data/kenya-gis-data#agriculture)
- [User Density Maps](https://data.humdata.org/dataset/highresolutionpopulationdensitymaps-ken)
- **Interference Models**

---

## 5. Project Deployment

This project contains multiple microservices and can be deployed via Docker or Kubernetes.

### Installation:

```bash
pip install -r requirements.txt
```

### 5G Network Optimization Dataset:

- **Schema:** id, scenario, description, label, estimated\_throughput\_increase
- [Dataset on Hugging Face](https://huggingface.co/datasets/infinite-dataset-hub/5GNetworkOptimization?row=44)

### Environment Setup:

```bash
export DJANGO_SETTINGS_MODULE=Network.settings
```

---

## 6. Time Series Predictive Algorithm

### SARIMA (Seasonal Autoregressive Integrated Moving Average)

- [Guide](https://machinelearningmastery.com/sarima-for-time-series-forecasting-in-python/)
- [Colab Notebook](https://colab.research.google.com/drive/1MGkMvDWOphm4Iyn8Kwq-_I2LyH07Khv9?usp=sharing#scrollTo=pSjoPXIHn2P7)

### Run in Debug Mode:

```bash
python3 -m pdb main.py
```

---

## 7. Graph Neural Networks (GNN)

- **Training model for network distribution**
- **Seeding every node in the graph with real internet data**
- **Data Streaming with Kafka** for real-time communication between nodes
- **Each node acts as both producer and consumer**, reporting current usage at intervals (1 month, 1 week, 1 hour, 1 minute)

---

## 8. Kafka Broker

### Local Setup:

1. **Download Kafka** ([Official Apache Kafka Download](https://kafka.apache.org/downloads))
2. **Start ZooKeeper (for distributed coordination):**
   ```bash
   cd kafka_2.12-3.9.0
   bin/zookeeper-server-start.sh config/zookeeper.properties
   ```
3. **Start Kafka Broker:**
   ```bash
   bin/kafka-server-start.sh config/server.properties
   ```

### Stopping Kafka:

```bash
rm -rf /tmp/zookeeper
rm -rf /tmp/kafka-logs
bin/kafka-server-stop.sh
bin/zookeeper-server-stop.sh
```

### Kafka Cleanup:

```bash
lsof -i :9092
kill -9 <PID>
```

### Checking Topics:

```bash
bin/kafka-topics.sh --bootstrap-server localhost:9092 --list
```

### Delete All Topics:

```bash
for topic in $(bin/kafka-topics.sh --bootstrap-server localhost:9092 --list); do
    bin/kafka-topics.sh --bootstrap-server localhost:9092 --topic $topic --delete;
done
```

### Kafka Consumer Groups:

```bash
kafka-consumer-groups.sh --bootstrap-server localhost:9092 --list
```

### Sample Node Communication:

```log
Node Kathmandu sent message to Node <ISP.NetworkPoint.NetworkPoint object at 0x108f14310>: Hello, neighbor!
Sending message to <ISP.NetworkPoint.NetworkPoint object at 0x1009349b0>
```

### Messages from Beginning:

```bash
bin/kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic node_Gandaki_messages --from-beginning
```

---

## 9. Monitoring & Logging

### Kafka UI:

- **Logs with Prometheus/Grafana** (To be confirmed)

### Installation:

```bash
brew install confluentinc/tap/ccloud-cli
brew install confluentinc/tap/confluent-platform
brew install prometheus
```

### Running Prometheus:

```bash
prometheus --config.file=prometheus-2.31.2.linux-amd64/prometheus.yml
```

- **Prometheus UI:** [http://localhost:9090/query](http://localhost:9090/query)

### Running Kafka Exporter:

```bash
docker run -ti --rm -p 9308:9308 danielqsj/kafka-exporter --kafka.server=host.docker.internal:9092
```

- **Kafka Exporter Metrics:** [http://localhost:9308/metrics](http://localhost:9308/metrics)

### Running Grafana:

```bash
brew install grafana
brew services start grafana
```

- **Grafana UI:** [http://localhost:3000](http://localhost:3000)

---

## 10. Additional Resources

- **AI Hackathon Data:** [Notion Page](https://balanced-airmail-b72.notion.site/AI-Hackhathon-181529bf8e08803db16acb72d0f899ef?pvs=74)

