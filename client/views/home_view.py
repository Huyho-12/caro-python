"""
Home view for Caro Game Client
"""

import tkinter as tk
from tkinter import messagebox, scrolledtext, ttk
import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class HomeView:
    """Home page window"""
    
    def __init__(self, client, user):
        self.client = client
        self.user = user
        self.window = tk.Tk()
        self.window.title(f"Trang chủ - {user.nickname}")
        self.window.geometry("800x600")
        self.window.resizable(False, False)
        
        # Center window
        self.center_window()
        
        # Create main frames
        self.create_top_frame()
        self.create_middle_frame()
        self.create_bottom_frame()
        
        # Hanh dong khi dong cua so window
        self.window.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    def center_window(self):
        """Center window on screen"""
        self.window.update_idletasks()
        width = self.window.winfo_width()
        height = self.window.winfo_height()
        x = (self.window.winfo_screenwidth() // 2) - (width // 2)
        y = (self.window.winfo_screenheight() // 2) - (height // 2)
        self.window.geometry(f'{width}x{height}+{x}+{y}')
    
    def create_top_frame(self):
        """Create top frame with user info"""
        top_frame = tk.Frame(self.window, bg="#2196F3", height=80)
        top_frame.pack(fill=tk.X)
        
        # User info
        info_text = f"Chào mừng: {self.user.nickname} | Trận: {self.user.num_games} | Thắng: {self.user.num_wins} | Hòa: {self.user.num_draws} | Xếp hạng: #{self.user.rank}"
        tk.Label(top_frame, text=info_text, font=("Arial", 12, "bold"),
                bg="#2196F3", fg="white").pack(pady=25)
    
    def create_middle_frame(self):
        """Create middle frame with room list and actions"""
        middle_frame = tk.Frame(self.window)
        middle_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Left side - Room list
        left_frame = tk.Frame(middle_frame)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        tk.Label(left_frame, text="DANH SÁCH PHÒNG", font=("Arial", 14, "bold")).pack(pady=10)
        
        # Room list table
        columns = ("ID", "Chủ phòng", "Người chơi", "Mật khẩu")
        self.room_tree = ttk.Treeview(left_frame, columns=columns, show="headings", height=15)
        
        for col in columns:
            self.room_tree.heading(col, text=col)
            self.room_tree.column(col, width=100)
        
        self.room_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Scrollbar for room list
        scrollbar = ttk.Scrollbar(left_frame, orient=tk.VERTICAL, command=self.room_tree.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.room_tree.configure(yscrollcommand=scrollbar.set)
        
        # Refresh button
        tk.Button(left_frame, text="🔄 Làm mới", command=self.refresh_rooms).pack(pady=5)
        
        # Right side - Actions
        right_frame = tk.Frame(middle_frame, width=200)
        right_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=(20, 0))
        
        tk.Label(right_frame, text="HÀNH ĐỘNG", font=("Arial", 14, "bold")).pack(pady=10)
        
        # Buttons
        tk.Button(right_frame, text="🎮 Tạo phòng", font=("Arial", 12),
                 bg="#4CAF50", fg="white", width=15,
                 command=self.create_room).pack(pady=5)
        
        tk.Button(right_frame, text="📥 Vào phòng", font=("Arial", 12),
                 bg="#2196F3", fg="white", width=15,
                 command=self.join_room).pack(pady=5)
        
        tk.Button(right_frame, text="👥 Bạn bè", font=("Arial", 12),
                 bg="#FF9800", fg="white", width=15,
                 command=self.view_friends).pack(pady=5)
        
        tk.Button(right_frame, text="🏆 Bảng xếp hạng", font=("Arial", 12),
                 bg="#9C27B0", fg="white", width=15,
                 command=self.view_rank).pack(pady=5)
        
        tk.Button(right_frame, text="🤖 Chơi với AI", font=("Arial", 12),
                 bg="#607D8B", fg="white", width=15,
                 command=self.play_with_ai).pack(pady=5)
        
        tk.Button(right_frame, text="🚪 Đăng xuất", font=("Arial", 12),
                 bg="#f44336", fg="white", width=15,
                 command=self.logout).pack(pady=20)
    
    def create_bottom_frame(self):
        """Create bottom frame with chat"""
        bottom_frame = tk.Frame(self.window, height=150)
        bottom_frame.pack(fill=tk.X, padx=20, pady=(0, 20))
        
        tk.Label(bottom_frame, text="CHAT SERVER", font=("Arial", 12, "bold")).pack()
        
        # Chat display
        self.chat_display = scrolledtext.ScrolledText(bottom_frame, height=5,
                                                       font=("Arial", 10),
                                                       state=tk.DISABLED)
        self.chat_display.pack(fill=tk.BOTH, expand=True)
    
    def add_chat_message(self, message):
        """Add message to chat display"""
        self.chat_display.config(state=tk.NORMAL)
        self.chat_display.insert(tk.END, message + "\n")
        self.chat_display.see(tk.END)
        self.chat_display.config(state=tk.DISABLED)
    
    def refresh_rooms(self):
        """Request room list from server"""
        self.client.socket_handle.write("get-list-room,")
    
    def update_room_list(self, rooms):
        """Update room list display"""
        # Clear current list
        for item in self.room_tree.get_children():
            self.room_tree.delete(item)
        
        # Add rooms
        for room in rooms:
            password_status = "Có" if room.get('has_password') else "Không"
            self.room_tree.insert("", tk.END, values=(
                room['id'],
                room['host'],
                f"{room['players']}/2",
                password_status
            ))
    
    def create_room(self):
        """Create new room"""
        # Ask for password
        password = tk.simpledialog.askstring("Tạo phòng", "Nhập mật khẩu (để trống nếu không cần):",
                                            parent=self.window)
        if password is not None:  # User didn't cancel
            print(f"Creating room with password: '{password}'")
            self.client.socket_handle.write(f"create-room,{password}")
            messagebox.showinfo("Thành công", "Đã tạo phòng! Đợi người chơi khác vào...")
    
    def join_room(self):
        """Join selected room"""
        selection = self.room_tree.selection()
        if not selection:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn phòng để tham gia")
            return
        
        item = self.room_tree.item(selection[0])
        room_id = item['values'][0]
        has_password = item['values'][3] == "Có"
        
        password = ""
        if has_password:
            password = tk.simpledialog.askstring("Nhập mật khẩu", "Nhập mật khẩu phòng:",
                                                parent=self.window)
            if password is None:  # User canceled
                return
        
        self.client.socket_handle.write(f"join-room,{room_id},{password}")
    
    def view_friends(self):
        """View friend list"""
        self.client.socket_handle.write("view-friend-list,")
        messagebox.showinfo("Thông báo", "Chức năng đang phát triển")
    
    def view_rank(self):
        """View ranking"""
        self.client.socket_handle.write("get-rank-charts,")
        # Will be handled in client when response arrives
    
    def play_with_ai(self):
        """Play with AI - Show difficulty selection dialog"""
        # Create difficulty selection dialog
        difficulty_window = tk.Toplevel(self.window)
        difficulty_window.title("Chọn độ khó AI")
        difficulty_window.geometry("400x380")
        difficulty_window.resizable(False, False)
        difficulty_window.transient(self.window)
        difficulty_window.grab_set()
        
        # Center the dialog
        self.center_dialog(difficulty_window, 400, 380)
        
        # Title
        title_frame = tk.Frame(difficulty_window, bg="#2196F3")
        title_frame.pack(fill=tk.X)
        tk.Label(title_frame, text="🎮 CHỌN ĐỘ KHÓ AI", font=("Arial", 16, "bold"),
                bg="#2196F3", fg="white").pack(pady=15)
        
        # Description
        desc_frame = tk.Frame(difficulty_window, bg="#f5f5f5")
        desc_frame.pack(fill=tk.X, padx=20, pady=15)
        tk.Label(desc_frame, text="Chọn mức độ thử thách phù hợp với bạn:",
                font=("Arial", 11), bg="#f5f5f5").pack(pady=5)
        
        # Buttons frame
        buttons_frame = tk.Frame(difficulty_window)
        buttons_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        def start_game(level):
            difficulty_window.destroy()
            self.window.withdraw()
            self.client.open_ai_game_view(level)
        
        # Easy button
        easy_frame = tk.Frame(buttons_frame, bg="#4CAF50", relief=tk.RAISED, bd=3)
        easy_frame.pack(fill=tk.X, pady=8)
        tk.Button(easy_frame, text="😊 DỄ", font=("Arial", 14, "bold"),
                 bg="#4CAF50", fg="white", width=30, height=1, bd=0,
                 command=lambda: start_game("easy")).pack()
        tk.Label(easy_frame, text="AI đánh ngẫu nhiên - Phù hợp người mới",
                font=("Arial", 9), bg="#4CAF50", fg="white").pack(pady=(0, 5))
        
        # Medium button
        medium_frame = tk.Frame(buttons_frame, bg="#FF9800", relief=tk.RAISED, bd=3)
        medium_frame.pack(fill=tk.X, pady=8)
        tk.Button(medium_frame, text="😐 TRUNG BÌNH", font=("Arial", 14, "bold"),
                 bg="#FF9800", fg="white", width=30, height=1, bd=0,
                 command=lambda: start_game("medium")).pack()
        tk.Label(medium_frame, text="AI thông minh (độ sâu 2) - Khuyên dùng",
                font=("Arial", 9), bg="#FF9800", fg="white").pack(pady=(0, 5))
        
        # Hard button
        hard_frame = tk.Frame(buttons_frame, bg="#f44336", relief=tk.RAISED, bd=3)
        hard_frame.pack(fill=tk.X, pady=8)
        tk.Button(hard_frame, text="😤 KHÓ", font=("Arial", 14, "bold"),
                 bg="#f44336", fg="white", width=30, height=1, bd=0,
                 command=lambda: start_game("hard")).pack()
        tk.Label(hard_frame, text="AI cao cấp (độ sâu 3) - Thử thách lớn!",
                font=("Arial", 9), bg="#f44336", fg="white").pack(pady=(0, 5))
        
        # Cancel button
        tk.Button(buttons_frame, text="✖ Hủy", font=("Arial", 11),
                 bg="#9E9E9E", fg="white", width=15,
                 command=difficulty_window.destroy).pack(pady=10)
    
    def center_dialog(self, dialog, width, height):
        """Center dialog relative to parent window"""
        x = self.window.winfo_x() + (self.window.winfo_width() // 2) - (width // 2)
        y = self.window.winfo_y() + (self.window.winfo_height() // 2) - (height // 2)
        dialog.geometry(f"{width}x{height}+{x}+{y}")
    
    def logout(self):
        """Logout"""
        if messagebox.askyesno("Xác nhận", "Bạn có chắc muốn đăng xuất?"):
            self.client.socket_handle.write("offline,")
            self.window.destroy()
            self.client.open_login_view()
    
    def on_closing(self):
        """Handle window close"""
        if messagebox.askyesno("Xác nhận", "Bạn có chắc muốn thoát?"):
            self.client.socket_handle.write("offline,")
            self.window.destroy()
            self.client.quit()
    
    def show(self):
        """Show window"""
        # Request initial room list
        self.refresh_rooms()
        # Only start mainloop if not already running
        # This prevents multiple mainloop calls
    
    def close(self):
        """Close window"""
        self.window.destroy()


# Import after class definition to avoid circular import
import tkinter.simpledialog
