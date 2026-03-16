# D:/Database/block.py

class Block:
    """
    Lớp Block đại diện cho một khối dữ liệu trên đĩa phân trang (disk block).
    Mỗi block có một định danh duy nhất (block_id) để Buffer Manager có thể tìm kiếm.
    """
    def __init__(self, block_id):
        # Lưu trữ ID của khối dữ liệu (ví dụ: 1, 2, 3...)
        self.block_id = block_id
