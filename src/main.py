import argparse
from cluster import Cluster

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Cluster Allocation")
    parser.add_argument("--n_nodes", type=int, default=4, help="Number of nodes")
    parser.add_argument("--n_shards", type=int, default=2, help="Number of shards")
    parser.add_argument("--n_replicas", type=int, default=2, help="Number of replicas")
    parser.add_argument("--data_size", type=int, default=2, help="Data size in TB")
    parser.add_argument("--storage_per_node", type=int, default=1, 
                        help="Storage per node in TB")
    args = parser.parse_args()

    n_nodes = args.n_nodes
    n_shards = args.n_shards
    n_replicas = args.n_replicas
    data_size = args.data_size
    storage_per_node = args.storage_per_node

    cluster = Cluster(n_nodes, n_replicas, data_size, n_shards, storage_per_node)
    cluster.shard_allocator()
    print(
        "Number of nodes: {} \nNumber of shards: {} \nNumber of replicas: {} \n \
            Data size: {} TB\nStorage per node: {} TB\n".format(
            n_nodes, n_shards, n_replicas, data_size, storage_per_node
        )
    )

    print("Cluster Allocation:")
    for i in range(n_nodes):
        print("Node {}: ".format(i), cluster.nodes[i].shard_list)

    cluster_score = round(cluster.cluster_score(), 3)
    print("Cluster Score: {} (higher is better.)".format(cluster_score))
