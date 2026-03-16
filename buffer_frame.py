# D:/Database/buffer_frame.py

class BufferFrame:
    """
    Lớp BufferFrame đóng vai trò như một ô (slot/frame) trong bộ nhớ đệm (Buffer Pool).
    Mỗi khung có thể chứa đúng một Block dữ liệu tại một thời điểm nhất định.
    """
    def __init__(self):
        # Chứa ID của block đang nằm trong frame này, nếu rỗng thì bằng None
        self.block_id = None
        
        # Cờ đánh dấu block có bị sửa đổi hay không (Dirty flag).
        # Nếu True (đã sửa), thì lúc bị đẩy ra khỏi bộ nhớ (replace), 
        # phải ghi lại (write back) những thay đổi đó xuống đĩa cứng.
        self.dirty = False
        
        # Biến đếm số lượng người/tiến trình đang dùng (pin) block này.
        # Nếu pin_count > 0, nghĩa là block đang được sử dụng và KHÔNG ĐƯỢC PHÉP bị thay thế.
        self.pin_count = 0
        
        # Biến lưu trữ lại mốc thời gian (hoặc request id) gần nhất block này được dùng.
        # Rất quan trọng cho các thuật toán thay thế như LRU (Least Recently Used) hay MRU.
        self.last_used_time = 0
