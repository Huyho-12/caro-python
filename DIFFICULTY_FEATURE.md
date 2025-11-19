# Tính năng chỉnh độ khó AI - Caro Game

## 📋 Tổng quan

Đã nâng cấp tính năng chọn và thay đổi độ khó AI với giao diện đẹp mắt và trải nghiệm người dùng tốt hơn.

## ✨ Các cải tiến

### 1. **Hộp thoại chọn độ khó khi bắt đầu chơi**
- Khi nhấn nút "🤖 Chơi với AI" từ trang chủ, xuất hiện hộp thoại chọn độ khó
- Hiển thị đầy đủ thông tin về từng mức độ khó
- Giao diện đẹp mắt với màu sắc phân biệt rõ ràng

### 2. **Cải thiện giao diện trong game**
- Hiển thị độ khó hiện tại với màu sắc và biểu tượng emoji
- Badge màu động thay đổi theo độ khó:
  - 😊 Dễ: Màu xanh lá (#4CAF50)
  - 😐 Trung bình: Màu cam (#FF9800)
  - 😤 Khó: Màu đỏ (#f44336)

### 3. **Nâng cấp hộp thoại đổi độ khó**
- Hiển thị độ khó hiện tại
- Mô tả chi tiết từng độ khó
- Đánh dấu độ khó đang chơi với "✓ ĐANG CHƠI"
- Thông báo khi chọn độ khó đã đang chơi
- Tự động bắt đầu ván mới sau khi đổi độ khó

## 🎮 Các độ khó

| Độ khó | Biểu tượng | Mô tả | Thuật toán |
|--------|-----------|-------|-----------|
| **Dễ** | 😊 | AI đánh ngẫu nhiên - Phù hợp người mới | Random move |
| **Trung bình** | 😐 | AI thông minh (độ sâu 2) - Khuyên dùng | Minimax depth 2 |
| **Khó** | 😤 | AI cao cấp (độ sâu 3) - Thử thách lớn | Minimax depth 3 |

## 📸 Hướng dẫn sử dụng

### Cách 1: Chọn độ khó khi bắt đầu
1. Từ trang chủ, nhấn nút **"🤖 Chơi với AI"**
2. Chọn một trong ba độ khó:
   - 😊 Dễ
   - 😐 Trung bình
   - 😤 Khó
3. Game sẽ bắt đầu với độ khó đã chọn

### Cách 2: Đổi độ khó trong khi chơi
1. Trong game AI, nhấn nút **"⚙️ Đổi độ khó"**
2. Xem độ khó hiện tại (được đánh dấu "✓ ĐANG CHƠI")
3. Chọn độ khó mới
4. Ván mới sẽ tự động bắt đầu

## 🔧 Chi tiết kỹ thuật

### Files được chỉnh sửa:

#### 1. `client/views/home_view.py`
- **Hàm mới**: `center_dialog()` - Căn giữa hộp thoại
- **Cải tiến**: `play_with_ai()` - Hiển thị hộp thoại chọn độ khó thay vì mở game trực tiếp

#### 2. `client/views/game_ai_view.py`
- **Cải tiến**: `create_top_info()` - Thêm difficulty badge với màu sắc động
- **Cải tiến**: `change_difficulty()` - Nâng cấp hoàn toàn giao diện và logic
- **Tính năng mới**: 
  - Hiển thị độ khó hiện tại
  - Đánh dấu độ khó đang chơi
  - Cảnh báo khi chọn lại độ khó đang chơi
  - Cập nhật màu badge khi đổi độ khó

### Cấu trúc màu sắc:
```python
difficulty_colors = {
    "easy": "#4CAF50",    # Xanh lá
    "medium": "#FF9800",  # Cam
    "hard": "#f44336"     # Đỏ
}

difficulty_icons = {
    "easy": "😊",
    "medium": "😐",
    "hard": "😤"
}
```

## 🎯 Tính năng nổi bật

✅ **Modal dialogs** với `transient()` và `grab_set()` để focus tốt hơn  
✅ **Màu sắc trực quan** giúp phân biệt độ khó  
✅ **Biểu tượng emoji** sinh động  
✅ **Mô tả chi tiết** giúp người chơi hiểu rõ từng độ khó  
✅ **Feedback tức thì** khi đổi độ khó  
✅ **Tự động reset** game khi đổi độ khó  
✅ **Ngăn chặn duplicate choice** - cảnh báo khi chọn lại độ khó hiện tại  

## 🚀 Cách chạy

```bash
# Khởi động server (terminal 1)
python server/server.py

# Khởi động client (terminal 2)
python client/main.py
```

Sau đó:
1. Đăng nhập với tài khoản (ví dụ: `player1` / `player1`)
2. Nhấn nút **"🤖 Chơi với AI"**
3. Chọn độ khó và bắt đầu chơi!

## 📝 Ghi chú

- Độ khó có thể thay đổi bất cứ lúc nào trong game
- Mỗi lần đổi độ khó, ván chơi sẽ reset
- Tỉ số giữa các ván được giữ nguyên khi đổi độ khó
- AI "Khó" có thể mất 2-5 giây để suy nghĩ (bình thường)

---

**Phát triển bởi**: GitHub Copilot  
**Ngày cập nhật**: 19/11/2025
