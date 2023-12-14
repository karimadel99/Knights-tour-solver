# main.py
import tkinter as tk
from knight_tour_solver import KnightTourSolver

if __name__ == "__main__":
    root = tk.Tk()
    app = KnightTourSolver(root)
    root.mainloop()
