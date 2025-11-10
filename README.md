# Space War Multiplayer Game in Java
Java multiplayer game using java.swing , java.net in local area network (LAN)
server and clients

made it after learning Object-oriented programming (OOP) in college

<<<<<<< HEAD
## Installation
=======
[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![MySQL](https://img.shields.io/badge/MySQL-8.0%2B-orange.svg)](https://www.mysql.com/)
[![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey.svg)](https://github.com)

**Trò chơi Caro multiplayer với AI thông minh, kiến trúc client-server hiện đại**

[Tính năng](#-tính-năng) •
[Demo](#-demo) •
[Cài đặt](#-cài-đặt) •
[Sử dụng](#-sử-dụng) •
[Tài liệu](#-tài-liệu)

</div>

---

## ✨ Tính năng

### 🖥️ Server
- ✅ Xử lý đa luồng với nhiều client đồng thời
- ✅ Quản lý phòng chơi (tạo, vào, rời phòng)
- ✅ Hệ thống đăng nhập/đăng ký với xác thực
- ✅ Quản lý trạng thái người chơi (online, offline, playing)
- ✅ Bảng xếp hạng theo thống kê thắng/thua
- ✅ Lưu trữ dữ liệu với MySQL
- ✅ Protocol messaging system

### 💻 Client
- ✅ Giao diện đồ họa đẹp mắt với Tkinter
- ✅ Đăng nhập/Đăng ký tài khoản
- ✅ Tạo phòng (có/không mật khẩu)
- ✅ Tham gia phòng từ danh sách
- ✅ Chơi game Caro 15x15 (5 in a row to win)
- ✅ Timer 60 giây cho mỗi lượt
- ✅ Hiển thị điểm số và lượt chơi
- ✅ Chat server (hiển thị thông báo)
- ✅ Xem bảng xếp hạng
- ✅ **Chơi với AI thông minh** (3 độ khó: Dễ, Trung bình, Khó)
- ✅ AI sử dụng thuật toán **Minimax với Alpha-Beta Pruning**



---

## 📸 Demo

### Giao diện chính

```
┌─────────────────────────────────────────────────────────────┐
│  🎮 CARO GAME - Chào mừng đến với game Caro online!         │
│                                                              │
│  📋 Đăng nhập           📋 Đăng ký           🏠 Trang chủ    │
│  ┌─────────────────┐   ┌──────────────┐    ┌─────────────┐ │
│  │ Username: ***   │   │ Tạo tài khoản│    │ Danh sách   │ │
│  │ Password: ***   │   │ mới ngay!    │    │ phòng chơi  │ │
│  └─────────────────┘   └──────────────┘    └─────────────┘ │
│                                                              │
│  🎮 Game Board (15x15)   🤖 AI Mode       👥 Multiplayer   │
│  ┌───────────────────┐  ┌──────────────┐  ┌──────────────┐ │
│  │ X O X O X O X O X │  │ Độ khó: ★★☆  │  │ Room #1      │ │
│  │ O X O X O X O X O │  │ AI thinking..│  │ 2/2 players  │ │
│  │ X O X O X O X O X │  └──────────────┘  └──────────────┘ │
│  └───────────────────┘                                      │
└─────────────────────────────────────────────────────────────┘
```

### Chế độ chơi

| Mode | Description | Status |
|------|-------------|--------|
| 🤖 **Single Player** | Chơi với AI (3 độ khó) | ✅ Hoàn thành |
| 👥 **Local Multiplayer** | Chơi 2 người trên 1 máy | ✅ Hoàn thành |
| 🌐 **Online Multiplayer** | Chơi qua mạng LAN/WiFi | ✅ Hoàn thành |
| 🏆 **Tournament** | Chế độ giải đấu | 🚧 Đang phát triển |

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
┌─────────────────────────────────────────────────────────┐
│                   CARO GAME SYSTEM                       │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  ┌──────────────┐         ┌──────────────┐             │
│  │   CLIENT 1   │◄───────►│              │             │
│  └──────────────┘         │              │             │
│                           │    SERVER    │◄────► MySQL │
│  ┌──────────────┐         │              │             │
│  │   CLIENT 2   │◄───────►│  Port 7777   │             │
│  └──────────────┘         └──────────────┘             │
│                                                          │
│  [Tkinter GUI] ◄──► [Socket] ◄──► [Thread Pool]        │
│        ▲                               ▲                │
│        │                               │                │
│    [AI Engine]                    [Room Manager]        │
│   (Minimax)                      [User Manager]         │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

---

## 📋 Yêu cầu hệ thống

### Phần cứng
- **RAM:** 512 MB (tối thiểu), 2 GB (khuyên dùng)
- **Ổ cứng:** 50 MB khả dụng
- **CPU:** Dual-core 1.0 GHz trở lên
- **Mạng:** LAN/WiFi (cho multiplayer online)

### Phần mềm
- **OS:** Windows 10/11, Linux, macOS
- **Python:** 3.8 hoặc cao hơn
- **MySQL:** 8.0+ (XAMPP khuyên dùng cho Windows)
- **Dependencies:** Xem `requirements.txt`

---

## 🚀 Cài đặt

### Bước 1: Clone repository
>>>>>>> ddb0ed659368c926e68503d24527be5075bd35ed

```bash
git clone https://github.com/Nanarow/SpaceWarMultiplayerGameInJava.git
```

## Usage
run **Server** at file  [ServerWindow.java](https://github.com/Nanarow/SpaceWarMultiplayerGameInJava/blob/main/src/Server/ServerWindow.java) 
run **Client** at file [MainClient.java](https://github.com/Nanarow/SpaceWarMultiplayerGameInJava/blob/main/src/Client/MainClient.java)
**Main Menu**
![enter image description here](https://github.com/Nanarow/SpaceWarMultiplayerGameInJava/blob/main/mainmenuScreenshot.png?raw=true)

if you don't know **IP** and **PORT** you can select at **LAN** and click join button to find a server automatically
you can TCP port forwarding by [**ngrok**](https://ngrok.com/)
```bash
ngrok tcp 4004
```
>4004 is a default server port
>
**In Game**

![enter image description here](https://github.com/Nanarow/SpaceWarMultiplayerGameInJava/blob/main/ingameScreenshot.png?raw=true)
move keys: **W, A, S, D**
skill keys: **RightClick , spacebar ,Q , X**

## Credit
coding by [**Nanarow**](https://github.com/Nanarow)
assets by [**Kristbooker**](https://github.com/Kristbooker)
