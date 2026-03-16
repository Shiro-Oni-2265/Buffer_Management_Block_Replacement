# D:/Database/replacement_policy.py

class ReplacementPolicy:
    """
    Lớp cơ sở (Base class) định nghĩa khuôn mẫu cho các thuật toán thay thế block.
    Sử dụng OOP Inheritance (Tính kế thừa) để các lớp thuật toán con ghi đè.
    """
    def choose_victim(self, frames):
        """
        Phương thức này sẽ chọn ra một BufferFrame làm "nạn nhân" (victim)
        để loại bỏ khỏi Buffer Pool khi bộ nhớ đã đầy.
        
        Tham số:
            frames: Danh sách các đối tượng BufferFrame trong Buffer Pool hiện tại.
            
        Trả về:
            Chỉ số (index) của frame sẽ bị thay thế. Trả về -1 nếu không có frame phù hợp.
        """
        # Phương thức này cố tình để nguyên để các lớp con (LRU, MRU) tự triển khai (Override).
        raise NotImplementedError("Cần phải được triển khai bởi lớp con (Subclass)!")
