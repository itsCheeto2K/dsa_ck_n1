#@title class Edge - THien
class Edge:
    __slots__ = ['u', 'v', 'w', 'origU', 'origV', 'original_w', 'to_cycle_vertex', 'real_edge']

    def __init__(self, u, v, w, origU=None, origV=None):
        self.u = int(u)
        self.v = int(v)
        self.w = float(w)
        self.origU = int(origU) if origU is not None else self.u
        self.origV = int(origV) if origV is not None else self.v
        self.original_w = self.w
        self.to_cycle_vertex = None
        self.real_edge = None

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
        new_e = Edge(self.u, self.v, self.w, self.origU, self.origV)
        new_e.original_w = getattr(self, "original_w", self.w)
        new_e.to_cycle_vertex = getattr(self, "to_cycle_vertex", None)
        new_e.real_edge = getattr(self, "real_edge", None)
        return new_e