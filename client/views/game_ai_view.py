"""
Minimal, clean `GameAIView` implementation (logic-only) to restore module
importability. This keeps the sparse-board + AI mapping logic and basic
stubs for UI methods. We'll expand the UI later once import/tests pass.
"""

import sys
import os
from typing import Optional, Tuple

try:
    import tkinter as tk
    from tkinter import messagebox
    _HAS_TK = True
except Exception:
    tk = None
    messagebox = None
    _HAS_TK = False

# make sure package imports work
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from shared.constants import INITIAL_BOARD_SIZE, WIN_CONDITION, GAME_TIMEOUT
from ai_player import AIPlayer


class GameAIView:
    """Small, import-safe GameAIView.

    This implementation intentionally avoids heavy Tk usage so we can
    validate logic (board_dict, AI mapping, win check) in a headless
    environment. The full UI will be reintroduced after tests pass.
    """

    def __init__(self, client: Optional[object] = None, difficulty: str = "medium"):
        self.client = client
        self.difficulty = difficulty
        self.board_dict: dict[Tuple[int, int], int] = {}
        self.view_size = INITIAL_BOARD_SIZE
        self.origin_x = 0
        self.origin_y = 0
        self.game_over = False
        self.my_turn = True
        self.my_score = 0
        self.ai_score = 0
        self.ai = AIPlayer(self.difficulty)

        # Timer/AI animation state defaults (set early so create_top_info can reference them)
        self._timer_after_id = None
        self._timer_total = GAME_TIMEOUT
        self._ai_think_after_id = None
        self._ai_think_state = 0

        # If Tk is available, build the full GUI similar to GameView
        if _HAS_TK:
            # Prefer using the existing visible window (e.g. HomeView.window) as the
            # parent for a Toplevel so the new window is properly owned and sized.
            parent = None
            try:
                if self.client and hasattr(self.client, 'current_view') and getattr(self.client, 'current_view'):
                    pv = getattr(self.client, 'current_view')
                    if hasattr(pv, 'window') and pv.window is not None:
                        # Only use as parent if the window still exists
                        try:
                            if callable(getattr(pv.window, 'winfo_exists', None)) and pv.window.winfo_exists():
                                parent = pv.window
                        except Exception:
                            parent = None
            except Exception:
                parent = None

            # Fallback to the Tk default root if present and alive
            if parent is None and getattr(tk, '_default_root', None):
                try:
                    if tk._default_root.winfo_exists():
                        parent = tk._default_root
                except Exception:
                    parent = None

            # Create a child Toplevel when possible, otherwise create a fresh Tk root
            if parent:
                self.window = tk.Toplevel(master=parent)
            else:
                self.window = tk.Tk()

            # Configure window
            try:
                self.window.title(f"Chơi với AI - Độ khó: {self.get_difficulty_name()}")
                self.window.geometry("900x700")
                self.window.resizable(False, False)
            except Exception:
                pass

            # center
            self.center_window()

            # UI: top info, board, bottom controls
            self.create_top_info()
            self.create_game_board()
            self.create_bottom_controls()

            # Pan/zoom configuration
            self._pan_step = max(1, self.view_size // 4)
            self._min_view = 5
            self._max_view = 31

            # Bind arrow keys for panning and +/- for zoom
            try:
                self.window.bind('<Left>', lambda e: self.pan(-self._pan_step, 0))
                self.window.bind('<Right>', lambda e: self.pan(self._pan_step, 0))
                self.window.bind('<Up>', lambda e: self.pan(0, -self._pan_step))
                self.window.bind('<Down>', lambda e: self.pan(0, self._pan_step))
                self.window.bind('<minus>', lambda e: self.zoom_out())
                self.window.bind('<plus>', lambda e: self.zoom_in())
                self.window.bind('<KP_Add>', lambda e: self.zoom_in())
                self.window.bind('<KP_Subtract>', lambda e: self.zoom_out())
            except Exception:
                pass

            # Timer state
            self.timer_seconds = 0

            self.window.protocol("WM_DELETE_WINDOW", self.on_closing)
            # Player starts first
            self.my_turn = True
            self.start_timer()
        else:
            # headless stub
            self.window = None
        

    def make_move(self, x: int, y: int) -> bool:
        """Handle player move in AI mode. Update UI, check win, and ask AI to move."""
        if self.game_over or not self.my_turn or self.board_dict.get((x, y), 0) != 0:
            return False

        # Place player move
        self.board_dict[(x, y)] = 1

        # Update button if visible
        if self.window:
            vi = x - self.origin_x
            vj = y - self.origin_y
            if 0 <= vi < self.view_size and 0 <= vj < self.view_size:
                try:
                    self.buttons[vi][vj].config(text="X", bg="#4CAF50", fg="white", state=tk.DISABLED)
                except Exception:
                    pass
            else:
                self.origin_x = x - (self.view_size // 2)
                self.origin_y = y - (self.view_size // 2)
                self.build_board_buttons()

        # Check win
        if self.check_win(x, y, 1):
            self.on_win()
            return True

        # Switch to AI
        self.my_turn = False
        self.update_turn_display()
        self.stop_timer()

        # Ask AI to move after short delay so UI updates
        if self.window:
            self.window.after(100, self._ai_move_and_update)
        else:
            self._ai_move_and_update()

        return True

    def ai_make_move(self) -> Optional[Tuple[int, int]]:
        # Deprecated - keep for compatibility; use _ai_move_and_update instead
        return self._ai_move_and_update()

    def _ai_move_and_update(self) -> Optional[Tuple[int, int]]:
        """Internal: compute AI move and update UI/state."""
        n = self.view_size
        local = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                local[i][j] = self.board_dict.get((self.origin_x + i, self.origin_y + j), 0)

        move = self.ai.get_move(local)
        if not move:
            # No move found
            self.my_turn = True
            self.update_turn_display()
            self.start_timer()
            return None

        li, lj = move
        gx, gy = self.origin_x + li, self.origin_y + lj

        # fallback if occupied
        if self.board_dict.get((gx, gy), 0) != 0:
            found = False
            for i in range(n):
                for j in range(n):
                    if local[i][j] == 0:
                        gx, gy = self.origin_x + i, self.origin_y + j
                        found = True
                        break
                if found:
                    break

        # Store AI move
        self.board_dict[(gx, gy)] = 2

        # Update UI
        if self.window:
            vi = gx - self.origin_x
            vj = gy - self.origin_y
            if 0 <= vi < self.view_size and 0 <= vj < self.view_size:
                try:
                    self.buttons[vi][vj].config(text="O", bg="#2196F3", fg="white", state=tk.DISABLED)
                except Exception:
                    pass
            else:
                self.origin_x = gx - (self.view_size // 2)
                self.origin_y = gy - (self.view_size // 2)
                self.build_board_buttons()

        # Check AI win
        if self.check_win(gx, gy, 2):
            self.on_lose()
            return gx, gy

        # Back to player
        self.my_turn = True
        self.update_turn_display()
        self.start_timer()
        return gx, gy

    def check_win(self, x: int, y: int, player: int) -> bool:
        dirs = [(0, 1), (1, 0), (1, 1), (1, -1)]
        for dx, dy in dirs:
            cnt = 1
            i, j = x + dx, y + dy
            while self.board_dict.get((i, j), 0) == player:
                cnt += 1
                i += dx; j += dy
            i, j = x - dx, y - dy
            while self.board_dict.get((i, j), 0) == player:
                cnt += 1
                i -= dx; j -= dy
            if cnt >= WIN_CONDITION:
                return True
        return False

    # Lightweight stubs for UI methods so other code can call them
    def new_game(self):
        self.board_dict.clear(); self.origin_x = 0; self.origin_y = 0; self.game_over = False; self.my_turn = True

    def change_difficulty(self, level: str):
        self.difficulty = level; self.ai = AIPlayer(level)

    def get_difficulty_name(self) -> str:
        mapping = {"easy": "Dễ", "medium": "Trung bình", "hard": "Khó"}
        return mapping.get(getattr(self, 'difficulty', 'medium'), "Trung bình")

    def get_state_snapshot(self) -> dict:
        return {"origin": (self.origin_x, self.origin_y), "view": self.view_size, "cells": dict(self.board_dict)}

    def show(self):
        """Lightweight smoke-run helper used by run_ai_smoketest.py.

        This does not open a GUI. It performs a single player move near
        the viewport center, lets the AI respond, then prints a short
        snapshot for verification.
        """
        print("[GameAIView.show] Starting smoke test (headless)")
        cx = self.origin_x + (self.view_size // 2)
        cy = self.origin_y + (self.view_size // 2)
        accepted = self.make_move(cx, cy)
        print(f"[GameAIView.show] Player move at ({cx},{cy}) accepted={accepted}")
        # If AI responded inside make_move, it has already run; otherwise call explicitly
        # (make_move triggers ai_make_move on success), but call again defensively.
        ai_move = None
        if not self.my_turn:
            ai_move = self.ai_make_move()
        # Print snapshot
        snap = self.get_state_snapshot()
        print(f"[GameAIView.show] AI move: {ai_move}")
        print(f"[GameAIView.show] Snapshot origin={snap['origin']} cells={len(snap['cells'])}")

    # ---- GUI helper methods (copied/adapted from GameView) ----
    def center_window(self):
        if not self.window:
            return
        self.window.update_idletasks()
        width = self.window.winfo_width()
        height = self.window.winfo_height()
        x = (self.window.winfo_screenwidth() // 2) - (width // 2)
        y = (self.window.winfo_screenheight() // 2) - (height // 2)
        self.window.geometry(f'{width}x{height}+{x}+{y}')

    def create_top_info(self):
        top_frame = tk.Frame(self.window, bg="#f0f0f0")
        top_frame.pack(fill=tk.X, padx=10, pady=10)

        # Player info (me)
        player_frame = tk.Frame(top_frame, bg="#4CAF50", relief=tk.RAISED, bd=2)
        player_frame.pack(side=tk.LEFT, padx=5)
        tk.Label(player_frame, text=getattr(self.client.user, 'nickname', 'Bạn'), font=("Arial", 14, "bold"),
                 bg="#4CAF50", fg="white").pack(padx=20, pady=5)
        tk.Label(player_frame, text=f"Thắng: {self.my_score}", font=("Arial", 10), bg="#4CAF50", fg="white").pack(padx=20, pady=2)
        self.my_turn_label = tk.Label(player_frame, text="⭐ Lượt của bạn" if self.my_turn else "",
                                      font=("Arial", 10, "bold"), bg="#4CAF50", fg="yellow")
        self.my_turn_label.pack(padx=20, pady=2)

        # Center info
        center_frame = tk.Frame(top_frame, bg="#f0f0f0")
        center_frame.pack(side=tk.LEFT, expand=True, fill=tk.X)
        tk.Label(center_frame, text="CHƠI VỚI AI", font=("Arial", 16, "bold"), bg="#f0f0f0").pack()
        self.score_label = tk.Label(center_frame, text=f"Tỉ số: {self.my_score} - {self.ai_score}", font=("Arial", 14), bg="#f0f0f0")
        self.score_label.pack()
        tk.Label(center_frame, text=f"Độ khó: {self.get_difficulty_name()}", font=("Arial", 12), bg="#f0f0f0", fg="#666").pack()

        # Timer label (center top). Created here so it's always available in GUI mode.
        self.timer_label = tk.Label(center_frame, text=f"Thời gian: {self._timer_total}s", font=("Arial", 12), bg="#f0f0f0", fg="#333")
        self.timer_label.pack()

        # AI info
        ai_frame = tk.Frame(top_frame, bg="#2196F3", relief=tk.RAISED, bd=2)
        ai_frame.pack(side=tk.RIGHT, padx=5)
        tk.Label(ai_frame, text="🤖 AI", font=("Arial", 14, "bold"), bg="#2196F3", fg="white").pack(padx=20, pady=5)
        tk.Label(ai_frame, text=f"Thắng: {self.ai_score}", font=("Arial", 10), bg="#2196F3", fg="white").pack(padx=20, pady=2)
        self.ai_turn_label = tk.Label(ai_frame, text="", font=("Arial", 10, "bold"), bg="#2196F3", fg="yellow")
        self.ai_turn_label.pack(padx=20, pady=2)

    def create_game_board(self):
        container = tk.Frame(self.window)
        container.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        self.canvas = tk.Canvas(container, width=600, height=400, bg="white")
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        v_scrollbar = tk.Scrollbar(container, orient=tk.VERTICAL, command=self.canvas.yview)
        v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        h_scrollbar = tk.Scrollbar(container, orient=tk.HORIZONTAL, command=self.canvas.xview)
        h_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)

        self.canvas.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)

        self.board_frame = tk.Frame(self.canvas, bg="white")
        self.canvas_window = self.canvas.create_window((0, 0), window=self.board_frame, anchor="nw")

        self.build_board_buttons()

        self.board_frame.update_idletasks()
        self.canvas.config(scrollregion=self.canvas.bbox("all"))

        def on_mousewheel(event):
            self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

        def on_shift_mousewheel(event):
            self.canvas.xview_scroll(int(-1 * (event.delta / 120)), "units")

        self.canvas.bind_all("<MouseWheel>", on_mousewheel)
        self.canvas.bind_all("<Shift-MouseWheel>", on_shift_mousewheel)

        self.canvas.bind("<ButtonPress-1>", lambda e: self.canvas.scan_mark(e.x, e.y))
        self.canvas.bind("<B1-Motion>", lambda e: self.canvas.scan_dragto(e.x, e.y, gain=1))

    def build_board_buttons(self):
        try:
            for r in getattr(self, 'buttons', []):
                for b in r:
                    b.destroy()
        except Exception:
            pass

        self.buttons = []
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

        self.board_frame.update_idletasks()
        self.canvas.config(scrollregion=self.canvas.bbox("all"))

    def create_bottom_controls(self):
        bottom_frame = tk.Frame(self.window)
        bottom_frame.pack(fill=tk.X, padx=10, pady=10)

        # Pan controls (arrows) + zoom
        pan_frame = tk.Frame(bottom_frame)
        pan_frame.pack(side=tk.LEFT)
        tk.Button(pan_frame, text="←", width=3, command=lambda: self.pan(-self._pan_step, 0)).pack(side=tk.LEFT, padx=2)
        tk.Button(pan_frame, text="↑", width=3, command=lambda: self.pan(0, -self._pan_step)).pack(side=tk.LEFT, padx=2)
        tk.Button(pan_frame, text="↓", width=3, command=lambda: self.pan(0, self._pan_step)).pack(side=tk.LEFT, padx=2)
        tk.Button(pan_frame, text="→", width=3, command=lambda: self.pan(self._pan_step, 0)).pack(side=tk.LEFT, padx=2)
        tk.Button(pan_frame, text="Zoom -", width=6, command=self.zoom_out).pack(side=tk.LEFT, padx=6)
        tk.Button(pan_frame, text="Zoom +", width=6, command=self.zoom_in).pack(side=tk.LEFT, padx=2)

        # Game control buttons
        tk.Button(bottom_frame, text="🔄 Chơi lại", font=("Arial", 11), bg="#4CAF50", fg="white", width=15,
                 command=self.reset_game).pack(side=tk.LEFT, padx=5)

        tk.Button(bottom_frame, text="⚙️ Đổi độ khó", font=("Arial", 11), bg="#2196F3", fg="white", width=15,
                 command=self.open_change_difficulty).pack(side=tk.LEFT, padx=5)

        tk.Button(bottom_frame, text="⏱️ Cấu hình thời gian", font=("Arial", 11), bg="#607D8B", fg="white", width=18,
                 command=self.open_time_config).pack(side=tk.LEFT, padx=5)

        tk.Button(bottom_frame, text="🏠 Về trang chủ", font=("Arial", 11), bg="#FF9800", fg="white", width=15,
                 command=self.go_home).pack(side=tk.LEFT, padx=5)

        tk.Button(bottom_frame, text="🚪 Thoát", font=("Arial", 11), bg="#f44336", fg="white", width=15,
                 command=self.on_closing).pack(side=tk.RIGHT, padx=5)

    def pan(self, dx: int, dy: int):
        """Shift the viewport by dx,dy (in cells) and rebuild visible board."""
        try:
            self.origin_x += dx
            self.origin_y += dy
            # small safety: keep origin within reasonable bounds (avoid overflow)
            if self.origin_x < -10_000:
                self.origin_x = -10_000
            if self.origin_y < -10_000:
                self.origin_y = -10_000
            if self.origin_x > 10_000:
                self.origin_x = 10_000
            if self.origin_y > 10_000:
                self.origin_y = 10_000
            if self.window:
                self.build_board_buttons()
        except Exception:
            pass

    def zoom_in(self):
        """Decrease view_size to zoom in (show fewer cells larger)."""
        try:
            new = max(self._min_view, self.view_size - 2)
            if new != self.view_size:
                # keep center location
                cx = self.origin_x + (self.view_size // 2)
                cy = self.origin_y + (self.view_size // 2)
                self.view_size = new
                self._pan_step = max(1, self.view_size // 4)
                self.origin_x = cx - (self.view_size // 2)
                self.origin_y = cy - (self.view_size // 2)
                if self.window:
                    self.build_board_buttons()
        except Exception:
            pass

    def zoom_out(self):
        """Increase view_size to zoom out (show more cells)."""
        try:
            new = min(self._max_view, self.view_size + 2)
            if new != self.view_size:
                cx = self.origin_x + (self.view_size // 2)
                cy = self.origin_y + (self.view_size // 2)
                self.view_size = new
                self._pan_step = max(1, self.view_size // 4)
                self.origin_x = cx - (self.view_size // 2)
                self.origin_y = cy - (self.view_size // 2)
                if self.window:
                    self.build_board_buttons()
        except Exception:
            pass

    def start_timer(self):
        # Use per-view configured timeout
        self.timer_seconds = getattr(self, '_timer_total', GAME_TIMEOUT)
        # Cancel any previous timer callback and start fresh
        try:
            if self._timer_after_id and self.window:
                try:
                    self.window.after_cancel(self._timer_after_id)
                except Exception:
                    pass
            self.update_timer()
        except Exception:
            # Best-effort: still call update_timer
            try:
                self.update_timer()
            except Exception:
                pass

    def stop_timer(self):
        # Cancel any pending timer callback so the countdown stops immediately
        try:
            if hasattr(self, '_timer_after_id') and self._timer_after_id and self.window:
                try:
                    self.window.after_cancel(self._timer_after_id)
                except Exception:
                    pass
        except Exception:
            pass
        finally:
            try:
                self._timer_after_id = None
            except Exception:
                pass

    def update_timer(self):
        if not self.window:
            return
        if self.my_turn and not self.game_over:
            try:
                # Create timer label if missing
                if not hasattr(self, 'timer_label'):
                    # fallback: create minimal timer label in case create_top_info wasn't called
                    try:
                        self.timer_label = tk.Label(self.window, text=f"Thời gian: {getattr(self,'_timer_total', GAME_TIMEOUT)}s")
                        self.timer_label.pack()
                    except Exception:
                        pass
                # decrement and display
                self.timer_seconds -= 1
                if hasattr(self, 'timer_label'):
                    self.timer_label.config(text=f"Thời gian: {self.timer_seconds}s")

                # If still time left, schedule next tick and remember the callback id
                if self.timer_seconds > 0:
                    try:
                        # cancel previous if any
                        if getattr(self, '_timer_after_id', None) and self._timer_after_id:
                            try:
                                self.window.after_cancel(self._timer_after_id)
                            except Exception:
                                pass
                        self._timer_after_id = self.window.after(1000, self.update_timer)
                    except Exception:
                        # fallback to non-cancellable call
                        try:
                            self.window.after(1000, self.update_timer)
                        except Exception:
                            pass
                else:
                    # Time out
                    try:
                        messagebox.showwarning("Hết giờ!", "Bạn đã hết thời gian")
                    except Exception:
                        pass
                    self.on_lose()
            except Exception:
                pass

        else:
            # If it's not player's turn, ensure timer label shows paused or AI thinking
            try:
                if hasattr(self, 'timer_label'):
                    self.timer_label.config(text=f"Tạm dừng")
            except Exception:
                pass

    def update_turn_display(self):
        if not self.window:
            return
        if self.my_turn:
            try:
                self.my_turn_label.config(text="⭐ Lượt của bạn")
                self.ai_turn_label.config(text="")
                # Stop AI thinking animation
                try:
                    if getattr(self, '_ai_think_after_id', None):
                        try:
                            self.window.after_cancel(self._ai_think_after_id)
                        except Exception:
                            pass
                        self._ai_think_after_id = None
                except Exception:
                    pass
                # Ensure timer_label is showing remaining time
                try:
                    if hasattr(self, 'timer_label') and getattr(self, 'timer_seconds', None) is not None:
                        self.timer_label.config(text=f"Thời gian: {self.timer_seconds}s")
                except Exception:
                    pass
            except Exception:
                pass
        else:
            try:
                self.my_turn_label.config(text="")
                self.ai_turn_label.config(text="⭐ AI đang suy nghĩ...")
                # Start a simple dot-animating indicator for AI thinking
                try:
                    # cancel previous if any
                    if getattr(self, '_ai_think_after_id', None):
                        try:
                            self.window.after_cancel(self._ai_think_after_id)
                        except Exception:
                            pass
                        self._ai_think_after_id = None
                    # start animation state
                    self._ai_think_state = 0
                    def _think_anim():
                        try:
                            dots = '.' * (self._ai_think_state % 4)
                            self.ai_turn_label.config(text=f"⭐ AI đang suy nghĩ{dots}")
                            self._ai_think_state += 1
                            self._ai_think_after_id = self.window.after(500, _think_anim)
                        except Exception:
                            pass
                    _think_anim()
                except Exception:
                    pass
            except Exception:
                pass

    def on_win(self):
        self.game_over = True
        self.my_score += 1
        self.update_score_display()
        if messagebox.askyesno("Chúc mừng!", "🎉 Bạn đã thắng!\\n\\nBạn có muốn chơi ván mới không?"):
            self.reset_game()
        else:
            self.go_home()

    def on_lose(self):
        self.game_over = True
        self.ai_score += 1
        self.update_score_display()
        if messagebox.askyesno("Tiếc quá!", "😢 AI đã thắng!\\n\\nBạn có muốn chơi ván mới không?"):
            self.reset_game()
        else:
            self.go_home()

    def reset_game(self):
        self.game_over = False
        self.my_turn = True
        self.board_dict.clear()
        self.origin_x = 0
        self.origin_y = 0
        if self.window:
            self.build_board_buttons()
            for i in range(self.view_size):
                for j in range(self.view_size):
                    try:
                        self.buttons[i][j].config(text="", bg="white", state=tk.NORMAL)
                    except Exception:
                        pass
            self.update_turn_display()
            self.start_timer()

    def open_change_difficulty(self):
        if not self.window:
            return
        difficulty_window = tk.Toplevel(self.window)
        difficulty_window.title("Chọn độ khó")
        difficulty_window.geometry("300x200")
        difficulty_window.resizable(False, False)

        def select_difficulty(level):
            self.difficulty = level
            self.ai = AIPlayer(level)
            self.window.title(f"Chơi với AI - Độ khó: {self.get_difficulty_name()}")
            difficulty_window.destroy()
            self.reset_game()

        tk.Label(difficulty_window, text="Chọn độ khó:", font=("Arial", 14, "bold")).pack(pady=20)
        tk.Button(difficulty_window, text="😊 Dễ", font=("Arial", 12), bg="#4CAF50", fg="white",
                 width=20, command=lambda: select_difficulty("easy")).pack(pady=5)
        tk.Button(difficulty_window, text="😐 Trung bình", font=("Arial", 12), bg="#FF9800", fg="white",
                 width=20, command=lambda: select_difficulty("medium")).pack(pady=5)
        tk.Button(difficulty_window, text="😤 Khó", font=("Arial", 12), bg="#f44336", fg="white",
                 width=20, command=lambda: select_difficulty("hard")).pack(pady=5)

    def open_time_config(self):
        """Open a small dialog to configure per-turn timeout (seconds)."""
        if not self.window:
            return
        try:
            cfg = tk.Toplevel(self.window)
            cfg.title("Cấu hình thời gian")
            cfg.geometry("320x140")
            cfg.resizable(False, False)

            tk.Label(cfg, text="Số giây cho mỗi lượt:", font=("Arial", 12)).pack(pady=(12, 6))
            val = tk.IntVar(value=getattr(self, '_timer_total', GAME_TIMEOUT))
            spin = tk.Spinbox(cfg, from_=5, to=600, increment=5, textvariable=val, width=8, font=("Arial", 12))
            spin.pack()

            btn_frame = tk.Frame(cfg)
            btn_frame.pack(fill=tk.X, pady=12, padx=12)

            def _save():
                try:
                    v = int(val.get())
                    if v < 5:
                        v = 5
                    if v > 600:
                        v = 600
                    self._timer_total = v
                    # If player's turn, update remaining seconds immediately
                    if self.my_turn:
                        self.timer_seconds = v
                        try:
                            if hasattr(self, 'timer_label'):
                                self.timer_label.config(text=f"Thời gian: {self.timer_seconds}s")
                        except Exception:
                            pass
                    cfg.destroy()
                except Exception:
                    try:
                        messagebox.showerror("Lỗi", "Giá trị không hợp lệ")
                    except Exception:
                        pass

            tk.Button(btn_frame, text="Lưu", width=10, bg="#4CAF50", fg="white", command=_save).pack(side=tk.LEFT, padx=8)
            tk.Button(btn_frame, text="Hủy", width=10, command=cfg.destroy).pack(side=tk.RIGHT, padx=8)
        except Exception:
            pass

    def update_score_display(self):
        try:
            if hasattr(self, 'score_label'):
                self.score_label.config(text=f"Tỉ số: {self.my_score} - {self.ai_score}")
        except Exception:
            pass

    def go_home(self):
        try:
            if self.window:
                self.window.destroy()
        except Exception:
            pass
        try:
            if self.client:
                self.client.open_home_view()
        except Exception:
            pass

    def on_closing(self):
        if messagebox.askyesno("Xác nhận", "Bạn có chắc muốn thoát?"):
            self.go_home()

