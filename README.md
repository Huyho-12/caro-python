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

## 📚 Documentation

| Document | Description |
|----------|-------------|
| [QUICKSTART.md](QUICKSTART.md) | 🚀 5-minute quick start guide |
| [INSTALL.md](INSTALL.md) | 📦 Detailed installation instructions |
| [MULTIPLAYER_GUIDE.md](MULTIPLAYER_GUIDE.md) | 🌐 LAN/WiFi multiplayer setup |
| [CHANGELOG.md](CHANGELOG.md) | 📝 Version history & updates |

---

## 🎯 API & Commands

### Quick Commands

```bash
# Development
python check_ip.py              # Check machine IP address
python create_database.py       # Setup database automatically

# Running
python server/server.py         # Start game server
python client/main.py           # Start game client

# Testing
python -m pytest tests/         # Run unit tests (if available)
```

### Server Configuration

File: `server/config.py`
```python
DB_CONFIG = {
    'host': 'localhost',          # MySQL host
    'user': 'root',                # MySQL username  
    'password': '',                # MySQL password (empty for XAMPP)
    'database': 'caro_game'        # Database name
}

SERVER_HOST = '0.0.0.0'           # Listen on all interfaces
SERVER_PORT = 7777                # Server port
MAX_CLIENTS = 50                  # Max concurrent clients
```

### Client Configuration

File: `network_config.py`
```python
SERVER_IP = "127.0.0.1"           # Server IP (localhost)
SERVER_PORT = 7777                # Server port (must match server)
```

---

## 🐛 Troubleshooting

<details>
<summary><strong>❌ Database Connection Failed</strong></summary>

**Problem:** `Can't connect to MySQL server`

**Solutions:**
1. Start MySQL/XAMPP:
   ```bash
   # Windows: Open XAMPP Control Panel → Start MySQL
   # Linux: sudo systemctl start mysql
   ```
2. Verify credentials in `server/config.py`
3. Create database:
   ```bash
   python create_database.py
   ```
4. Check MySQL is running:
   ```bash
   netstat -ano | findstr 3306
   ```

</details>

<details>
<summary><strong>❌ Server Connection Timeout</strong></summary>

**Problem:** Client can't connect to server

**Solutions:**
1. Verify server is running
2. Check `network_config.py` has correct IP
3. Disable Firewall temporarily or allow port 7777
4. Test connection:
   ```bash
   ping 192.168.1.100  # Replace with server IP
   telnet 192.168.1.100 7777
   ```

</details>

<details>
<summary><strong>⚠️ AI Too Slow</strong></summary>

**Problem:** AI takes too long to make a move

**Solutions:**
- Use "Medium" difficulty (recommended)
- "Hard" difficulty may take 3-5 seconds
- Ensure your CPU meets requirements

</details>

<details>
<summary><strong>⚠️ GUI Not Responding</strong></summary>

**Problem:** Window freezes or doesn't update

**Solutions:**
1. Close and restart client
2. Check server logs for errors
3. Verify Python 3.8+ is installed
4. Update Tkinter:
   ```bash
   # Linux
   sudo apt-get install python3-tk
   ```

</details>

---

## 🎯 Highlights & Features

### 🤖 Intelligent AI
- **Algorithm:** Minimax with Alpha-Beta Pruning
- **Difficulty Levels:** Easy (random), Medium (depth 2), Hard (depth 3)
- **Optimization:** Move ordering, heuristic evaluation, smart move selection
- **Performance:** < 2s response time on average hardware

### 🌐 Networking
- **Protocol:** Custom socket-based protocol
- **Architecture:** Multi-threaded server with ThreadPoolExecutor
- **Scalability:** Supports 50+ concurrent clients
- **Features:** Room management, user authentication, real-time updates

### 🎨 User Experience
- **GUI Framework:** Tkinter with custom components
- **Responsive:** Queue-based event handling for smooth UI
- **Intuitive:** Simple navigation, clear game state indicators
- **Customizable:** Easy to extend and modify

---

## � Contributing

We welcome contributions! Here's how you can help:

1. **Report Bugs:** Open an issue with detailed description
2. **Suggest Features:** Share your ideas in issues
3. **Submit Pull Requests:** Fork, create branch, commit, push, PR
4. **Improve Documentation:** Fix typos, add examples
5. **Share:** Star ⭐ the project and share with friends!

### Development Setup

```bash
git clone https://github.com/Huyho-12/caro-python.git
cd caro-python
pip install -r requirements.txt
python create_database.py
```

### Code Style
- Follow PEP 8 guidelines
- Add docstrings to functions
- Comment complex logic
- Test before committing

---

## 📊 Project Status

| Feature | Status | Version |
|---------|--------|---------|
| Core Game Engine | ✅ Complete | 2.0.0 |
| AI Player | ✅ Complete | 2.0.0 |
| Multiplayer (LAN) | ✅ Complete | 2.0.0 |
| User Authentication | ✅ Complete | 2.0.0 |
| Room Management | ✅ Complete | 2.0.0 |
| Friend System | 🚧 In Progress | TBD |
| Tournament Mode | 📋 Planned | TBD |
| Sound Effects | 📋 Planned | TBD |
| Online Multiplayer | 📋 Planned | TBD |

---

## 🙏 Acknowledgments

- **Python Community** - For amazing libraries and support
- **MySQL** - Reliable database system
- **Tkinter** - Simple yet powerful GUI framework
- **Minimax Algorithm** - Foundation of AI intelligence

---

## 📄 License

```
MIT License

Copyright (c) 2025 Caro Game Python

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
```

---

<div align="center">

**Made with ❤️ and ☕**

⭐ Star this project if you find it useful!

[⬆ Back to top](#-caro-game---python-edition)

</div>
