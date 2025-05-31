# FCSE: Social Networks and Media - Final Project
This document serves as a _brief_ overview of the project. 

## 1. Dataset
We are working with the ToN_IoT dataset focusing on the `train_test_network.csv`. Since this dataset is heavily imbalanced and skewed toward the `Attack` class, we use `project_utils/balanced-dataset-creator.py` to create the `balanced_train_test_network.csv` file. This is a balanced dataset containing exactly 50,000 entries classified as `Normal` form the original dataset, and 50,000 randomly sampled `Attack` entries from the ~160,000 entries in the original dataset. 

## 2. Deep Learning Models
We are relying on GCN and GraphSAGE models for our classifiers. 

## 3. Our Results 
Based on the following graph structure, we are classiying entries into two categories. 

| Element            | What You Use From Dataset                              |
|--------------------|--------------------------------------------------------|
| **Nodes**          | IP addresses from `src_ip` and `dst_ip`                |
| **Edges**          | One edge per connection or flow from `src_ip → dst_ip` |
| **Directionality** | Yes – flows are directed from source to destination    |
| **Edge Weight**    | Optional – could be frequency, total bytes, etc.       |

Edge Attributes:
- **proto** (TCP/UDP/ICMP)
- **service** (HTTP, DNS, SSL, etc.)
- **duration** (length of the flow in seconds)
- **src_bytes** / dst_bytes (payload size per direction)
- **conn_state** (S0, S1, REJ — Zeek flow state)
- **missed_bytes** (for gap analysis)
- **label** (0 = normal, 1 = attack)
- **type** (attack category, e.g., DDoS, DoS, backdoor)
