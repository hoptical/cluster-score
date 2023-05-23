from itertools import cycle
import statistics
import argparse


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


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Cluster Allocation")
    parser.add_argument("--n_nodes", type=int, default=4, help="Number of nodes")
    parser.add_argument("--n_shards", type=int, default=2, help="Number of shards")
    parser.add_argument("--n_replicas", type=int, default=2, help="Number of replicas")
    parser.add_argument("--data_size", type=int, default=2, help="Data size in TB")
    parser.add_argument("--storage_per_node", type=int, default=1, help="Storage per node in TB")
    args = parser.parse_args()

    n_nodes = args.n_nodes
    n_shards = args.n_shards
    n_replicas = args.n_replicas
    data_size = args.data_size
    storage_per_node = args.storage_per_node

    cluster = Cluster(n_nodes, n_replicas, data_size, n_shards, storage_per_node)
    cluster.shard_allocator()
    print(
        "Number of nodes: {} \nNumber of shards: {} \nNumber of replicas: {} \nData size: {} TB\nStorage per node: {} TB\n".format(
            n_nodes, n_shards, n_replicas, data_size, storage_per_node
        )
    )

    print("Cluster Allocation:")
    for i in range(n_nodes):
        print("Node {}: ".format(i), cluster.nodes[i].shard_list)

    cluster_score = cluster.cluster_score()
    print("Cluster Score: {} (higher is better.)".format(cluster_score))
