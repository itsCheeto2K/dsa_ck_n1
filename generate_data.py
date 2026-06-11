#@title Create test case
import random
import os

def generate_test_case(filename: str, V: int, E: int, root: int = 0):

    if E < V - 1:
        raise ValueError("For a graph to be connected, the number of edges (E) must be at least V − 1.")

    with open(filename, 'w') as f:
        f.write(f"{V} {E}\n")

        edges_written = 0

        connected_nodes = [root]
        unconnected_nodes = list(range(V))
        unconnected_nodes.remove(root)

        random.shuffle(unconnected_nodes)

        for v in unconnected_nodes:
            u = random.choice(connected_nodes)
            w = random.randint(100, 1000)
            f.write(f"{u} {v} {w}\n")

            connected_nodes.append(v)
            edges_written += 1

        while edges_written < E:
            u = random.randint(0, V - 1)
            v = random.randint(0, V - 1)

            if u != v and v != root:
                w = random.randint(1, 100)
                f.write(f"{u} {v} {w}\n")
                edges_written += 1

    print(f"Done: {filename} (Size: {os.path.getsize(filename) / (1024*1024):.2f} MB)\n")

if __name__ == "__main__":
    generate_test_case("test_5k.txt", V=500, E=5000)
    generate_test_case("test_10k.txt", V=1000, E=10000)
    generate_test_case("test_30k.txt", V=3000, E=30000)
    generate_test_case("test_50k.txt", V=5000, E=50000)