# Mô phỏng Bộ Quản lý Bộ đệm (DBMS Buffer Manager Simulation)

Dự án này là một chương trình mô phỏng hoạt động của trình quản lý bộ đệm (Buffer Manager) trong các hệ quản trị cơ sở dữ liệu (DBMS). Chương trình quản lý vùng nhớ đệm (Buffer Pool) và sử dụng các thuật toán thay thế trang (Page/Block Replacement Algorithms) khác nhau khi vùng nhớ đệm đầy.

## 🌟 Các tính năng chính

- **Quản lý Buffer Pool**: Xử lý các yêu cầu (requests) nạp các block (khối dữ liệu) từ đĩa vào bộ nhớ đệm (vào các frame).
- **Thuật toán thay thế**: Hỗ trợ hai thuật toán phổ biến:
  - **LRU (Least Recently Used)**: Thay thế block ít được sử dụng nhất trong thời gian gần đây nhất.
  - **MRU (Most Recently Used)**: Thay thế block vừa mới được sử dụng gần đây nhất.
- **Trạng thái Block**: Quản lý các trạng thái quan trọng như:
  - `Pin` / `Unpin`: Đánh dấu block đang được sử dụng hoặc đã giải phóng.
  - `Dirty`: Đánh dấu block đã bị chỉnh sửa và cần ghi tiếp xuống đĩa (Disk) trước khi bị đẩy ra khỏi Buffer Pool (Eviction).
- **Thống kê chuyên sâu**: Theo dõi và in ra số liệu thống kê về quá trình hoạt động: số lần Hit (tìm thấy trong đệm), Miss (phải tải từ đĩa), và số lần ghi (write ra đĩa do block bị thay thế ở trạng thái Dirty).

## 📁 Cấu trúc thư mục dự án

- **`main.py`**: Điểm bắt đầu (entry point) của hệ thống. Chạy bộ mô phỏng với chuỗi yêu cầu test cố định và In ra kết quả chi tiết.
- **`buffer_pool.py`**: Chứa lớp `BufferPool` đóng vai trò là Buffer Manager, quản lý tập hợp các Buffer Frame và điều phối thuật toán thay thế.
- **`buffer_frame.py`**: Chứa lớp khung đệm (frame) để bọc lấy block và quản lý bộ đếm pin (pin count), cờ dirty file.
- **`block.py`**: Chứa thông tin về dữ liệu khối (khối ID, dữ liệu cụ thể, v.v.).
- **`replacement_policy.py`**: Chứa class/interface định nghĩa chuẩn mực cho thuật toán thay thế block để các thuật toán chi tiết kế thừa.
- **`lru_replacement.py`**: Cài đặt chi tiết cho thuật toán thay thế LRU.
- **`mru_replacement.py`**: Cài đặt chi tiết cho thuật toán thay thế MRU.

## 🚀 Hướng dẫn cài đặt và sử dụng

### 1. Yêu cầu hệ thống
- Máy tính cài đặt **Python 3.x** trở lên. (Không yêu cầu thêm thư viện ngoài).

### 2. Cách chạy mô phỏng
Mở Terminal / Command Prompt tại thư mục dự án (`d:\Database`) và gõ lệnh sau:

```bash
python main.py
```

### 3. Hiểu kết quả mô phỏng
Phiên bản hiện tại trong `main.py` sẽ thực thi một chuỗi yêu cầu giả lập: `[1, 2, 3, 1, 4, 5, 2, 1, 6]` với giới hạn Buffer Pool là **3 frames**. Trình mô phỏng sẽ:
1. Chạy qua từng requests với thuật toán **LRU**.
2. Ngay sau đó thiết lập lại và chạy cùng requests trên nhưng với thuật toán **MRU**.
3. Tại mỗi bước, in ra trạng thái hiện tại của buffer, thuật toán đang chọn Victim nào (nếu bị đầy), và tóm tắt thông số Hit/Miss cùng thao tác Disk I/O ở cuối. Tỉ lệ frame bị đánh dấu là `Dirty` (bị sửa đổi) sẽ được mô phỏng ngẫu nhiên (sát suất khoảng 25%).

---
*Dự án này là minh hoạ về cách tổ chức mô phỏng cơ chế cấp phát, duy trì và thay thế bộ nhớ trong máy tính và DBMS. Mã nguồn được viết bằng Python bám sát theo các quy chuẩn Lập trình Hướng Đối tượng (OOP) nhằm mục đích giáo dục và tra cứu.*
