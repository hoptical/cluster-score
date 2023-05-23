# Cluster Score

During desining cluster for datases, an engineer should consider different parameters like _Point of Failure_, _Shard Allocation_ and etc. Due to this challenging procedure, this repository has been created to provide a simple programming code in order to calculate score for a cluster with the specified paramters.

## Paramaters

At the moment, these parameters have been considered:

- Number of nodes
- Number of shards
- Number of replicas
- Total data size (without replica)
- Storage size per node

## Score Calculation

To calculate the cluster score, the below forumla is used:

```math
inhomogeneity = std_{dev}(nodes shard size)

score = n_{replicas} / (1 + inhomogeneity)
```

Higher score is better. Additionally, if total data size (including replicas) exceeds the total nodes storage, the `score = -1`.
