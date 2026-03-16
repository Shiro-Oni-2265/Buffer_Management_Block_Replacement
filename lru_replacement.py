# D:/Database/lru_replacement.py
from replacement_policy import ReplacementPolicy

class LRUReplacement(ReplacementPolicy):
    """
    Lớp LRUReplacement (Least Recently Used) kế thừa từ ReplacementPolicy.
    Thuật toán LRU sẽ chọn block đã LÂU NHẤT CHƯA ĐƯỢC SỬ DỤNG làm nạn nhân.
    """
    def choose_victim(self, frames):
        """
        Tìm frame nạn nhân theo chiến lược chặn ít truy cập gần nhất.
        
        Cách xác định:
        Duyệt qua các frame, tìm frame nào có `last_used_time` nhỏ nhất (tức là cũ nhất),
        với điều kiện frame đó đang chứa block (không rỗng) và `pin_count` bằng 0.
        """
        victim_index = -1
        # Gán thời gian bé nhất ban đầu là vô cực, dùng để làm mốc so sánh dần
        min_time = float('inf')
        
        for i, frame in enumerate(frames):
            # Quy tắc 1 của Buffer Manager: Block bị pin (pin_count > 0) thì không thể thay thế.
            if frame.block_id is not None and frame.pin_count == 0:
                # Nếu thời gian lúc dùng lần cuối nhỏ hơn giá trị min hiện tại
                if frame.last_used_time < min_time:
                    # Cập nhật thời gian nhỏ nhất và lưu index làm nạn nhân
                    min_time = frame.last_used_time
                    victim_index = i
                    
        return victim_index
