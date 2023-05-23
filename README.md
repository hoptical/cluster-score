# Cluster Score

During desining cluster for datases, an engineer should consider different parameters like _Point of Failure_, _Shard Allocation_ and etc. Due to this challenging procedure, this repository has been created to provide a simple programming code in order to calculate score for a cluster with the specified paramters.

## Score Calculation

To calculate the cluster score, the below forumla is used:

```math
inhomogeneity = std_{dev}(nodes\_shard\_size)
```

```math
score = n_{replicas} / (1 + inhomogeneity)
```

Higher score is better. Additionally, if total data size (including replicas) exceeds the total nodes storage, the `score = -1`.

## Usage

### Paramaters

At the moment, these parameters have been considered:

- n_nodes: Number of nodes
- n_shards: Number of shards
- n_replicas: Number of replicas
- data_size: Total data size (without replica)
- storage_per_node: Storage size per node

```bash
python src/main.py --n_nodes 4 --n_shards 2 --n_replicas 2 --data_size 2 --storage_per_node 1
```

Output:

```text
Number of nodes: 4 
Number of shards: 2 
Number of replicas: 2 
Data size: 2 TB
Storage per node: 1 TB

Cluster Allocation:
Node 0:  [0]
Node 1:  [0]
Node 2:  [1]
Node 3:  [1]
Cluster Score: 2.0 (higher is better.)
```
