import tkinter as tk
from tkinter import ttk
from ttkthemes import ThemedStyle
import numpy as np
from tkinter import messagebox

class KnightTourSolver:
    def __init__(self, master):
        self.master = master
        self.master.title("Knight's Tour Solver")

        # Set the style
        self.style = ThemedStyle(self.master)
        self.style.set_theme("plastik")  # You can choose different themes: "clam", "alt", "default", etc.

        # Variables for user input
        self.n_var = tk.IntVar()
        self.x_var = tk.IntVar()
        self.y_var = tk.IntVar()

        # Page 1: Input Page
        self.input_frame = tk.Frame(self.master, bg="#D3D3D3")  # Set background color
        self.input_frame.pack(pady=20)

        tk.Label(self.input_frame, text="Enter Board Size (N x N):", bg="#D3D3D3").grid(row=0, column=0, padx=10, pady=10)
        tk.Entry(self.input_frame, textvariable=self.n_var).grid(row=0, column=1, padx=10, pady=10)

        tk.Label(self.input_frame, text="Enter Starting Point (X, Y):", bg="#D3D3D3").grid(row=1, column=0, padx=10, pady=10)
        tk.Label(self.input_frame, text="X:", bg="#D3D3D3").grid(row=1, column=1, padx=5, pady=10)
        tk.Entry(self.input_frame, textvariable=self.x_var).grid(row=1, column=2, padx=5, pady=10)
        tk.Label(self.input_frame, text="Y:", bg="#D3D3D3").grid(row=1, column=3, padx=5, pady=10)
        tk.Entry(self.input_frame, textvariable=self.y_var).grid(row=1, column=4, padx=5, pady=10)

        next_btn = ttk.Button(self.input_frame, text="Next", command=self.show_algorithm_page, style="TButton")
        next_btn.grid(row=2, column=2, pady=20)

    def show_algorithm_page(self):
        # Validate input
        if self.n_var.get() <= 0 or not (1 <= self.x_var.get() <= self.n_var.get()) or not (1 <= self.y_var.get() <= self.n_var.get()):
            messagebox.showerror("Error", "Invalid input. Please check the values.")
            return

        # Page 2: Algorithm Selection Page
        self.input_frame.destroy()

        self.algorithm_frame = tk.Frame(self.master, bg="#D3D3D3")  # Set background color
        self.algorithm_frame.pack(pady=40)  # Increase the padding for a larger page

        tk.Label(self.algorithm_frame, text="Select Algorithm:", bg="#D3D3D3").grid(row=0, column=0, padx=10, pady=10)

        backtracking_btn = ttk.Button(self.algorithm_frame, text="Backtracking", command=self.show_solution_page_backtracking, style="TButton")
        backtracking_btn.grid(row=1, column=0, pady=10)

        genetics_btn = ttk.Button(self.algorithm_frame, text="Genetics", command=self.show_solution_page_genetics, style="TButton")
        genetics_btn.grid(row=1, column=1, pady=10)

    def show_solution_page_backtracking(self):
        solution_board = self.solve_knights_tour_backtracking()
        self.show_solution_board(solution_board)

    def show_solution_page_genetics(self):
        # Placeholder for Genetics algorithm
        solution_board = self.solve_genetics()
        self.show_solution_board(solution_board)

    def solve_knights_tour_backtracking(self):
        n = self.n_var.get()
        start_x = self.x_var.get()
        start_y = self.y_var.get()
        board = np.full((n, n), -1)
        move_count = 0
        x_moves = [2, 1, -1, -2, -2, -1, 1, 2]
        y_moves = [1, 2, 2, 1, -1, -2, -2, -1]

        def is_valid_move(x, y):
            return 0 <= x < n and 0 <= y < n and board[x][y] == -1

        def solve_util(x, y, move_count):
            if move_count == n * n:
                return True

            for i in range(8):
                next_x, next_y = x + x_moves[i], y + y_moves[i]
                if is_valid_move(next_x, next_y):
                    board[next_x][next_y] = move_count
                    if solve_util(next_x, next_y, move_count + 1):
                        return True
                    board[next_x][next_y] = -1

            return False

        # Start from the user-defined position
        board[start_x - 1][start_y - 1] = 0
        if not solve_util(start_x - 1, start_y - 1, 1):
            messagebox.showinfo("Solution", "Solution does not exist.")
        else:
            return board

    def solve_genetics(self):
        # Placeholder for Genetics algorithm
        # Replace with actual implementation
        return [[0] * self.n_var.get() for _ in range(self.n_var.get())]

    def show_solution_board(self, board):
        # Page 3: Solution Display Page
        self.algorithm_frame.destroy()

        self.output_frame = tk.Frame(self.master, bg="#D3D3D3")  # Set background color
        self.output_frame.pack()

        canvas = tk.Canvas(self.output_frame, width=50 * self.n_var.get(), height=50 * self.n_var.get(), bg="white")
        canvas.grid(row=0, column=0, padx=10, pady=10)

        for row in range(self.n_var.get()):
            for col in range(self.n_var.get()):
                color = "white" if (row + col) % 2 == 0 else "#87CEEB"  # Alternating white and light blue colors

                canvas.create_rectangle(col * 50, row * 50, (col + 1) * 50, (row + 1) * 50, fill=color,
                                        outline="black")

                label_text = str(board[row][col])
                label = tk.Label(canvas, text=label_text, width=4, height=2, relief="ridge", borderwidth=2)
                label.place(x=col * 50 + 25, y=row * 50 + 25,
                            anchor="center")  # Place label in the center of each square


if __name__ == "__main__":
    root = tk.Tk()
    app = KnightTourSolver(root)
    root.mainloop()
