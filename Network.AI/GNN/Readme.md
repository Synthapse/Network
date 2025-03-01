## 1. Graph Neural Networks (GNN)

- **Training model for network distribution**
- **Seeding every node in the graph with real internet data**
- **Data Streaming with Kafka** for real-time communication between nodes
- **Each node acts as both producer and consumer**, reporting current usage at intervals (1 month, 1 week, 1 hour, 1 minute)


## 2. GIS Data & Interference Models (Kenya)

- [GIS Data](https://www.wri.org/data/kenya-gis-data#agriculture)
- [User Density Maps](https://data.humdata.org/dataset/highresolutionpopulationdensitymaps-ken)
- **Interference Models**

---




Random tensor (per features)

mb_available | mb_usage_last_quarter | bandwidth | latency

It's on network level:

mb_usage_last_quarter | mb_usage_last_two_quarter | mb_usage_last_three_quarter

000 = {list: 3} [29224.3463589436, 46731.83472317014, 41686.139013587934]
001 = {list: 3} [43674.736478054794, 24291.00938697618, 1248.4183025814943]
002 = {list: 3} [21527.616998842663, 35466.603776836426, 23283.022967155623]
003 = {list: 3} [14114.419707596393, 38829.303989541986, 1590.5896113646345]


Predicted Data Usage for Next Quarter (15min) (GB):

Predicted Data Usage for Next Quarter (15min) (MB): tensor([[20875.6348],
        [22878.3145],
        [23793.2930],
        [23855.7637],
        [23940.5273],
        [23958.9062],
        [23956.0742],
        [24013.4785],
        [24013.4180],
        [24065.9766],
        [24020.2598],
        [24036.2070],