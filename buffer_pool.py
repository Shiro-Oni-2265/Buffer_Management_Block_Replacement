# D:/Database/buffer_pool.py
from buffer_frame import BufferFrame

class BufferPool:
    """
    Lớp cốt lõi quản lý Buffer (Bộ đệm dữ liệu trên RAM).
    Xử lý các logic: tìm nạp (load), gỡ bỏ (replace), pin block, mark dirty...
    """
    def __init__(self, pool_size, replacement_policy):
        # pool_size: số lượng frame tối đa
        self.pool_size = pool_size
        
        # Khởi tạo danh sách các frame rỗng tương ứng với pool_size
        self.frames = [BufferFrame() for _ in range(pool_size)]
        
        # Lưu thuật toán thay thế (Ví dụ: truyền vào LRU hoặc MRU)
        self.replacement_policy = replacement_policy
        
        # current_time: Biến đếm thời gian ảo. Cứ mỗi lần request_block, nó sẽ tăng 1.
        self.current_time = 0
        
        # --- Khởi tạo các biến để làm Thống kê (Statistics) theo yêu cầu ---
        self.total_requests = 0     # Tổng số lượt yêu cầu block
        self.hits = 0               # Số lượt tìm thấy block ngay trong buffer (HIT)
        self.misses = 0             # Số lượt không tìm thấy, phải nạp từ disk (MISS)
        self.replaced_blocks = 0    # Số lần bộ nhớ đầy phải thay thế (replace) block cũ
        
    def get_hit_ratio(self):
        """Tính tỉ lệ Hit Ratio = Số lần Hit / Tổng số lần yêu cầu"""
        if self.total_requests == 0:
            return 0.0
        return self.hits / self.total_requests

    def find_block(self, block_id):
        """Hàm công cụ: Tìm một block xem nó đang ở frame (index) nào, không có trả -1."""
        for i, frame in enumerate(self.frames):
            if frame.block_id == block_id:
                return i
        return -1
        
    def find_free_frame(self):
        """Hàm công cụ: Tìm frame đang rỗng chưa chứa block, không có trả về -1."""
        for i, frame in enumerate(self.frames):
            if frame.block_id is None:
                return i
        return -1

    def request_block(self, block_id):
        """
        Logic cốt lõi: Yêu cầu một block từ hệ thống.
        1. Nếu có sẵn (HIT) -> cập nhật thời gian.
        2. Nếu chưa có (MISS) -> nạp vào frame trống.
        3. Nếu đầy -> Gọi thuật toán tìm Victim và đổi chỗ (có thể write dirty to disk).
        """
        self.total_requests += 1
        self.current_time += 1
        
        # TÌM TRONG BỘ NHỚ
        frame_idx = self.find_block(block_id)
        
        if frame_idx != -1: # -----> HIT
            self.hits += 1
            # Cập nhật thời gian sử dụng block để LRU/MRU quản lý chính xác
            self.frames[frame_idx].last_used_time = self.current_time
            print(f"Request Block {block_id} -> HIT")
            return
            
        # NẾU KHÔNG TÌM THẤY -----> MISS
        self.misses += 1
        
        # Tìm xem có chổ trống không
        free_idx = self.find_free_frame()
        
        if free_idx != -1: 
            # ---> CÒN CHỖ TRỐNG: load đè trực tiếp vô
            print(f"Request Block {block_id} -> MISS -> loaded into frame {free_idx}")
            new_frame = self.frames[free_idx]
            new_frame.block_id = block_id
            new_frame.dirty = False
            new_frame.pin_count = 0
            new_frame.last_used_time = self.current_time
            return
            
        # KHÔNG CÒN TRỐNG ---> TÌM NẠN NHÂN ĐỂ THAY THẾ (Buffer Full)
        victim_idx = self.replacement_policy.choose_victim(self.frames)
        
        if victim_idx == -1:
            print(f"LỖI: Tất cả frame đang bị khóa (pinned). Không thể thay thế.")
            return
            
        self.replaced_blocks += 1
        victim = self.frames[victim_idx]
        
        # QUAN TRỌNG: Simulate Write-back
        # "If the victim block is dirty: simulate writing it back to disk and print [...]"
        if victim.dirty:
            print(f"Writing dirty block {victim.block_id} to disk")
            print(f"Write block {victim.block_id} back to disk")
            
        # Lắp Block mới yêu cầu vào Frame vừa đoạt được
        print(f"Request Block {block_id} -> MISS -> Buffer full, replacing Block {victim.block_id} in frame {victim_idx}")
        
        victim.block_id = block_id
        victim.dirty = False
        victim.pin_count = 0
        victim.last_used_time = self.current_time

    def pin_block(self, block_id):
        """Hàm đánh dấu sử dụng. Mỗi lần pin sẽ cộng pin_count lên 1. Block sẽ không bị thay thế."""
        idx = self.find_block(block_id)
        if idx != -1:
            self.frames[idx].pin_count += 1
            
    def unpin_block(self, block_id):
        """Khi dùng xong, gọi unpin để trừ đi pin_count."""
        idx = self.find_block(block_id)
        if idx != -1 and self.frames[idx].pin_count > 0:
            self.frames[idx].pin_count -= 1

    def mark_dirty(self, block_id):
        """Đánh dấu block này đã bị sửa đổi. Trước khi rời buffer phải được ghi đĩa."""
        idx = self.find_block(block_id)
        if idx != -1:
            self.frames[idx].dirty = True

    def print_state(self):
        """In trạng thái các frame trong buffer."""
        print("Buffer State:")
        for i, frame in enumerate(self.frames):
            if frame.block_id is None:
                print(f"Frame {i}: Empty")
            else:
                dirty_str = " (Dirty)" if frame.dirty else ""
                pin_str = f" [Pin: {frame.pin_count}]" if frame.pin_count > 0 else ""
                print(f"Frame {i}: Block {frame.block_id}{dirty_str}{pin_str}")
        print("-" * 30)

    def print_statistics(self):
        """In tổng hợp các dữ liệu thống kê khi kết thúc."""
        print("\n=== Buffer Pool Statistics ===")
        print(f"- Total requests: {self.total_requests}")
        print(f"- Hits: {self.hits}")
        print(f"- Misses: {self.misses}")
        # Định dạng in float lấy 2 chữ số thập phân
        print(f"- Hit ratio: {self.get_hit_ratio():.2f}")
        print(f"- Number of replaced blocks: {self.replaced_blocks}")
        print("==============================")
