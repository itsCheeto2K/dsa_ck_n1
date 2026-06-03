try:
	from src.directed_graph import DirectedGraph
	from src.edge import Edge
	from src.arborescence import Arborescence
	from src.union_find import UnionFind
except Exception:
	from directed_graph import DirectedGraph
	from edge import Edge
	from arborescence import Arborescence
	from union_find import UnionFind


class ChuLiuEdmonds:
	"""Chu–Liu/Edmonds algorithm for minimum spanning arborescence (directed MST)."""

	def __init__(self):
		self._contract_stack = []
		self._min_parent = None
		self._min_edge_idx = None
		self._min_weight = None
		self._root = None

	# Public API
	def solve(self, g: DirectedGraph, root: int) -> Arborescence:
		if g is None:
			raise ValueError("Graph cannot be None")

		numV = g.getNumVertices()
		root = int(root)
		if root < 0 or root >= numV:
			raise ValueError(f"Invalid root: {root}")
		if numV == 0:
			return Arborescence([], root, 0)
		if numV == 1:
			return Arborescence([], root, 1)

		return self._solve_recursive(g, root)

	def _solve_recursive(self, g: DirectedGraph, root: int) -> Arborescence:
		numV = g.getNumVertices()

		min_parent, min_edge_idx, min_weight = self._compute_min_in(g, root)
		cycle_node = self.detectCycle(min_parent, numV)

		if cycle_node == -1:
			chosen = []
			for v in range(numV):
				if v == root:
					continue
				chosen.append(g.edges[min_edge_idx[v]])
			return Arborescence(chosen, root, numV)

		prev = (self._min_parent, self._min_edge_idx, self._min_weight, self._root)
		self._min_parent = min_parent
		self._min_edge_idx = min_edge_idx
		self._min_weight = min_weight
		self._root = root

		try:
			id_map = [-1] * numV
			contracted = self.contract(g, cycle_node, id_map)
			contracted_root = id_map[root]
			contracted_arbo = self._solve_recursive(contracted, contracted_root)
			return self.expand(contracted_arbo, self._contract_stack[-1]["cycle_id"])
		finally:
			self._min_parent, self._min_edge_idx, self._min_weight, self._root = prev

	def findMinInEdges(self, g: DirectedGraph, root: int):
		min_parent, _, _ = self._compute_min_in(g, root)
		return min_parent

	def detectCycle(self, minIn, numV: int) -> int:
		numV = int(numV)
		visited = [0] * numV
		stamp = [0] * numV

		for start in range(numV):
			if visited[start]:
				continue

			v = start
			iter_id = start + 1
			while v != -1 and not visited[v] and stamp[v] != iter_id:
				stamp[v] = iter_id
				v = minIn[v]

			if v != -1 and stamp[v] == iter_id:
				return v

			v = start
			while v != -1 and not visited[v]:
				visited[v] = 1
				v = minIn[v]

		return -1

	def contract(self, g: DirectedGraph, cycleNode: int, id):
		if self._min_parent is None or self._min_edge_idx is None or self._min_weight is None:
			raise RuntimeError("contract() called without min-in data")

		numV = g.getNumVertices()
		cycle_node = int(cycleNode)

		cycle_vertices = self._collect_cycle_vertices(self._min_parent, cycle_node)
		if self._root in cycle_vertices:
			raise ValueError("Internal error: root unexpectedly part of a cycle")

		# Union-Find is used for bookkeeping the contracted super-vertex (cycle).
		# It does NOT replace directed-cycle detection in Chu–Liu/Edmonds.
		uf = UnionFind(numV)
		cycle_list = list(cycle_vertices)
		cycle_rep = cycle_list[0]
		for v in cycle_list[1:]:
			uf.union(cycle_rep, v)

		next_id = 0
		for v in range(numV):
			if not uf.same(v, cycle_rep):
				id[v] = next_id
				next_id += 1

		cycle_id = next_id
		for v in cycle_vertices:
			id[v] = cycle_id
		newV = next_id + 1

		contracted = DirectedGraph(newV)

		for e in g.edges:
			new_u = id[e.u]
			new_v = id[e.v]
			if new_u == new_v:
				continue

			adjusted_w = e.w
			to_cycle_vertex = None
			if e.v in cycle_vertices and e.u not in cycle_vertices:
				adjusted_w = e.w - self._min_weight[e.v]
				to_cycle_vertex = e.v

			new_edge = Edge(new_u, new_v, adjusted_w, e.origU, e.origV)
			new_edge.original_w = getattr(e, "original_w", e.w)
			if to_cycle_vertex is not None:
				new_edge.to_cycle_vertex = to_cycle_vertex
			contracted.edges.append(new_edge)

		self._contract_stack.append(
			{
				"graph": g,
				"root": self._root,
				"numV": numV,
				"cycle_id": cycle_id,
				"cycle_vertices": cycle_vertices,
				"min_edge_idx": self._min_edge_idx,
			}
		)
		return contracted

	def expand(self, contracted: Arborescence, cycleNode: int, *args, **kwargs) -> Arborescence:
		if not self._contract_stack:
			raise RuntimeError("expand() called without contract context")

		ctx = self._contract_stack.pop()
		g = ctx["graph"]
		root = ctx["root"]
		numV = ctx["numV"]
		cycle_id = ctx["cycle_id"]
		cycle_vertices = ctx["cycle_vertices"]
		min_edge_idx = ctx["min_edge_idx"]

		if int(cycleNode) != cycle_id:
			cycle_id = int(cycleNode)

		entering = None
		result_edges = []

		for e in contracted.edges:
			if e.v == cycle_id:
				entering = e
			else:
				result_edges.append(self._originalize_edge(e))

		break_vertex = None
		if entering is not None:
			break_vertex = getattr(entering, "to_cycle_vertex", None)

		for v in cycle_vertices:
			if break_vertex is not None and v == break_vertex:
				continue
			cycle_edge = g.edges[min_edge_idx[v]]
			result_edges.append(self._originalize_edge(cycle_edge))

		if entering is not None:
			result_edges.append(self._originalize_edge(entering))

		if len(result_edges) != numV - 1:
			raise ValueError("Internal error: expanded edge count mismatch")

		return Arborescence(result_edges, root, numV)

	def _compute_min_in(self, g: DirectedGraph, root: int):
		numV = g.getNumVertices()
		root = int(root)

		INF = float("inf")
		best_w = [INF] * numV
		min_parent = [-1] * numV
		min_edge_idx = [-1] * numV

		for i, e in enumerate(g.edges):
			if e.v == root:
				continue
			if e.w < best_w[e.v]:
				best_w[e.v] = e.w
				min_parent[e.v] = e.u
				min_edge_idx[e.v] = i

		min_parent[root] = -1
		min_edge_idx[root] = -1
		best_w[root] = 0.0

		for v in range(numV):
			if v == root:
				continue
			if min_edge_idx[v] == -1:
				raise ValueError(f"No arborescence exists: vertex {v} has no incoming edge")

		return min_parent, min_edge_idx, best_w

	def _collect_cycle_vertices(self, parent, cycle_node: int):
		cycle_vertices = set()
		v = cycle_node
		while v not in cycle_vertices:
			cycle_vertices.add(v)
			v = parent[v]
			if v == -1:
				raise ValueError("Internal error: cycle trace reached -1")
		return cycle_vertices

	def _originalize_edge(self, e: Edge) -> Edge:
		w = getattr(e, "original_w", e.w)
		return Edge(int(e.origU), int(e.origV), float(w), int(e.origU), int(e.origV))