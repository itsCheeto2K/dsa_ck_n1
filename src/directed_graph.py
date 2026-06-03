class DirectedGraph:
    def __init__(self, numVertices):
        self.numVertices = numVertices
        self.edges = []

    def addEdge(self, u, v, w):
        self.edges.append(Edge(u, v, w, u, v))

    def getEdges(self):
        return self.edges.copy()

    def getNumVertices(self):
        return self.numVertices

    def clone(self):
        clonedGraph = DirectedGraph(self.numVertices)
        for edge in self.edges:
            clonedGraph.edges.append(edge.clone())
        return clonedGraph

    @staticmethod
    def readFromFile(path):
        try:
            with open(path, "r") as file:
                lines = [
                    line.strip()
                    for line in file
                    if line.strip()
                ]
            if not lines:
                return None

            V, E = map(int,lines[0].split())
            graph = DirectedGraph(V)

            for i in range(1, E + 1):
                u, v, w = lines[i].split()
                graph.addEdge(int(u), int(v), float(w))
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
                graph.addEdge(int(u), int(v), float(w))
            return graph

        except Exception as e:
            print(f"Input error: {e}")
            return None