"""
Game view for playing Caro
"""

import tkinter as tk
from tkinter import messagebox
import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from shared.constants import INITIAL_BOARD_SIZE, WIN_CONDITION, GAME_TIMEOUT, BOARD_EXPANSION_SIZE, MAX_BOARD_SIZE


class GameView:
    """Game playing window"""
    
    def __init__(self, client, room_id, competitor, is_host, competitor_ip):
        self.client = client
        self.room_id = room_id
        self.competitor = competitor
        self.is_host = is_host
        self.competitor_ip = competitor_ip
        self.my_turn = is_host  # Host starts first
        
        # Game state (sparse board + viewport)
        # store only played cells: (x,y) -> 1|2
        self.board_dict = {}
        # viewport size (visible cells per side)
        self.view_size = INITIAL_BOARD_SIZE
        # top-left global coordinate of viewport
        self.origin_x = 0
        self.origin_y = 0
        self.buttons = []
        self.game_over = False
        self.timer_seconds = GAME_TIMEOUT
        self.my_score = 0
        self.competitor_score = 0
        
        # Create window
        self.window = tk.Tk()
        self.window.title(f"Phòng {room_id} - Caro Game")
        self.window.geometry("900x700")
        self.window.resizable(False, False)
        
        # Center window
        self.center_window()
        
        # Create UI
        self.create_top_info()
        self.create_game_board()
        self.create_bottom_controls()
        
        # Handle window close
        self.window.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        # Start timer if it's my turn
        if self.my_turn:
            self.start_timer()
    
    def center_window(self):
        """Center window on screen"""
        self.window.update_idletasks()
        width = self.window.winfo_width()
        height = self.window.winfo_height()
        x = (self.window.winfo_screenwidth() // 2) - (width // 2)
        y = (self.window.winfo_screenheight() // 2) - (height // 2)
        self.window.geometry(f'{width}x{height}+{x}+{y}')
    
    def create_top_info(self):
        """Create top info panel"""
        top_frame = tk.Frame(self.window, bg="#f0f0f0")
        top_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Player 1 (me)
        player1_frame = tk.Frame(top_frame, bg="#4CAF50", relief=tk.RAISED, bd=2)
        player1_frame.pack(side=tk.LEFT, padx=5)
        
        tk.Label(player1_frame, text=self.client.user.nickname, font=("Arial", 14, "bold"),
                bg="#4CAF50", fg="white").pack(padx=20, pady=5)
        tk.Label(player1_frame, text=f"Thắng: {self.my_score}", font=("Arial", 10),
                bg="#4CAF50", fg="white").pack(padx=20, pady=2)
        self.my_turn_label = tk.Label(player1_frame, text="⭐ Lượt của bạn" if self.my_turn else "",
                                      font=("Arial", 10, "bold"), bg="#4CAF50", fg="yellow")
        self.my_turn_label.pack(padx=20, pady=2)
        
        # Center info
        center_frame = tk.Frame(top_frame, bg="#f0f0f0")
        center_frame.pack(side=tk.LEFT, expand=True, fill=tk.X)
        
        tk.Label(center_frame, text=f"PHÒNG {self.room_id}", font=("Arial", 16, "bold"),
                bg="#f0f0f0").pack()
        
        self.score_label = tk.Label(center_frame, text=f"Tỉ số: {self.my_score} - {self.competitor_score}",
                                    font=("Arial", 14), bg="#f0f0f0")
        self.score_label.pack()
        
        self.timer_label = tk.Label(center_frame, text=f"Thời gian: {self.timer_seconds}s",
                                    font=("Arial", 12), bg="#f0f0f0", fg="red")
        self.timer_label.pack()
        
        # Player 2 (competitor)
        player2_frame = tk.Frame(top_frame, bg="#2196F3", relief=tk.RAISED, bd=2)
        player2_frame.pack(side=tk.RIGHT, padx=5)
        
        tk.Label(player2_frame, text=self.competitor.nickname, font=("Arial", 14, "bold"),
                bg="#2196F3", fg="white").pack(padx=20, pady=5)
        tk.Label(player2_frame, text=f"Thắng: {self.competitor_score}", font=("Arial", 10),
                bg="#2196F3", fg="white").pack(padx=20, pady=2)
        self.competitor_turn_label = tk.Label(player2_frame, text="" if self.my_turn else "⭐ Lượt đối thủ",
                                             font=("Arial", 10, "bold"), bg="#2196F3", fg="yellow")
        self.competitor_turn_label.pack(padx=20, pady=2)
    
    def create_game_board(self):
        """Create game board with scrollbars"""
        # Container frame with scrollbars
        container = tk.Frame(self.window)
        container.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        
        # Create canvas
        self.canvas = tk.Canvas(container, width=600, height=400, bg="white")
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Add scrollbars
        v_scrollbar = tk.Scrollbar(container, orient=tk.VERTICAL, command=self.canvas.yview)
        v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        h_scrollbar = tk.Scrollbar(container, orient=tk.HORIZONTAL, command=self.canvas.xview)
        h_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)

        self.canvas.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)

        # Create frame inside canvas
        self.board_frame = tk.Frame(self.canvas, bg="white")
        self.canvas_window = self.canvas.create_window((0, 0), window=self.board_frame, anchor="nw")
        
        # Create buttons for board
        self.build_board_buttons()

        # Update scroll region
        self.board_frame.update_idletasks()
        self.canvas.config(scrollregion=self.canvas.bbox("all"))

        # Mouse wheel scrolling (vertical) and horizontal via Shift+Wheel
        def on_mousewheel(event):
            self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

        def on_shift_mousewheel(event):
            # Shift+wheel scrolls horizontally
            self.canvas.xview_scroll(int(-1 * (event.delta / 120)), "units")

        # Bind wheel events to canvas so the user can scroll
        self.canvas.bind_all("<MouseWheel>", on_mousewheel)
        self.canvas.bind_all("<Shift-MouseWheel>", on_shift_mousewheel)

        # Enable panning by click-drag on the canvas
        self.canvas.bind("<ButtonPress-1>", lambda e: self.canvas.scan_mark(e.x, e.y))
        self.canvas.bind("<B1-Motion>", lambda e: self.canvas.scan_dragto(e.x, e.y, gain=1))

    def build_board_buttons(self):
        """(Re)build the button grid for the current board size and state"""
        # Destroy existing widgets if any
        try:
            for r in getattr(self, 'buttons', []):
                for b in r:
                    b.destroy()
        except Exception:
            pass

        self.buttons = []
        # Build buttons for the viewport area [origin_x .. origin_x+view_size-1]
        for vi in range(self.view_size):
            row = []
            gx = self.origin_x + vi
            for vj in range(self.view_size):
                gy = self.origin_y + vj
                val = self.board_dict.get((gx, gy), 0)
                text = ""
                state = tk.NORMAL
                bg = "white"
                if val == 1:
                    text = "X"
                    bg = "#4CAF50"
                    state = tk.DISABLED
                elif val == 2:
                    text = "O"
                    bg = "#2196F3"
                    state = tk.DISABLED

                btn = tk.Button(self.board_frame, text=text, width=2, height=1,
                                font=("Arial", 14, "bold"), bg=bg,
                                relief=tk.RAISED, bd=1,
                                state=state,
                                command=lambda x=gx, y=gy: self.make_move(x, y))
                btn.grid(row=vi, column=vj, padx=0, pady=0)
                row.append(btn)
            self.buttons.append(row)

        # Update scroll region
        self.board_frame.update_idletasks()
        self.canvas.config(scrollregion=self.canvas.bbox("all"))

    def expand_board_if_needed(self, x, y):
        # No-op in sparse model; kept for backward compatibility
        return x, y
    
    def create_bottom_controls(self):
        """Create bottom control panel"""
        bottom_frame = tk.Frame(self.window)
        bottom_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Buttons
        tk.Button(bottom_frame, text="🤝 Xin hòa", font=("Arial", 11),
                 bg="#FF9800", fg="white", width=12,
                 command=self.request_draw).pack(side=tk.LEFT, padx=5)
        
        tk.Button(bottom_frame, text="🔄 Chơi lại", font=("Arial", 11),
                 bg="#9C27B0", fg="white", width=12,
                 command=self.request_revenge).pack(side=tk.LEFT, padx=5)
        
        tk.Button(bottom_frame, text="🚪 Rời phòng", font=("Arial", 11),
                 bg="#f44336", fg="white", width=12,
                 command=self.leave_room).pack(side=tk.LEFT, padx=5)
        
        # Chat
        chat_frame = tk.Frame(bottom_frame)
        chat_frame.pack(side=tk.RIGHT, fill=tk.X, expand=True, padx=(20, 0))
        
        self.chat_entry = tk.Entry(chat_frame, font=("Arial", 11))
        self.chat_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.chat_entry.bind('<Return>', lambda e: self.send_chat())
        
        tk.Button(chat_frame, text="Gửi", font=("Arial", 11),
                 command=self.send_chat).pack(side=tk.RIGHT, padx=(5, 0))
    
    def make_move(self, x, y):
        """Handle player move"""
        if self.game_over:
            messagebox.showinfo("Thông báo", "Ván đấu đã kết thúc")
            return
        
        if not self.my_turn:
            messagebox.showwarning("Cảnh báo", "Chưa đến lượt của bạn")
            return
        
        # Check existing move
        if self.board_dict.get((x, y), 0) != 0:
            messagebox.showwarning("Cảnh báo", "Ô này đã được đánh")
            return

        # Make move (store in dict)
        self.board_dict[(x, y)] = 1  # 1 for player, 2 for competitor

        # If the move is inside current viewport, update button; otherwise center viewport
        vi = x - self.origin_x
        vj = y - self.origin_y
        if 0 <= vi < self.view_size and 0 <= vj < self.view_size:
            try:
                self.buttons[vi][vj].config(text="X", bg="#4CAF50", fg="white", state=tk.DISABLED)
            except Exception:
                pass
        else:
            # center viewport on the move
            self.origin_x = x - (self.view_size // 2)
            self.origin_y = y - (self.view_size // 2)
            self.build_board_buttons()
        
        # Send move to server
        try:
            self.client.socket_handle.write(f"user-move,{x},{y}")
        except Exception:
            pass
        
        # Check win
        if self.check_win(x, y, 1):
            self.on_win()
            return
        
        # Check draw (board full)
        if self.is_board_full():
            self.on_draw()
            return
        
    # Switch turn
        self.my_turn = False
        self.update_turn_display()
        self.stop_timer()
    
    def on_competitor_move(self, x, y):
        """Handle competitor move"""
        # Store competitor move
        self.board_dict[(x, y)] = 2

        # If move is inside viewport, update; otherwise center viewport on it
        vi = x - self.origin_x
        vj = y - self.origin_y
        if 0 <= vi < self.view_size and 0 <= vj < self.view_size:
            try:
                self.buttons[vi][vj].config(text="O", bg="#2196F3", fg="white", state=tk.DISABLED)
            except Exception:
                pass
        else:
            self.origin_x = x - (self.view_size // 2)
            self.origin_y = y - (self.view_size // 2)
            self.build_board_buttons()
        
        # Check if competitor wins
        if self.check_win(x, y, 2):
            self.on_lose()
            return
        
        # Check draw
        if self.is_board_full():
            self.on_draw()
            return
        
        # My turn now
        self.my_turn = True
        self.update_turn_display()
        self.start_timer()
    
    def check_win(self, x, y, player):
        """Check if player wins at position (x, y) using sparse board dict."""
        directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
        for dx, dy in directions:
            count = 1
            # forward
            i, j = x + dx, y + dy
            while self.board_dict.get((i, j), 0) == player:
                count += 1
                i += dx
                j += dy

            # backward
            i, j = x - dx, y - dy
            while self.board_dict.get((i, j), 0) == player:
                count += 1
                i -= dx
                j -= dy

            if count >= WIN_CONDITION:
                return True

        return False
    
    def is_board_full(self):
        """Check if board is full"""
        # With an effectively infinite sparse board, we never consider it "full"
        return False
    
    def on_win(self):
        """Handle win"""
        self.game_over = True
        self.stop_timer()
        self.my_score += 1
        self.update_score_display()
        self.client.socket_handle.write("win,")
        # Hiển thị thông báo và hỏi chơi lại
        result = messagebox.askyesno("Chúc mừng!", 
                                     "🎉 Bạn đã thắng!\n\nBạn có muốn chơi ván mới không?")
        if result:
            self.reset_game()
        else:
            self.leave_room()
    
    def on_lose(self):
        """Handle lose"""
        self.game_over = True
        self.stop_timer()
        self.competitor_score += 1
        self.update_score_display()
        # Hiển thị thông báo và hỏi chơi lại
        result = messagebox.askyesno("Tiếc quá!", 
                                     "😢 Bạn đã thua\n\nBạn có muốn chơi ván mới không?")
        if result:
            self.reset_game()
        else:
            self.leave_room()
    
    def on_draw(self):
        """Handle draw"""
        self.game_over = True
        self.stop_timer()
        # Hiển thị thông báo và hỏi chơi lại
        result = messagebox.askyesno("Hòa!", 
                                     "🤝 Ván đấu hòa!\n\nBạn có muốn chơi ván mới không?")
        if result:
            self.reset_game()
        else:
            self.leave_room()
    
    def reset_game(self):
        """Reset game board for new round"""
        # Reset game state
        self.game_over = False
        self.my_turn = self.is_host  # Host starts first
        # clear sparse board
        self.board_dict.clear()
        # reset viewport origin
        self.origin_x = 0
        self.origin_y = 0
        
        # Rebuild buttons for the (empty) viewport
        self.build_board_buttons()

        # Reset all buttons' visuals
        for i in range(self.view_size):
            for j in range(self.view_size):
                try:
                    self.buttons[i][j].config(text="", bg="white", state=tk.NORMAL)
                except Exception:
                    pass
        
        # Update display
        self.update_turn_display()
        if self.my_turn:
            self.start_timer()
        
        # Notify server about new game
        self.client.socket_handle.write("new-game,")
        messagebox.showinfo("Ván mới", "Bắt đầu ván đấu mới!")
    
    def update_turn_display(self):
        """Update turn indicators"""
        if self.my_turn:
            self.my_turn_label.config(text="⭐ Lượt của bạn")
            self.competitor_turn_label.config(text="")
        else:
            self.my_turn_label.config(text="")
            self.competitor_turn_label.config(text="⭐ Lượt đối thủ")
    
    def update_score_display(self):
        """Update score display"""
        self.score_label.config(text=f"Tỉ số: {self.my_score} - {self.competitor_score}")
    
    def start_timer(self):
        """Start countdown timer"""
        self.timer_seconds = GAME_TIMEOUT
        self.update_timer()
    
    def stop_timer(self):
        """Stop timer"""
        pass  # Timer will stop when turn changes
    
    def update_timer(self):
        """Update timer display"""
        if self.my_turn and not self.game_over:
            self.timer_label.config(text=f"Thời gian: {self.timer_seconds}s")
            
            if self.timer_seconds > 0:
                self.timer_seconds -= 1
                self.window.after(1000, self.update_timer)
            else:
                # Timeout - lose
                messagebox.showwarning("Hết giờ!", "Bạn đã hết thời gian")
                self.client.socket_handle.write("lose,")
                self.on_lose()
    
    def request_draw(self):
        """Request draw"""
        if self.game_over:
            messagebox.showinfo("Thông báo", "Ván đấu đã kết thúc")
            return
        
        self.client.socket_handle.write("draw-request,")
        messagebox.showinfo("Thông báo", "Đã gửi yêu cầu hòa đến đối thủ")
    
    def request_revenge(self):
        """Request revenge (play again)"""
        if not self.game_over:
            messagebox.showinfo("Thông báo", "Ván đấu chưa kết thúc")
            return
        
        self.client.socket_handle.write("ask-for-revenge,")
        messagebox.showinfo("Thông báo", "Đã gửi yêu cầu chơi lại đến đối thủ")
    
    def leave_room(self):
        """Leave room"""
        if messagebox.askyesno("Xác nhận", "Bạn có chắc muốn rời phòng?"):
            self.client.socket_handle.write("leave-room,")
            self.window.destroy()
            self.client.open_home_view()
    
    def send_chat(self):
        """Send chat message"""
        message = self.chat_entry.get().strip()
        if message:
            self.client.socket_handle.write(f"send-message,{message}")
            self.chat_entry.delete(0, tk.END)
    
    def on_receive_message(self, message):
        """Display received chat message"""
        messagebox.showinfo("Tin nhắn", f"{self.competitor.nickname}: {message}")
    
    def on_closing(self):
        """Handle window close"""
        self.leave_room()
    
    def show(self):
        """Show window"""
        # Don't call mainloop - it's already running
    
    def close(self):
        """Close window"""
        self.window.destroy()
