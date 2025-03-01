# Network/Energy Optimization Project (IoT)

Develop AI-driven tools to improve decentralized network performance and scalability.

## Components:
1. **Network.AI**
2. **Network.Data**
3. **Network.Frontend**
4. **Network.Backend**

## Macro Scale (Entire Network)
- **Particle Swarm Optimization (PSO)**
- **Ant Colony Optimization (ACO)**
- **Optimizing WiFi Tower Placement** (PSO + GNN)
- **Finding Best Routing Paths for Connectivity** (ACO + GNN)
- **Load Balancing in Networks** (GNN helps ACO/PSO balance traffic)
- **Autonomous Drone-Based Signal Boosting** (ACO finds best signal relay points)

## Micro Scale (Individual Nodes)
- **ns3 Simulations**


### AI Hackathon Data:
- [Notion Page](https://balanced-airmail-b72.notion.site/AI-Hackhathon-181529bf8e08803db16acb72d0f899ef?pvs=74)

### Experimental
**Network.Infrastructure**

---

## Infrastructure Cost:

Google Cloud Pricing Calculators:
- [Cloud Calculator Link 1](https://cloud.google.com/products/calculator?hl=en&dl=CjhDaVJoWWpsaFlXSTFOeTB6Wm1SaExUUXlNelV0T0RrMk9TMDNNREkxT0RGa09EWTNOemdRQWc9PRAuGiQ2MDQ4QTJFNC1GRkUxLTQ5OTItOTQ2NC0zNTgxMTkzRDkwRTM)
- [Cloud Calculator Link 2](https://cloud.google.com/products/calculator/estimate-preview/CiRhYjlhYWI1Ny0zZmRhLTQyMzUtODk2OS03MDI1ODFkODY3NzgQAg==?hl=en)

### Services & Costs:
- **Grafana** (Google Cloud Run) - On-demand, pay-per-use pricing
- **Kafka/Zookeeper/Kafka Exporter** (Google Compute Engine) - Requires at least **2 vCPUs and 4GB+ RAM** for small workloads
- **Recommended Instance:** `c2-standard-4` (4 vCPUs, 16GB RAM) → **$26.60/month (730 hours)**

### Grafana Access:
- **URL:** [Grafana Service](https://grafana-service-946555989276.europe-central2.run.app/login)
- **Credentials:** `admin/synthapse`

Cloud Run Pricing Examples: [Cloud Run Pricing](https://cloud.google.com/run/pricing)

---

## Google Cloud Configuration

```bash
gcloud config set project cognispace
gcloud config set account coginspace@cognispace.iam.gserviceaccount.com

# Assign IAM permissions to Kafka
gcloud artifacts repositories add-iam-policy-binding kafka \  
  --location=europe-central2 \  
  --project=voicesense \  
  --member="allUsers" \  
  --role="roles/artifactregistry.writer"
```

---

## 5G Network Optimization Dataset

- **Schema:** `id`, `scenario`, `description`, `label`, `estimated_throughput_increase`
- **Dataset:** [Hugging Face Link](https://huggingface.co/datasets/infinite-dataset-hub/5GNetworkOptimization?row=44)

### Environment Setup

```bash
export DJANGO_SETTINGS_MODULE=Network.settings
pip install -r requirements.txt
```

---

## 6. Time Series Predictive Algorithm

### SARIMA (Seasonal Autoregressive Integrated Moving Average)

- **Guide:** [SARIMA Guide](https://machinelearningmastery.com/sarima-for-time-series-forecasting-in-python/)
- **Colab Notebook:** [Google Colab Link](https://colab.research.google.com/drive/1MGkMvDWOphm4Iyn8Kwq-_I2LyH07Khv9?usp=sharing#scrollTo=pSjoPXIHn2P7)

### Debug Mode:

```bash
python3 -m pdb main.py
```

---

## 8. Kafka Broker Setup

### Local Setup:

1. **Download Kafka:** [Apache Kafka](https://kafka.apache.org/downloads)
2. **Start ZooKeeper:**
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
rm -rf /tmp/zookeeper /tmp/kafka-logs
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

### Deleting All Topics:
```bash
for topic in $(bin/kafka-topics.sh --bootstrap-server localhost:9092 --list); do
    bin/kafka-topics.sh --bootstrap-server localhost:9092 --topic $topic --delete;
done
```

### Kafka Consumer Groups:
```bash
kafka-consumer-groups.sh --bootstrap-server localhost:9092 --list
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
prometheus --config.file=prometheus.yml
```
- **UI:** [http://localhost:9090/query](http://localhost:9090/query)

### Running Kafka Exporter:
```bash
docker run -ti --rm -p 9308:9308 danielqsj/kafka-exporter --kafka.server=host.docker.internal:9092
```
- **Metrics:** [http://localhost:9308/metrics](http://localhost:9308/metrics)

### Running Grafana:
```bash
brew install grafana
brew services start grafana
```
- **UI:** [http://localhost:3000](http://localhost:3000)

---

