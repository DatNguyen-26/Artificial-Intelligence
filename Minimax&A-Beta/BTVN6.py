import tkinter as tk
from tkinter import messagebox
import math

# --- CẤU HÌNH MÀU SẮC (MODERN NEON THEME) ---
BG_COLOR = "#1e1e2e"          # Màu nền ứng dụng (Dark)
BOARD_COLOR = "#313244"       # Màu nền bàn cờ
BTN_COLOR = "#45475a"         # Màu nút cờ khi chưa đánh
HOVER_COLOR = "#585b70"       # Màu khi di chuột qua
X_COLOR = "#89b4fa"           # X: Blue Neon
O_COLOR = "#f5c2e7"           # O: Pink Neon
STATUS_COLOR = "#cdd6f4"      # Màu chữ thông báo

X = "X"
O = "O"
EMPTY = ""

class TicTacToePro:
    def __init__(self, root):
        self.root = root
        self.root.title("Tic-Tac-Toe AI - Modern Edition")
        self.root.geometry("400x600")
        self.root.configure(bg=BG_COLOR)
        
        self.board = [[EMPTY for _ in range(3)] for _ in range(3)]
        self.game_over = False
        self.buttons = [[None for _ in range(3)] for _ in range(3)]
        
        self.create_ui()

    def create_ui(self):
        # 1. Header & Title
        header = tk.Frame(self.root, bg=BG_COLOR, pady=20)
        header.pack()
        
        tk.Label(header, text="TIC TAC TOE", font=('Helvetica', 28, 'bold'), 
                 bg=BG_COLOR, fg=X_COLOR).pack()
        tk.Label(header, text="VS ARTIFICIAL INTELLIGENCE", font=('Helvetica', 10), 
                 bg=BG_COLOR, fg=STATUS_COLOR).pack()

        # 2. Status Label
        self.status_label = tk.Label(self.root, text="Lượt của bạn (X)", font=('Helvetica', 14), 
                                     bg=BG_COLOR, fg=STATUS_COLOR, pady=10)
        self.status_label.pack()

        # 3. Game Board Container
        board_container = tk.Frame(self.root, bg=BOARD_COLOR, padx=10, pady=10, 
                                   highlightbackground=X_COLOR, highlightthickness=1)
        board_container.pack(pady=10)

        for r in range(3):
            for c in range(3):
                btn = tk.Button(board_container, text=EMPTY, font=('Helvetica', 32, 'bold'),
                                width=4, height=1, bg=BTN_COLOR, fg=STATUS_COLOR,
                                activebackground=HOVER_COLOR, activeforeground=STATUS_COLOR,
                                bd=0, relief="flat",
                                command=lambda row=r, col=c: self.user_move(row, col))
                btn.grid(row=r, column=c, padx=5, pady=5)
                
                # Hiệu ứng Hover
                btn.bind("<Enter>", lambda e, b=btn: self.on_enter(b))
                btn.bind("<Leave>", lambda e, b=btn: self.on_leave(b))
                
                self.buttons[r][c] = btn

        # 4. Footer & Control
        footer = tk.Frame(self.root, bg=BG_COLOR, pady=20)
        footer.pack()
        
        reset_btn = tk.Button(footer, text="CHƠI LẠI", font=('Helvetica', 12, 'bold'), 
                              bg=X_COLOR, fg=BG_COLOR, padx=20, pady=10, 
                              bd=0, cursor="hand2", command=self.reset_game)
        reset_btn.pack()

    def on_enter(self, btn):
        if btn['state'] == 'normal':
            btn.config(bg=HOVER_COLOR)

    def on_leave(self, btn):
        if btn['state'] == 'normal':
            btn.config(bg=BTN_COLOR)

    # --- AI LOGIC (ALPHA-BETA) ---

    def user_move(self, r, c):
        if self.game_over or self.board[r][c] != EMPTY:
            return
        self.make_move(r, c, X)
        if not self.game_over:
            self.root.after(500, self.ai_move) # AI chờ 0.5s để tạo cảm giác tự nhiên

    def ai_move(self):
        move = self.alpha_beta_search(self.board)
        if move:
            self.make_move(move[0], move[1], O)

    def make_move(self, r, c, player):
        self.board[r][c] = player
        color = X_COLOR if player == X else O_COLOR
        self.buttons[r][c].config(text=player, state='disabled', disabledforeground=color)
        
        res = self.check_winner(self.board)
        if res:
            self.end_game(f"QUÂN {res} CHIẾN THẮNG!")
        elif all(cell != EMPTY for row in self.board for cell in row):
            self.end_game("TRẬN ĐẤU HÒA!")

    def check_winner(self, board):
        for i in range(3):
            if board[i][0] == board[i][1] == board[i][2] != EMPTY: return board[i][0]
            if board[0][i] == board[1][i] == board[2][i] != EMPTY: return board[0][i]
        if board[0][0] == board[1][1] == board[2][2] != EMPTY: return board[0][0]
        if board[0][2] == board[1][1] == board[2][0] != EMPTY: return board[0][2]
        return None

    def alpha_beta_search(self, board):
        best_val = -math.inf
        best_move = None
        alpha, beta = -math.inf, math.inf
        for r in range(3):
            for c in range(3):
                if board[r][c] == EMPTY:
                    board[r][c] = O
                    val = self.min_value(board, alpha, beta)
                    board[r][c] = EMPTY
                    if val > best_val:
                        best_val, best_move = val, (r, c)
                    alpha = max(alpha, best_val)
        return best_move

    def max_value(self, board, alpha, beta):
        res = self.check_winner(board)
        if res == O: return 10
        if res == X: return -10
        if all(c != EMPTY for r in board for c in r): return 0
        v = -math.inf
        for r in range(3):
            for c in range(3):
                if board[r][c] == EMPTY:
                    board[r][c] = O
                    v = max(v, self.min_value(board, alpha, beta))
                    board[r][c] = EMPTY
                    alpha = max(alpha, v)
                    if beta <= alpha: return v
        return v

    def min_value(self, board, alpha, beta):
        res = self.check_winner(board)
        if res == O: return 10
        if res == X: return -10
        if all(c != EMPTY for r in board for c in r): return 0
        v = math.inf
        for r in range(3):
            for c in range(3):
                if board[r][c] == EMPTY:
                    board[r][c] = X
                    v = min(v, self.max_value(board, alpha, beta))
                    board[r][c] = EMPTY
                    beta = min(beta, v)
                    if beta <= alpha: return v
        return v

    def end_game(self, message):
        self.game_over = True
        self.status_label.config(text=message, fg=O_COLOR)
        messagebox.showinfo("Game Over", message)

    def reset_game(self):
        self.board = [[EMPTY for _ in range(3)] for _ in range(3)]
        self.game_over = False
        self.status_label.config(text="Lượt của bạn (X)", fg=STATUS_COLOR)
        for r in range(3):
            for c in range(3):
                self.buttons[r][c].config(text=EMPTY, state='normal', bg=BTN_COLOR)

if __name__ == "__main__":
    root = tk.Tk()
    app = TicTacToePro(root)
    root.mainloop()