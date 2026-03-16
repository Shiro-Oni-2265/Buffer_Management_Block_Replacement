# D:/Database/mru_replacement.py
from replacement_policy import ReplacementPolicy

class MRUReplacement(ReplacementPolicy):
    """
    Lớp MRUReplacement (Most Recently Used) kế thừa từ ReplacementPolicy.
    Thuật toán MRU đối nghịch với LRU, nó sẽ đuổi block MỚI VỪA ĐƯỢC SỬ DỤNG GẦN NHẤT.
    Thường hiệu quả trong các truy vấn lặp (loop) trên một tập data lớn hơn buffer.
    """
    def choose_victim(self, frames):
        """
        Tìm frame nạn nhân theo chiến lược vừa truy cập gần nhất (Most Recently Used).
        
        Cách xác định:
        Duyệt qua toàn bộ frame, tìm `last_used_time` lớn nhất (tức là mới nhất),
        điều kiện bắt buộc vẫn là không rỗng và `pin_count` = 0.
        """
        victim_index = -1
        # Gán thời gian lớn nhất ban đầu là -1
        max_time = -1
        
        for i, frame in enumerate(frames):
            # Không thay thế các frame đang được sử dụng (pin_count > 0)
            if frame.block_id is not None and frame.pin_count == 0:
                # Nhắm vào block vừa được dùng mới nhất (last_used_time bự nhất)
                if frame.last_used_time > max_time:
                    max_time = frame.last_used_time
                    victim_index = i
                    
        return victim_index
