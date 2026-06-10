from __future__ import annotations
from secrets import choice
import time
import sys

# Increase recursion limit to prevent Stack Overflow (RecursionError) for large graphs
sys.setrecursionlimit(2000000)

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

EMBEDDED_INPUT = """\
# Format:
#   V E root(optional)
#   then E lines: u v w

4 6 0
0 1 10
0 2 20
1 2 2
2 1 3
2 3 5
1 3 15
"""

def _read_problem_from_text(text: str):
    raw_lines = text.splitlines()
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


def run_solver(graph: DirectedGraph, root: int, test_name: str = ""):
    """Helper function to orchestrate the algorithm execution, timing, and formatting."""
    print(f"\n{'='*45}")
    print(f"🚀 STARTING TEST: {test_name}")
    print(f"Scale: {graph.getNumVertices()} vertices, {len(graph.edges)} edges")
    print(f"{'-'*45}")

    # Start high-resolution timer
    start_time = time.perf_counter()
    
    solver = ChuLiuEdmonds()
    arbo = solver.solve(graph, root)
    
    # End timer
    end_time = time.perf_counter()
    execution_time = end_time - start_time

    # Print results
    is_valid = arbo.is_valid()
    print(f"Valid          : {'✅ True' if is_valid else '❌ False'}")
    print(f"Total weight   : {arbo.total_weight()}")
    print(f"Execution time : {execution_time:.4f} seconds")

    # Only print edge details for small graphs to avoid console lag
    if len(graph.edges) <= 20:
        print("\nSelected edges details:")
        for edge in sorted(arbo.edges, key=lambda e: (e.u, e.v)):
            print(f"  {edge}")
    else:
        print("\n(Edge list hidden to prevent console lag)")
    print(f"{'='*45}\n")


def main():
    while True:
        print("📊 CHU-LIU/EDMONDS ALGORITHM TEST MENU")
        print("1. Run Small Demo (Embedded Input - Cycle Trap)")
        print("2. Run test_10k.txt (10,000 edges)")
        print("3. Run test_100k.txt (100,000 edges)")
        print("4. Run test_1m.txt (1,000,000 edges)")
        print("0. Exit")
        
        choice = input("Select an option (0-4): ").strip()
        
        if choice == '0':
            print("Exited program.")
            break
            
        elif choice == '1':
            problem = _read_problem_from_text(EMBEDDED_INPUT)
            if problem is not None:
                graph, root = problem
                run_solver(graph, root, "Embedded Demo (4 Vertices - 6 Edges)")
            else:
                print("Error parsing embedded input.")
            
        elif choice in ['2', '3', '4']:
            file_map = {'2': 'test_10k.txt', '3': 'test_100k.txt', '4': 'test_1m.txt'}
            filename = file_map[choice]
            
            try:
                print(f"Reading data from file {filename}...")
                
                # Mở file và đọc toàn bộ nội dung
                with open(filename, 'r') as f:
                    file_content = f.read()
                
                # Dùng parser xịn xò của chúng ta để xử lý
                problem = _read_problem_from_text(file_content)
                
                if problem is None:
                    print(f"Error: File {filename} is empty or corrupted.")
                    continue
                    
                graph, root = problem
                run_solver(graph, root, f"File {filename}")
                
            except FileNotFoundError:
                print(f"Error: File {filename} not found. Please run generate_data.py first!")
            except Exception as e:
                print(f"Error processing file: {e}")


if __name__ == "__main__":
    main()