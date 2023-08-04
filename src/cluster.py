from itertools import cycle
import statistics

class Node:
    def __init__(self, size) -> None:
        self.shard_list = []
        self.size = size

class Cluster:
    def __init__(self, n_nodes, n_replicas, data_size, n_shards, nodes_storage_list):
        self.n_shards = n_shards
        self.n_replicas = n_replicas
        # data_size is the original size without replication
        self.data_size = data_size
        self.n_nodes = n_nodes
        if isinstance(nodes_storage_list, int):
            storage_per_node = nodes_storage_list
            nodes_storage_list = [storage_per_node for _ in range(n_nodes)]
        else:
            assert len(nodes_storage_list) == n_nodes
        self.cluster_storage_size = sum(nodes_storage_list)
        self.nodes = [Node(nodes_storage_list[i]) for i in range(n_nodes)]

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
        if total_data_size > (self.cluster_storage_size):
            return -1
        inhomogeneity = statistics.stdev(
            [len(node.shard_list) for node in self.nodes]
        )
        return self.n_replicas / (1 + inhomogeneity)