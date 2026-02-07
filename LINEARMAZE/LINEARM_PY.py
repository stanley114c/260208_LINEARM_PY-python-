import tkinter as tk
from collections import deque
import os
# test
# ==========================================
# 1. 檔案路徑與基本設定
# ==========================================
FILE_PATH = r"C:\Users\s1104\Desktop\LINEARMAZE-20260206T053527Z-001\LINEARMAZE\animation"
N = 25 
CELL = 25 
PAD = 10
FLOOD_DELAY = 20  # 洪水擴散速度 (越小越快)
PATH_DELAY = 60   # 紅線路徑速度

# 起點與終點設定 (根據您的矩陣)
START = (24, 13)  # 底部的 2
END_TARGETS = [(7, 19), (7, 20), (8, 19), (8, 20)] # 上方的 2x2 紅色區域

def load_maze(filename):
    """讀取 C 語言輸出的迷宮，若失敗則使用程式碼內嵌地圖"""
    try:
        with open(filename, "r", encoding="utf-8") as f:
            n = int(f.readline().strip())
            grid = [f.readline().split() for _ in range(n)]
            return n, grid
    except:
        # 如果找不到檔案，這裡放您提供的 25x25 矩陣作為備援
        raw = [
            [1,1,1,1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
            [1,1,1,1,0,1,1,1,1,0,0,0,0,1,1,1,1,1,0,0,0,0,0,0,1],
            [1,0,0,0,0,0,0,1,1,0,1,1,1,1,0,1,1,1,0,1,1,1,1,1,1],
            [1,1,1,1,1,1,0,1,1,0,1,1,1,1,0,0,0,0,0,0,0,0,0,1,1],
            [1,1,1,1,1,1,0,1,1,0,1,1,1,1,0,1,1,0,1,1,1,1,0,1,1],
            [1,1,0,0,0,0,0,1,1,0,1,1,1,1,0,1,1,0,0,0,0,1,0,1,1],
            [1,1,1,1,1,1,0,1,1,0,0,0,0,0,0,1,1,1,1,1,1,1,0,1,1],
            [1,1,1,1,1,1,0,1,1,1,1,0,1,1,0,1,1,1,1,2,2,0,0,1,1],
            [1,1,0,0,0,0,0,1,1,1,1,0,1,1,0,0,0,1,1,2,2,1,1,1,1],
            [1,1,1,0,1,1,0,1,1,1,1,0,1,1,1,1,0,1,1,1,1,1,1,1,1],
            [1,1,1,0,1,1,0,0,0,0,0,0,1,1,1,1,0,1,1,1,1,1,1,1,1],
            [1,0,0,0,1,1,1,1,1,1,1,0,1,1,0,0,0,0,0,0,0,0,0,0,1],
            [1,0,1,0,0,0,1,1,1,1,1,0,1,1,1,1,0,1,1,0,1,1,1,1,1],
            [1,0,1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1],
            [1,0,1,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,1,1,0,1,1],
            [1,0,1,0,1,1,1,1,1,1,0,1,1,1,1,1,0,1,1,0,1,1,0,1,1],
            [1,0,1,1,1,1,1,1,1,1,0,1,1,1,1,1,0,1,1,0,0,0,0,0,1],
            [1,0,0,0,0,0,0,0,0,0,0,1,1,0,1,1,0,1,1,0,1,1,1,1,1],
            [1,1,0,1,1,0,1,1,1,1,0,1,1,0,0,0,0,1,1,0,0,0,0,0,0],
            [1,1,0,1,1,0,1,1,1,1,0,0,0,0,1,1,0,1,1,0,1,1,0,1,1],
            [1,1,0,1,1,1,1,1,1,1,1,1,1,0,1,1,0,1,1,0,1,1,0,1,1],
            [1,1,0,1,1,1,0,0,0,0,0,0,0,0,1,1,0,1,1,0,1,1,0,1,1],
            [1,1,0,1,1,1,1,1,1,0,1,1,1,0,1,1,0,1,1,0,1,1,1,1,1],
            [1,1,1,1,0,0,0,0,0,0,1,1,1,0,1,1,0,0,0,0,0,0,1,1,1],
            [1,1,1,1,1,1,1,1,1,0,1,1,1,2,1,1,1,1,1,1,1,1,1,1,1]
        ]
        return 25, [[str(x) for x in r] for r in raw]

class DoubleAnim:
    def __init__(self, root, n, grid):
        self.root, self.n, self.grid = root, n, grid
        self.dist = [[-1]*n for _ in range(n)]
        self.path_cells = []
        
        # UI 設定
        canvas_size = PAD * 2 + n * CELL
        self.canvas = tk.Canvas(root, width=canvas_size, height=canvas_size, bg="white")
        self.canvas.pack()
        self.info = tk.Label(root, text="演示開始：洪水演算法擴散中...", font=("Arial", 10))
        self.info.pack(pady=5)

        # BFS 初始化 (洪水演算法)
        self.queue = deque([START])
        self.dist[START[0]][START[1]] = 0
        
        self.draw_maze()
        self.tick_flood()

    def draw_maze(self):
        for r in range(self.n):
            for c in range(self.n):
                x1, y1 = PAD + c*CELL, PAD + r*CELL
                x2, y2 = x1 + CELL, y1 + CELL
                color = "black" if self.grid[r][c] == "1" else "white"
                # 終點區域標示
                if (r, c) in END_TARGETS: color = "#ffebee" 
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="#ccc")

    def draw_dot(self, r, c, color):
        offset = CELL * 0.2
        x1, y1 = PAD + c*CELL + offset, PAD + r*CELL + offset
        x2, y2 = x1 + CELL - (offset*2), y1 + CELL - (offset*2)
        self.canvas.create_oval(x1, y1, x2, y2, fill=color, outline="")

    # --- 階段一：洪水演算法展示 ---
    def tick_flood(self):
        if not self.queue:
            self.start_backtrace()
            return

        # 一次處理一個點的擴散
        r, c = self.queue.popleft()
        self.draw_dot(r, c, "#56c7ff") # 藍色水流

        # 檢查是否碰到終點區域
        if (r, c) in END_TARGETS:
            self.final_end = (r, c)
            self.start_backtrace()
            return

        for dr, dc in [(-1,0), (1,0), (0,-1), (0,1)]:
            nr, nc = r+dr, c+dc
            if 0 <= nr < self.n and 0 <= nc < self.n:
                if self.grid[nr][nc] != "1" and self.dist[nr][nc] == -1:
                    self.dist[nr][nc] = self.dist[r][c] + 1
                    self.queue.append((nr, nc))
        
        self.root.after(FLOOD_DELAY, self.tick_flood)

    # --- 階段二：BFS 最短路徑展示 ---
    def start_backtrace(self):
        self.info.config(text="洪水抵達終點！正在回溯 BFS 最短路徑...")
        
        # 尋找路徑點
        cur = self.final_end
        while cur != START:
            self.path_cells.append(cur)
            r, c = cur
            for dr, dc in [(-1,0), (1,0), (0,-1), (0,1)]:
                nr, nc = r+dr, c+dc
                if 0 <= nr < self.n and 0 <= nc < self.n and self.dist[nr][nc] == self.dist[r][c] - 1:
                    cur = (nr, nc)
                    break
        self.path_cells.append(START)
        self.path_cells.reverse() # 起點到終點
        self.path_idx = 0
        self.tick_path()

    def tick_path(self):
        if self.path_idx < len(self.path_cells):
            r, c = self.path_cells[self.path_idx]
            self.draw_dot(r, c, "red") # 紅色路徑
            self.path_idx += 1
            self.root.after(PATH_DELAY, self.tick_path)
        else:
            self.info.config(text=f"演示完成！最短路徑長度：{len(self.path_cells)-1} 步")

if __name__ == "__main__":
    n, grid = load_maze(FILE_PATH)
    root = tk.Tk()
    root.title("雙階段演示：洪水擴散 + BFS 最短路徑")
    DoubleAnim(root, n, grid)
    root.mainloop()