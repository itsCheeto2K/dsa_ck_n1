
from __future__ import annotations

from pathlib import Path

try:
	from src.directed_graph import DirectedGraph
	from src.chu_liu_edmonds import ChuLiuEdmonds
except Exception:
	from directed_graph import DirectedGraph
	from chu_liu_edmonds import ChuLiuEdmonds


def _strip_comment(line: str) -> str:
	for token in ("#", "//"):
		idx = line.find(token)
		if idx != -1:
			line = line[:idx]
	return line.strip()


def _read_problem_from_file(path: Path):
	if not path.exists():
		return None

	raw_lines = path.read_text(encoding="utf-8", errors="ignore").splitlines()
	lines = [_strip_comment(line) for line in raw_lines]
	lines = [line for line in lines if line]
	if not lines:
		return None

	header = lines[0].split()
	if len(header) < 2:
		raise ValueError("First line must be: V E [root]")

	V = int(header[0])
	E = int(header[1])
	root = int(header[2]) if len(header) >= 3 else None

	if len(lines) < 1 + E:
		raise ValueError(f"Expected {E} edge lines but file has only {len(lines) - 1}")

	edge_lines = lines[1 : 1 + E]
	remaining = lines[1 + E :]

	if root is None and remaining:
		tail = remaining[0].split()
		if len(tail) == 1:
			root = int(tail[0])
		elif len(tail) >= 2 and tail[0].lower() == "root":
			root = int(tail[1])

	if root is None:
		root = 0

	graph = DirectedGraph(V)
	for line in edge_lines:
		parts = line.split()
		if len(parts) < 3:
			raise ValueError(f"Invalid edge line: '{line}'")
		u, v, w = parts[0], parts[1], parts[2]
		graph.addEdge(u, v, w, validate=True)

	if root < 0 or root >= V:
		raise ValueError(f"Invalid root: {root}")

	return graph, root


def main():
	base_dir = Path(__file__).resolve().parent
	input_path = base_dir / "data" / "input.txt"

	try:
		problem = _read_problem_from_file(input_path)
		if problem is None:
			print(f"Input file is empty or missing: {input_path}")
			print("Falling back to console input...")
			graph = DirectedGraph.readFromConsole()
			if graph is None:
				return
			root = int(input("Enter root vertex: ").strip())
		else:
			graph, root = problem

		solver = ChuLiuEdmonds()
		arbo = solver.solve(graph, root)
		arbo.print_result()

	except Exception as e:
		print(f"Error: {e}")


if __name__ == "__main__":
	main()