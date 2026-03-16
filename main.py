# D:/Database/main.py
from lru_replacement import LRUReplacement
from mru_replacement import MRUReplacement
from buffer_pool import BufferPool
import random

def run_simulation(policy_name, requests, buffer_size):
    """
    Hàm chạy bộ mô phỏng Buffer Pool. Nhận vào tên thuật toán, chuỗi requests và kích thước pool.
    """
    print(f"\n*************************************************")
    print(f" START SIMULATION: {policy_name} REPLACEMENT POLICY")
    print(f"*************************************************")
    
    # 1. Khởi tạo đối tượng thuật toán thay thế dựa vào tên được truyền vào
    if policy_name == "LRU":
        algorithm = LRUReplacement()
    else:
        algorithm = MRUReplacement()
        
    # 2. Khởi tạo Buffer Pool (Buffer Manager)
    manager = BufferPool(buffer_size, algorithm)
    
    # Số block requests cần chạy
    for block_num in requests:
        # Gọi xử lý yêu cầu (Sẽ sinh ra các text log: HIT/MISS/LOAD, etc...)
        manager.request_block(block_num)
        
        # Mô phỏng: Đánh dấu một số block ngẫu nhiên là bị chỉnh sửa (Dirty) - tỷ lệ khoảng 25%
        if random.random() < 0.25:
            manager.mark_dirty(block_num)
        
        # In tổng quan trạng thái sau mỗi block request theo yêu cầu bài toán
        manager.print_state()
        
    # 3. In ra số liệu thống kê cuối cùng cho thuật toán hiện tại
    manager.print_statistics()


def main():
    """Hàm main: Trái tim của phần mềm, nơi mọi thứ bắt đầu."""
    
    # Đề bài yêu cầu chuỗi mô phỏng requests là: [1, 2, 3, 1, 4, 5, 2, 1, 6]
    test_sequence = [1, 2, 3, 1, 4, 5, 2, 1, 6]
    
    # Đề bài yêu cầu kích thước Buffer Pool = 3 frames (0, 1, 2)
    pool_size = 3
    
    # Cố định random seed (hạt giống) để lúc nào chạy ra kết quả khối Dirty cũng giống nhau.
    # Việc cố định này giúp thực hành Unit Test hay giải thích cho Intern dễ dàng, nhất quán. 
    random.seed(42)  
    
    # -- CHẠY LẦN 1: Thuật toán LRU (Least Recently Used) --
    run_simulation("LRU", test_sequence, pool_size)
    
    # -- CHẠY LẦN 2: Thuật toán MRU (Most Recently Used) --
    # Sẽ thấy khác biệt ở frame bị đẩy (victim) khi bộ nhớ đầy. MRU đẩy thằng truy cập sát nhất.
    run_simulation("MRU", test_sequence, pool_size)


# Cấu trúc phổ biến để chạy hàm main() ở Python
if __name__ == "__main__":
    main()
