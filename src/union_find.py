class UnionFind:
    def __init__(self, n):
        self.parent = [i for i in range(n)]
        self.rank = [0] * n

    def find(self, x):
        while self.parent[x] != x:
            # Path Compression (path halving)
            self.parent[x] = self.parent[self.parent[x]]
            x = self.parent[x]
        return x

    def union(self, x, y):
        rootX = self.find(x)
        rootY = self.find(y)

        if rootX == rootY:
            return

        # Union by Rank
        if self.rank[rootX] < self.rank[rootY]:
            rootX, rootY = rootY, rootX

        self.parent[rootY] = rootX

        if self.rank[rootX] == self.rank[rootY]:
            self.rank[rootX] += 1

    def same(self, x, y):
        return self.find(x) == self.find(y)

    def reset(self, n):
        self.parent = [i for i in range(n)]
        self.rank = [0] * n