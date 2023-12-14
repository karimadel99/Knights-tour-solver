# knight_tour_solver.py
import tkinter as tk
from tkinter import ttk
from ttkthemes import ThemedStyle
import numpy as np
from tkinter import messagebox
from backtracking_solver import solve_knights_tour_backtracking
from genetics_solver import solve_genetics
from optimized_backtracking_solver import solve_optimized_backtracking

class KnightTourSolver:
    def __init__(self, master):
        self.master = master
        self.master.title("Knight's Tour Solver")

        # Set the style
        self.style = ThemedStyle(self.master)
        self.style.set_theme("plastik")

        # Variables for user input
        self.n_var = tk.IntVar()
        self.x_var = tk.IntVar()
        self.y_var = tk.IntVar()

        # Page 1: Input Page
        self.input_frame = tk.Frame(self.master, bg="#D3D3D3")
        self.input_frame.pack(pady=20)

        tk.Label(self.input_frame, text="Enter Board Size (N x N):", bg="#D3D3D3").grid(row=0, column=0, padx=10, pady=10)
        validate_input_cmd = self.master.register(self.validate_input)
        tk.Entry(self.input_frame, textvariable=self.n_var, validate="key", validatecommand=(validate_input_cmd, "%P")).grid(row=0, column=1, padx=10, pady=10)

        tk.Label(self.input_frame, text="Enter Starting Point (X, Y):", bg="#D3D3D3").grid(row=1, column=0, padx=10, pady=10)
        tk.Label(self.input_frame, text="X:", bg="#D3D3D3").grid(row=1, column=1, padx=5, pady=10)
        tk.Entry(self.input_frame, textvariable=self.x_var, validate="key", validatecommand=(validate_input_cmd, "%P")).grid(row=1, column=2, padx=5, pady=10)
        tk.Label(self.input_frame, text="Y:", bg="#D3D3D3").grid(row=1, column=3, padx=5, pady=10)
        tk.Entry(self.input_frame, textvariable=self.y_var, validate="key", validatecommand=(validate_input_cmd, "%P")).grid(row=1, column=4, padx=5, pady=10)

        next_btn = ttk.Button(self.input_frame, text="Next", command=self.show_algorithm_page, style="TButton")
        next_btn.grid(row=2, column=2, pady=20)

    def validate_input(self, value):
        return value.isdigit() or value == ""

    def show_algorithm_page(self):
        # Validate input
        if not self.n_var.get() or self.n_var.get() <= 0 or not (1 <= self.x_var.get() <= self.n_var.get()) or not (1 <= self.y_var.get() <= self.n_var.get()):
            messagebox.showerror("Error", "Invalid input. Please check the values.")
            return

        # Page 2: Algorithm Selection Page
        self.input_frame.destroy()

        self.algorithm_frame = tk.Frame(self.master, bg="#D3D3D3")
        self.algorithm_frame.pack(pady=30)

        tk.Label(self.algorithm_frame, text="Select Algorithm:", bg="#D3D3D3").grid(row=0, column=0, padx=10, pady=10)

        backtracking_btn = ttk.Button(self.algorithm_frame, text="Backtracking", command=self.show_solution_page_backtracking, style="TButton")
        backtracking_btn.grid(row=1, column=0, pady=10)

        genetics_btn = ttk.Button(self.algorithm_frame, text="Genetics", command=self.show_solution_page_genetics, style="TButton")
        genetics_btn.grid(row=1, column=1, pady=10)

        optimized_backtracking_btn = ttk.Button(self.algorithm_frame, text="Optimized Backtracking", command=self.show_solution_page_optimized_backtracking, style="TButton")
        optimized_backtracking_btn.grid(row=1, column=3, pady=10)

    def show_solution_page_backtracking(self):
        solution_board = solve_knights_tour_backtracking(self.n_var.get(), self.x_var.get(), self.y_var.get())
        self.show_solution_board(solution_board)

    def show_solution_page_genetics(self):
        # Placeholder for Genetics algorithm
        solution_board = solve_genetics(self.n_var.get())
        self.show_solution_board(solution_board)

    def show_solution_page_optimized_backtracking(self):
        solution_board = solve_optimized_backtracking(self.n_var.get(), self.x_var.get(), self.y_var.get())
        self.show_solution_board(solution_board)

    def show_solution_board(self, board):
        self.algorithm_frame.destroy()

        self.output_frame = tk.Frame(self.master, bg="#D3D3D3")
        self.output_frame.pack()

        canvas = tk.Canvas(self.output_frame, width=50 * self.n_var.get(), height=50 * self.n_var.get(), bg="white")
        canvas.grid(row=0, column=0, padx=10, pady=10)

        for row in range(self.n_var.get()):
            for col in range(self.n_var.get()):
                color = "white" if (row + col) % 2 == 0 else "#87CEEB"

                canvas.create_rectangle(col * 50, row * 50, (col + 1) * 50, (row + 1) * 50, fill=color,
                                        outline="black")

                label_text = str(board[row][col])
                label = tk.Label(canvas, text=label_text, width=4, height=2, relief="ridge", borderwidth=2)
                label.place(x=col * 50 + 25, y=row * 50 + 25, anchor="center")


if __name__ == "__main__":
    root = tk.Tk()
    app = KnightTourSolver(root)
    root.mainloop()
