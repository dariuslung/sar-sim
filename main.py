import argparse
import random

class Node:
    def __init__(self, name, num_nodes):
        self.name = name
        self.data = [name + str(i) for i in range(num_nodes)]

class RingAllReduce:
    def __init__(self, num_nodes, node_latency, link_latency, skip, shift, print_steps):
        self.num_nodes = num_nodes
        self.node_latency = node_latency
        self.link_latency = link_latency
        self.skip = skip
        self.shift = shift
        self.print_steps = print_steps
        # Node as characters 'a' to 'z' (limited to 26 nodes)
        self.nodes = [Node(chr(ord('a') + i), num_nodes) for i in range(num_nodes)]

    def simulate(self):
        print(f"Number of nodes: {self.num_nodes}.")
        print(f"Node latencies: {self.node_latency}")
        print(f"Link latencies: {self.link_latency}")
        print(f"Skip steps: {self.skip}")
        print(f"Shift value: {self.shift}")
        
        # Ring AllReduce logic
        STEPS = self.num_nodes - 1
        total_latency = 0
        for step in range(STEPS - self.skip):
            per_step_node_latencies = []
            per_step_link_latencies = []
            if self.print_steps:
                print(f"\n--- Step {step + 1} ---")
            for i in range(self.num_nodes):
                # Shift index
                sender = self.nodes[i]
                receiver = self.nodes[(i + 1) % self.num_nodes]
                # Simulate sending data
                data_index = (i + self.shift - step) % self.num_nodes
                data_to_send = sender.data[data_index]
                sender.data[data_index] = None
                receiver.data[data_index] += data_to_send
                # Record latencies
                per_step_node_latencies.append(self.node_latency[i])
                per_step_link_latencies.append(self.link_latency[i])
                if self.print_steps:
                    print(f"Node {sender.name} sends {data_to_send} to Node {receiver.name}")

            per_step_latency = max(per_step_node_latencies) + max(per_step_link_latencies)
            total_latency += per_step_latency
            if self.print_steps:
                print(f"Step {step + 1} latency: {per_step_latency}")

        # Final data state
        print("\nFinal data at each node:")
        for node in self.nodes:
            print(f"Node {node.name}: {node.data}")

        # Total latency
        print(f"Total latency: {total_latency}")

if __name__ == "__main__":
    # Get Ring AllReduce configuration
    parser = argparse.ArgumentParser(description="Ring AllReduce Simulation")
    parser.add_argument("-n", "--num-nodes", help="number of nodes", default=5, type=int)
    parser.add_argument("--node-latency", help="comma-separated node latencies", default=None)
    parser.add_argument("--link-latency", help="comma-separated link latencies", default=None)
    parser.add_argument("--skip", help="number of skip steps", default=0, type=int)
    parser.add_argument("--shift", help="shift value for starting skip index", default=0, type=int)
    parser.add_argument("--rand-shift", help="use random shift value", action="store_true")
    parser.add_argument("--print-steps", help="print each step", action="store_true")
    
    # Process configuration
    num_nodes = parser.parse_args().num_nodes
    node_latency = list(map(int, parser.parse_args().node_latency.split(','))) if parser.parse_args().node_latency else [1] * num_nodes
    link_latency = list(map(int, parser.parse_args().link_latency.split(','))) if parser.parse_args().link_latency else [1] * num_nodes
    if len(node_latency) != num_nodes or len(link_latency) != num_nodes:
        raise ValueError("Length of node-latency and link-latency must match num-nodes")
    skip = parser.parse_args().skip
    shift = parser.parse_args().shift if parser.parse_args().rand_shift == False else random.randint(0, num_nodes - 1)
    print_steps = parser.parse_args().print_steps
    
    RingAllReduce(num_nodes, node_latency, link_latency, skip, shift, print_steps).simulate()