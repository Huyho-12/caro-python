<div align="center">

# 🎮 Caro Game - Python Client-Server

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Database](https://img.shields.io/badge/database-MySQL-orange.svg)](https://www.mysql.com/)
[![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey.svg)](https://github.com)

**Trò chơi Caro (Gomoku) multiplayer với AI thông minh, kiến trúc client-server hiện đại**

[Tính năng](#-tính-năng) •
[Cài đặt](#-cài-đặt) •
[Sử dụng](#-sử-dụng) •
[Tài liệu](#-tài-liệu) •
[Screenshots](#-screenshots)

</div>

---

## ✨ Tính năng

### 🖥️ Server Side
- ✅ **Multi-threaded Server** - Xử lý nhiều client đồng thời
- ✅ **Room Management** - Tạo, vào, rời phòng chơi
- ✅ **User Authentication** - Đăng nhập/đăng ký với MySQL
- ✅ **Game State Management** - Quản lý trạng thái game real-time
- ✅ **Statistics Tracking** - Lưu thống kê thắng/thua/hòa
- ✅ **Socket Communication** - Protocol messaging system
- ✅ **Database Integration** - MySQL với mysql-connector-python

### 💻 Client Side
- ✅ **Tkinter GUI** - Giao diện đồ họa thân thiện
- ✅ **Login/Register** - Quản lý tài khoản người chơi
- ✅ **Room System** - Tạo phòng (có/không mật khẩu), xem danh sách phòng
- ✅ **Game Board 15x15** - Caro board với win condition: 5 in a row
- ✅ **Real-time Updates** - Cập nhật nước đi đối thủ ngay lập tức
- ✅ **Chat System** - Chat trong game với đối thủ
- ✅ **User Statistics** - Xem thống kê cá nhân (wins, draws, games)
- ✅ **AI Opponent** - Chơi với AI thông minh (3 độ khó)

### 🤖 AI Features
- ✅ **Minimax Algorithm** - Thuật toán tìm kiếm nước đi tốt nhất
- ✅ **Alpha-Beta Pruning** - Tối ưu hóa performance
- ✅ **3 Difficulty Levels**:
  - **Easy** (Depth 1) - Cho người mới
  - **Medium** (Depth 2) - Thách thức vừa phải
  - **Hard** (Depth 3) - Đối thủ mạnh

### 🌐 Network Features
- ✅ **LAN/WiFi Multiplayer** - Chơi qua mạng local
- ✅ **Multiple Clients** - Nhiều client trên cùng 1 máy
- ✅ **Configurable IP** - Dễ dàng config qua `network_config.py`
- ✅ **Error Handling** - Xử lý mất kết nối, timeout

---

## 📸 Screenshots

> **Lưu ý**: Screenshots có trong thư mục `docs/images/` (xem hướng dẫn chụp ảnh tại `docs/QUICKSTART_SCREENSHOTS.md`)

### Các màn hình chính

| Màn hình | Mô tả |
|----------|-------|
| **Login** | Đăng nhập tài khoản |
| **Register** | Đăng ký tài khoản mới |
| **Home/Lobby** | Trang chủ với danh sách phòng, tạo phòng, chơi AI |
| **Game Multiplayer** | Màn hình chơi game 2 người |
| **Game AI** | Màn hình chơi với AI |
| **Game Result** | Hiển thị kết quả (Win/Lose/Draw) |

### Chế độ chơi

| Mode | Description | Board Size | Status |
|------|-------------|------------|--------|
| 🤖 **AI Mode** | Chơi với AI (Easy/Medium/Hard) | 15x15 | ✅ Hoàn thành |
| 👥 **Multiplayer** | Chơi với người khác (Local/Online) | 15x15 | ✅ Hoàn thành |
| 🏠 **Practice** | Luyện tập offline | 15x15 | ✅ Hoàn thành |

---

## 🛠️ Tech Stack

<table>
<tr>
<td>

**Backend**
- 🐍 Python 3.8+
- 🗄️ MySQL 8.0+
- 🔌 Socket Programming
- 🧵 Multi-threading
- 📦 mysql-connector-python

</td>
<td>

**Frontend**
- 🖼️ Tkinter GUI
- 🎨 Custom Components
- 📊 Real-time Updates
- ⚡ Queue-based Events

</td>
<td>

**AI & Algorithms**
- 🤖 Minimax Algorithm
- ✂️ Alpha-Beta Pruning
- 🎯 Heuristic Evaluation
- ⚡ Move Optimization

</td>
</tr>
</table>

### Kiến trúc hệ thống

```
┌───────────────────────────────────────────────────────────────┐
│                    CARO GAME ARCHITECTURE                      │
├───────────────────────────────────────────────────────────────┤
│                                                                │
│  ┌──────────────┐              ┌──────────────┐              │
│  │  CLIENT 1    │◄────────────►│              │              │
│  │  (Tkinter)   │   TCP/IP     │              │              │
│  └──────────────┘   Port 7777  │    SERVER    │◄────► MySQL │
│        │                        │              │    Database │
│   [AI Engine]                   │  (Python)    │              │
│   [Minimax]                     └──────────────┘              │
│                                        ▲                       │
│  ┌──────────────┐                     │                       │
│  │  CLIENT 2    │◄────────────────────┘                       │
│  │  (Tkinter)   │      Thread per Client                      │
│  └──────────────┘                                             │
│                                                                │
│  Components:                                                  │
│  • Client: Socket Handler, Views (Login, Home, Game)         │
│  • Server: ServerThread, Room Manager, User DAO               │
│  • Shared: User Model, Room Model, Constants                  │
│                                                                │
└───────────────────────────────────────────────────────────────┘
```

> Xem thêm chi tiết: `docs/ARCHITECTURE.md`

---

## 📋 Yêu cầu hệ thống

### Phần mềm bắt buộc
- **Python:** 3.8+ ([Download](https://www.python.org/downloads/))
- **MySQL:** 8.0+ (XAMPP khuyên dùng - [Download](https://www.apachefriends.org/))
- **Git:** Để clone repository ([Download](https://git-scm.com/))

### Phần cứng tối thiểu
- **CPU:** Dual-core 1.0 GHz
- **RAM:** 512 MB
- **Disk:** 100 MB khả dụng
- **Network:** LAN/WiFi (cho multiplayer)

### Hệ điều hành hỗ trợ
- ✅ Windows 10/11
- ✅ Linux (Ubuntu 18.04+)
- ✅ macOS 10.14+

---

## 🚀 Cài đặt

### Bước 1: Clone repository

```bash
git clone https://github.com/Huyho-12/caro-python.git
cd caro-python
```

### Bước 2: Cài đặt thư viện

```bash
pip install -r requirements.txt
```

### Bước 3: Cài đặt MySQL

**Windows (XAMPP):**
1. Tải XAMPP từ [https://www.apachefriends.org/](https://www.apachefriends.org/)
2. Cài đặt và khởi động MySQL từ XAMPP Control Panel

**Linux:**
```bash
sudo apt-get install mysql-server
sudo systemctl start mysql
```

**macOS:**
```bash
brew install mysql
brew services start mysql
```

### Bước 4: Cấu hình Database

**Tùy chọn 1: Tự động (Khuyên dùng)**
```bash
python create_database.py
```

Script sẽ tự động:
- ✅ Kết nối MySQL (localhost, user: root, no password)
- ✅ Tạo database `caro_game`
- ✅ Tạo bảng `user` với đầy đủ fields
- ✅ Thêm sample accounts

**Tùy chọn 2: Thủ công**
```sql
-- Mở MySQL Command Line hoặc phpMyAdmin
CREATE DATABASE caro_game;
USE caro_game;

CREATE TABLE user (
    id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(50) UNIQUE NOT NULL,
    nickname VARCHAR(50) NOT NULL,
    password VARCHAR(255) NOT NULL,
    num_wins INT DEFAULT 0,
    num_draws INT DEFAULT 0,
    num_games INT DEFAULT 0
);
```

### Bước 5: Cấu hình Network (Cho multiplayer online)

**Chơi trên 1 máy:** Dùng localhost (mặc định) - Bỏ qua bước này

**Chơi trên 2+ máy khác nhau:**

1. **Trên máy Server**: Kiểm tra IP
```bash
python check_ip.py
# Output: Your IP: 192.168.1.100
```

2. **Trên máy Client**: Sửa `network_config.py`
```python
SERVER_IP = "192.168.1.100"  # IP của máy server
SERVER_PORT = 7777            # Mặc định 7777
```

> **Lưu ý**: Đảm bảo firewall cho phép port 7777

---

## 🎮 Sử dụng

### 1️⃣ Khởi động Server

Mở terminal/cmd và chạy:

```bash
cd caro-python
python server/server.py
```

**Output mong đợi:**
```
==================================================
Caro Game Server
==================================================
Database connection successful
Server started on 0.0.0.0:7777
Waiting to accept users...
==================================================
```

### 2️⃣ Khởi động Client

**Mở terminal MỚI** (giữ server chạy), sau đó:

```bash
python client/main.py
```

Cửa sổ game sẽ mở với màn hình đăng nhập.

### 3️⃣ Hướng dẫn sử dụng

#### Đăng nhập/Đăng ký
- **Đăng nhập**: Nhập username/password → Click "Đăng nhập"
- **Đăng ký**: Click "Chưa có tài khoản? Đăng ký" → Điền form → Click "Đăng ký"

#### Chơi với AI
1. Từ màn hình Home, click **"Chơi với AI"**
2. Chọn độ khó: Easy / Medium / Hard
3. Click vào ô để đánh
4. Win condition: 5 quân liên tiếp (ngang/dọc/chéo)

#### Multiplayer Online
1. **Player 1**: Click "Tạo phòng" → Nhập tên phòng → (Tùy chọn: mật khẩu)
2. **Player 2**: Chọn phòng từ danh sách → Click "Vào phòng"
3. Game tự động bắt đầu khi đủ 2 người

**Board:** 20x20 ô  
**Win:** 5 quân liên tiếp  
**Chat:** Gửi tin nhắn cho đối thủ trong game

---

## 🌐 Multiplayer trên 2 máy

### Máy Server (Host game)

```bash
# Bước 1: Xem IP của máy
python check_ip.py
# Output: Your IP: 192.168.1.100

# Bước 2: Khởi động server
python server/server.py
```

### Máy Client (Join game)

```bash
# Bước 1: Cấu hình IP server
# Sửa file network_config.py:
SERVER_IP = "192.168.1.100"  # IP máy server từ bước trên

# Bước 2: Khởi động client
python client/main.py
```

> **Lưu ý**: 
> - Cả 2 máy phải cùng mạng LAN/WiFi
> - Firewall phải cho phép port 7777
> - Chi tiết: [MULTIPLAYER_GUIDE.md](MULTIPLAYER_GUIDE.md)

---

## 📁 Cấu trúc dự án

```
caro-python/
├── 📂 server/                     # Server-side code
│   ├── server.py                  # Main server, accept connections
│   ├── server_thread.py           # Handle each client in separate thread
│   ├── room.py                    # Room management (create, join, leave)
│   ├── user_dao.py                # Database access layer (MySQL)
│   └── config.py                  # Database & server configuration
│
├── 📂 client/                     # Client-side code
│   ├── main.py                    # Entry point, start client app
│   ├── client.py                  # Main client controller
│   ├── socket_handle.py           # Socket communication handler
│   ├── ai_player.py               # AI opponent (Minimax algorithm)
│   └── 📁 views/                  # GUI components (Tkinter)
│       ├── login_view.py          # Login screen
│       ├── register_view.py       # Registration screen
│       ├── home_view.py           # Main lobby
│       ├── game_view.py           # Multiplayer game board
│       └── game_ai_view.py        # AI game board
│
├── 📁 shared/                     # Shared modules
│   ├── models.py                  # Data models (User, Point)
│   └── constants.py               # Protocol constants & messages
│
├── 📁 docs/                       # Technical documentation
│   ├── README.md                  # Documentation index
│   ├── ARCHITECTURE.md            # System architecture
│   ├── FLOWCHARTS.md              # Process flowcharts
│   ├── PSEUDO_CODE.md             # Algorithm pseudo code
│   ├── PLANTUML_INDEX.md          # UML diagrams index
│   └── plantuml/                  # PlantUML diagram files
│
├── 📁 assets/                     # Resources
│
├── 🛠️ Utilities
│   ├── network_config.py          # Network IP configuration
│   ├── check_ip.py                # Check local IP address
│   ├── create_database.py         # Auto database setup
│   └── requirements.txt           # Python dependencies
│
└── 📄 Documentation
    ├── README.md                  # This file - Main documentation
    ├── QUICKSTART.md              # 5-minute quick start guide
    ├── INSTALL.md                 # Detailed installation guide
    ├── MULTIPLAYER_GUIDE.md       # LAN/WiFi setup guide
    └── CHANGELOG.md               # Version history
```

---

## 📚 Tài liệu

| Tài liệu | Mô tả |
|----------|-------|
| [QUICKSTART.md](QUICKSTART.md) | 🚀 Hướng dẫn nhanh 5 phút |
| [INSTALL.md](INSTALL.md) | 📦 Hướng dẫn cài đặt chi tiết |
| [MULTIPLAYER_GUIDE.md](MULTIPLAYER_GUIDE.md) | 🌐 Hướng dẫn chơi qua LAN/WiFi |
| [CHANGELOG.md](CHANGELOG.md) | 📝 Lịch sử phiên bản & cập nhật |

---

## 🎯 API & Lệnh

### Lệnh nhanh

```bash
# Phát triển
python check_ip.py              # Kiểm tra địa chỉ IP của máy
python create_database.py       # Tự động thiết lập database

# Chạy
python server/server.py         # Khởi động server
python client/main.py           # Khởi động client

# Kiểm thử
python -m pytest tests/         # Chạy unit tests (nếu có)
```

### Cấu hình Server

File: `server/config.py`
```python
DB_CONFIG = {
    'host': 'localhost',          # MySQL host
    'user': 'root',                # Tên đăng nhập MySQL  
    'password': '',                # Mật khẩu MySQL (để trống cho XAMPP)
    'database': 'caro_game'        # Tên database
}

SERVER_HOST = '0.0.0.0'           # Lắng nghe trên tất cả giao diện mạng
SERVER_PORT = 7777                # Cổng server
MAX_CLIENTS = 50                  # Số lượng client tối đa
```

### Cấu hình Client

File: `network_config.py`
```python
SERVER_IP = "127.0.0.1"           # IP server (localhost)
SERVER_PORT = 7777                # Cổng server (phải khớp với server)
```

---

## 🐛 Khắc phục sự cố

<details>
<summary><strong>❌ Kết nối Database thất bại</strong></summary>

**Vấn đề:** `Can't connect to MySQL server`

**Giải pháp:**
1. Khởi động MySQL/XAMPP:
   ```bash
   # Windows: Mở XAMPP Control Panel → Start MySQL
   # Linux: sudo systemctl start mysql
   ```
2. Kiểm tra thông tin đăng nhập trong `server/config.py`
3. Tạo database:
   ```bash
   python create_database.py
   ```
4. Kiểm tra MySQL đang chạy:
   ```bash
   netstat -ano | findstr 3306
   ```

</details>

<details>
<summary><strong>❌ Kết nối Server timeout</strong></summary>

**Vấn đề:** Client không thể kết nối đến server

**Giải pháp:**
1. Xác nhận server đang chạy
2. Kiểm tra `network_config.py` có IP đúng
3. Tạm thời tắt Firewall hoặc cho phép cổng 7777
4. Kiểm tra kết nối:
   ```bash
   ping 192.168.1.100  # Thay bằng IP server
   telnet 192.168.1.100 7777
   ```

</details>

<details>
<summary><strong>⚠️ AI chậm</strong></summary>

**Vấn đề:** AI mất quá nhiều thời gian để đi nước

**Giải pháp:**
- Dùng độ khó "Trung bình" (khuyên dùng)
- Độ khó "Khó" có thể mất 3-5 giây
- Đảm bảo CPU đáp ứng yêu cầu

</details>

<details>
<summary><strong>⚠️ Giao diện không phản hồi</strong></summary>

**Vấn đề:** Cửa sổ bị đơ hoặc không cập nhật

**Giải pháp:**
1. Đóng và khởi động lại client
2. Kiểm tra logs của server
3. Xác nhận Python 3.8+ đã cài đặt
4. Cập nhật Tkinter:
   ```bash
   # Linux
   sudo apt-get install python3-tk
   ```

</details>

---

## 🎯 Điểm nổi bật & Tính năng

### 🤖 AI thông minh
- **Thuật toán:** Minimax với Alpha-Beta Pruning
- **Độ khó:** Dễ (ngẫu nhiên), Trung bình (độ sâu 2), Khó (độ sâu 3)
- **Tối ưu hóa:** Sắp xếp nước đi, đánh giá heuristic, chọn nước đi thông minh
- **Hiệu năng:** Thời gian phản hồi < 2s trên phần cứng trung bình

### 🌐 Mạng
- **Giao thức:** Giao thức socket tùy chỉnh
- **Kiến trúc:** Server đa luồng với ThreadPoolExecutor
- **Khả năng mở rộng:** Hỗ trợ 50+ client đồng thời
- **Tính năng:** Quản lý phòng, xác thực người dùng, cập nhật real-time

### 🎨 Trải nghiệm người dùng
- **Framework GUI:** Tkinter với các component tùy chỉnh
- **Phản hồi nhanh:** Xử lý sự kiện dựa trên Queue để UI mượt mà
- **Trực quan:** Điều hướng đơn giản, chỉ báo trạng thái game rõ ràng
- **Tùy chỉnh:** Dễ dàng mở rộng và sửa đổi

---

## 💡 Đóng góp

Chúng tôi hoan nghênh mọi đóng góp! Đây là cách bạn có thể giúp đỡ:

1. **Báo lỗi:** Mở issue với mô tả chi tiết
2. **Đề xuất tính năng:** Chia sẻ ý tưởng của bạn trong issues
3. **Gửi Pull Request:** Fork, tạo branch, commit, push, PR
4. **Cải thiện tài liệu:** Sửa lỗi chính tả, thêm ví dụ
5. **Chia sẻ:** Star ⭐ dự án và chia sẻ với bạn bè!

### Thiết lập môi trường phát triển

```bash
git clone https://github.com/Huyho-12/caro-python.git
cd caro-python
pip install -r requirements.txt
python create_database.py
```

### Quy tắc code
- Tuân thủ hướng dẫn PEP 8
- Thêm docstrings cho các hàm
- Comment các logic phức tạp
- Kiểm thử trước khi commit

---

## 📊 Trạng thái dự án

| Tính năng | Trạng thái | Phiên bản |
|-----------|-----------|-----------|
| Core Game Engine | ✅ Hoàn thành | 2.0.0 |
| AI Player | ✅ Hoàn thành | 2.0.0 |
| Multiplayer (LAN) | ✅ Hoàn thành | 2.0.0 |
| User Authentication | ✅ Hoàn thành | 2.0.0 |
| Room Management | ✅ Hoàn thành | 2.0.0 |
| Friend System | 🚧 Đang phát triển | TBD |
| Tournament Mode | 📋 Đã lên kế hoạch | TBD |
| Sound Effects | 📋 Đã lên kế hoạch | TBD |
| Online Multiplayer | 📋 Đã lên kế hoạch | TBD |

---

## 🙏 Lời cảm ơn

- **Python Community** - Thư viện tuyệt vời và sự hỗ trợ
- **MySQL** - Hệ thống database đáng tin cậy
- **Tkinter** - Framework GUI đơn giản nhưng mạnh mẽ
- **Minimax Algorithm** - Nền tảng của trí tuệ AI

---

## 📄 Giấy phép

```
Giấy phép MIT

Bản quyền (c) 2025 Caro Game Python

Cho phép miễn phí bất kỳ ai có được bản sao phần mềm này và các tệp tài liệu
liên quan ("Phần mềm"), để xử lý Phần mềm không bị hạn chế, bao gồm nhưng
không giới hạn quyền sử dụng, sao chép, sửa đổi, hợp nhất, xuất bản, phân phối,
cấp phép phụ và/hoặc bán bản sao của Phần mềm, và cho phép những người được
cung cấp Phần mềm được phép làm như vậy, với các điều kiện sau:

Thông báo bản quyền ở trên và thông báo cho phép này phải được bao gồm trong
tất cả các bản sao hoặc phần quan trọng của Phần mềm.

PHẦN MỀM ĐƯỢC CUNG CẤP "NGUYÊN BẢN", KHÔNG CÓ BẤT KỲ BẢO ĐẢM NÀO, RÕ RÀNG
HOẶC NGỤ Ý, BAO GỒM NHƯNG KHÔNG GIỚI HẠN BẢO ĐẢM VỀ KHẢ NĂNG BÁN ĐƯỢC, PHÙ
HỢP CHO MỤC ĐÍCH CỤ THỂ VÀ KHÔNG VI PHẠM.
```

---

<div align="center">

**Được tạo với ❤️ và ☕**

⭐ Star dự án này nếu bạn thấy hữu ích!

[⬆ Về đầu trang](#-caro-game---python-client-server)

</div>
