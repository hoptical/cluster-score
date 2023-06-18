from itertools import cycle
import statistics

class Node:
    def __init__(self) -> None:
        self.shard_list = []


class Cluster:
    def __init__(self, n_nodes, n_replicas, data_size, n_shards, storage_per_node):
        self.n_shards = n_shards
        self.n_replicas = n_replicas
        # data_size is the original size without replication
        self.data_size = data_size
        self.storage_per_node = storage_per_node
        self.n_nodes = n_nodes
        self.nodes = [Node() for _ in range(n_nodes)]

    def shard_allocator(self):
        # Round-roubin method
        pool = cycle([i for i in range(self.n_nodes)])
        for i in range(self.n_shards):
            for _ in range(self.n_replicas):
                # Allocating using a circular queue
                candidate = self.nodes[pool.__next__()]
                candidate.shard_list.append(i)

    def cluster_score(self):
        # lower is better
        total_data_size = self.data_size * self.n_replicas
        if total_data_size > (self.n_nodes * self.storage_per_node):
            return -1
        inhomogeneity = statistics.stdev(
            [len(node.shard_list) for node in self.nodes]
        )
        return self.n_replicas / (1 + inhomogeneity)