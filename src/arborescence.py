#@title class Arborescence - KAn
class Arborescence:
    def __init__(self, edges, root, num_vertices):
        self.edges = edges
        self.root = root
        self.num_vertices = num_vertices

    def total_weight(self):
        return sum(e.w for e in self.edges)

    def is_valid(self):
        in_degree = {}
        outgoing = {}
        for e in self.edges:
            in_degree[e.v] = in_degree.get(e.v, 0) + 1
            if e.u not in outgoing:
                outgoing[e.u] = []
            outgoing[e.u].append(e.v)

        for v in range(self.num_vertices):
            if v == self.root:
                if in_degree.get(v, 0) != 0:
                    return False
            else:
                if in_degree.get(v, 0) != 1:
                    return False

        if len(self.edges) != self.num_vertices - 1:
            return False

        reachable = set([self.root])
        stack = [self.root]
        while stack:
            u = stack.pop()
            for v in outgoing.get(u, []):
                if v not in reachable:
                    reachable.add(v)
                    stack.append(v)

        return len(reachable) == self.num_vertices

    def print_result(self):
        print(f"Hợp lệ: {self.is_valid()}")
        print(f"Tổng trọng số: {self.total_weight()}")
        for edge in sorted(self.edges, key=lambda e: (e.u, e.v)):
            print(f"  {edge}")