class Edge:
    def __init__(self, u, v, w, origU, origV):
        self.u = u
        self.v = v
        self.w = w
        self.origU = origU
        self.origV = origV

    def __str__(self):
        return f"{self.u} -> {self.v} : {self.w}"
    def __repr__(self):
        return self.__str__()

    def debug_str(self):
        return (
            f"{self.u} -> {self.v} : {self.w} "
            f"(orig: {self.origU} -> {self.origV})"
        )

    def clone(self):
        return Edge(
            self.u,
            self.v,
            self.w,
            self.origU,
            self.origV
        )