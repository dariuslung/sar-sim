import argparse

class Node:
    def __init__(self, name, num_nodes):
        self.name = name
        self.data = [name + str(i) for i in range(num_nodes)]

class RingAllReduce:
    def __init__(self, num_nodes, node_latency, link_latency):
        self.num_nodes = num_nodes
        self.node_latency = node_latency
        self.link_latency = link_latency
        # Node as characters 'a' to 'z' (limited to 26 nodes)
        self.nodes = [Node(chr(ord('a') + i), num_nodes) for i in range(num_nodes)]

    def simulate(self):
        print(f"Number of nodes: {self.num_nodes}.")
        print(f"Node latencies: {self.node_latency}")
        print(f"Link latencies: {self.link_latency}")

        # Ring AllReduce logic
        STEPS = self.num_nodes - 1
        total_latency = 0
        for step in range(STEPS):
            print(f"\n--- Step {step + 1} ---")
            for i in range(self.num_nodes):
                sender = self.nodes[i]
                receiver = self.nodes[(i + 1) % self.num_nodes]
                data_to_send = sender.data[(i - step) % self.num_nodes]
                sender.data[(i - step) % self.num_nodes] = None  # Simulate sending data
                receiver.data[(i - step) % self.num_nodes] += data_to_send
                print(f"Node {sender.name} sends {data_to_send} to Node {receiver.name}")

            total_latency_per_step = max(self.node_latency) + max(self.link_latency)
            total_latency += total_latency_per_step
            print(f"Step {step + 1} latency: {total_latency_per_step}")
        print(f"Total latency: {total_latency}")

        # Final data state
        print("\nFinal data at each node:")
        for node in self.nodes:
            print(f"Node {node.name}: {node.data}")

if __name__ == "__main__":
    # Get Ring AllReduce configuration
    parser = argparse.ArgumentParser(description="Ring AllReduce Simulation")
    parser.add_argument("-n", help="Number of nodes", default="5")
    parser.add_argument("--node-latency", help="Comma-separated node latencies", default=None)
    parser.add_argument("--link-latency", help="Comma-separated link latencies", default=None)
    
    # Process configuration
    num_nodes = int(parser.parse_args().n)
    node_latency = list(map(int, parser.parse_args().node_latency.split(','))) if parser.parse_args().node_latency else [1] * num_nodes
    link_latency = list(map(int, parser.parse_args().link_latency.split(','))) if parser.parse_args().link_latency else [1] * num_nodes
    
    RingAllReduce(num_nodes, node_latency, link_latency).simulate()