import random
import os

def generate_test_case(filename: str, V: int, E: int, root: int = 0):
    print(f"Đang tạo {filename} (V={V}, E={E})...")
    
    if E < V - 1:
        raise ValueError("Số cạnh (E) phải lớn hơn hoặc bằng V - 1 để đồ thị liên thông.")
    
    with open(filename, 'w') as f:
        # Ghi header với 2 số V và E (Fix lỗi unpack)
        f.write(f"{V} {E}\n")
        
        edges_written = 0
        
        # --- BƯỚC 1: TẠO BỘ XƯƠNG SỐNG (SPANNING TREE) ---
        # Đảm bảo chắc chắn mọi đỉnh đều có thể đi tới được từ Root
        connected_nodes = [root]
        unconnected_nodes = list(range(V))
        unconnected_nodes.remove(root)
        
        # Trộn ngẫu nhiên các đỉnh chưa kết nối
        random.shuffle(unconnected_nodes)
        
        for v in unconnected_nodes:
            # Chọn ngẫu nhiên 1 đỉnh ĐÃ kết nối làm cha
            u = random.choice(connected_nodes)
            w = random.randint(100, 1000) # Trọng số xương sống cho cao một chút
            f.write(f"{u} {v} {w}\n")
            
            connected_nodes.append(v)
            edges_written += 1
            
        print(f"  -> Đã dựng xong xương sống liên thông ({edges_written} cạnh).")
        
        # --- BƯỚC 2: TẠO CHU TRÌNH NGẪU NHIÊN (NOISE/CYCLES) ---
        # Bắn các cạnh còn lại một cách ngẫu nhiên để tạo bẫy
        while edges_written < E:
            u = random.randint(0, V - 1)
            v = random.randint(0, V - 1)
            
            # Không tự trỏ vào chính mình và không trỏ vào Root
            if u != v and v != root:
                w = random.randint(1, 100) # Trọng số bẫy chu trình cho thật rẻ để lừa thuật toán tham lam
                f.write(f"{u} {v} {w}\n")
                edges_written += 1
                
    print(f"✅ Hoàn tất: {filename} (Kích thước: {os.path.getsize(filename) / (1024*1024):.2f} MB)\n")

if __name__ == "__main__":
    # Sinh lại toàn bộ dữ liệu với thuật toán mới
    generate_test_case("test_10k.txt", V=1000, E=10000)
    generate_test_case("test_100k.txt", V=10000, E=100000)
    generate_test_case("test_1m.txt", V=100000, E=1000000)