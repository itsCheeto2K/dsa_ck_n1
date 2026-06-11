#@title class DirectedGraph - MTu
from src.edge import Edge

class DirectedGraph:
    def __init__(self, numVertices):
        self.numVertices = numVertices
        self.edges = []

    def setNumVertices(self, numVertices, pruneInvalidEdges=False):
        if numVertices is None:
            raise ValueError("numVertices cannot be None")
        numVertices = int(numVertices)
        if numVertices < 0:
            raise ValueError("numVertices must be non-negative")

        if numVertices < self.numVertices:
            has_out_of_range = any(
                (e.u < 0 or e.u >= numVertices or e.v < 0 or e.v >= numVertices)
                for e in self.edges
            )
            if has_out_of_range:
                if pruneInvalidEdges:
                    self.edges = [
                        e
                        for e in self.edges
                        if 0 <= e.u < numVertices and 0 <= e.v < numVertices
                    ]
                else:
                    raise ValueError(
                        "Cannot shrink numVertices: existing edges reference removed vertices"
                    )

        self.numVertices = numVertices

    def _validateEdge(self, u, v, w):
        V = self.numVertices
        if u < 0 or u >= V or v < 0 or v >= V:
            raise ValueError(f"Invalid edge: {u} -> {v}")
        if u == v:
            raise ValueError("Self-loop not allowed")

    def addEdge(self, u, v, w, validate=True):
        u = int(u)
        v = int(v)
        w = float(w)
        if validate:
            self._validateEdge(u, v, w)
        self.edges.append(Edge(u, v, w, u, v))

    def getEdges(self):
        return [edge.clone() for edge in self.edges]

    def getNumVertices(self):
        return self.numVertices

    def clone(self):
        clonedGraph = DirectedGraph(self.numVertices)
        for edge in self.edges:
            clonedGraph.edges.append(edge.clone())
        return clonedGraph

    @staticmethod
    def _stripComment(line):
        for token in ("#", "//"):
            idx = line.find(token)
            if idx != -1:
                line = line[:idx]
        return line.strip()

    @staticmethod
    def readFromFile(path):
        try:
            with open(path, "r") as file:
                raw_lines = [DirectedGraph._stripComment(line) for line in file]
                lines = [line for line in raw_lines if line]

            if not lines:
                return None

            V, E = map(int, lines[0].split())
            graph = DirectedGraph(V)

            edge_lines = lines[1:]
            edge_count = 0
            for line in edge_lines:
                if edge_count >= E:
                    break
                parts = line.split()
                if len(parts) < 3:
                    raise ValueError(f"Invalid edge line: '{line}'")
                u, v, w = parts[0], parts[1], parts[2]
                graph.addEdge(u, v, w, validate=True)
                edge_count += 1

            if edge_count != E:
                raise ValueError(
                    f"Expected {E} edges but found {edge_count} in file: {path}"
                )
            return graph

        except Exception as e:
            print(f"File reading error: {e}")
            return None

    @staticmethod
    def readFromConsole():
        try:
            print("Enter number of vertices and edges (V E):")

            V, E = map(int, input().split())
            graph = DirectedGraph(V)
            print(f"Enter {E} edges in format: u v w")

            for _ in range(E):
                u, v, w = input().split()
                graph.addEdge(u, v, w, validate=True)
            return graph

        except Exception as e:
            print(f"Input error: {e}")
            return None