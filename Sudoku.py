import tkinter as tk
from tkinter import messagebox
import random
import copy

class SudokuApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sudoku")
        self.grid = [[0 for _ in range(9)] for _ in range(9)]  # Solved grid
        self.puzzle = None  # Puzzle with blanks
        self.entries = [[None for _ in range(9)] for _ in range(9)]  # UI entries
        self.create_ui()
        self.new_game()

    def create_ui(self):
        # Create 9x9 grid
        for i in range(9):
            for j in range(9):
                entry = tk.Entry(self.root, width=3, justify="center", font=("Arial", 16))
                entry.grid(row=i, column=j, padx=1 if j % 3 != 0 else 2, pady=1 if i % 3 != 0 else 2)
                entry.bind("<KeyRelease>", self.validate_input)  # Real-time validation
                self.entries[i][j] = entry

        # Buttons
        btn_frame = tk.Frame(self.root)
        btn_frame.grid(row=9, column=0, columnspan=9, pady=10)
        tk.Button(btn_frame, text="New Game", command=self.new_game).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Check", command=self.check_solution).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Reset", command=self.reset_game).pack(side=tk.LEFT, padx=5)

    def is_valid(self, grid, row, col, num):
        # Check row and column
        for x in range(9):
            if grid[row][x] == num or grid[x][col] == num:
                return False
        # Check 3x3 subgrid
        start_row, start_col = 3 * (row // 3), 3 * (col // 3)
        for i in range(3):
            for j in range(3):
                if grid[start_row + i][start_col + j] == num:
                    return False
        return True

    def solve_sudoku(self, grid):
        for i in range(9):
            for j in range(9):
                if grid[i][j] == 0:
                    for num in range(1, 10):
                        if self.is_valid(grid, i, j, num):
                            grid[i][j] = num
                            if self.solve_sudoku(grid):
                                return True
                            grid[i][j] = 0
                    return False
        return True

    def generate_puzzle(self):
        # Generate a solved grid
        self.grid = [[0 for _ in range(9)] for _ in range(9)]
        self.solve_sudoku(self.grid)
        # Create a copy and remove numbers
        self.puzzle = copy.deepcopy(self.grid)
        for _ in range(40):  # Adjust this number for difficulty (e.g., 30-50)
            row, col = random.randint(0, 8), random.randint(0, 8)
            self.puzzle[row][col] = 0
        return self.puzzle

    def display_puzzle(self):
        for i in range(9):
            for j in range(9):
                self.entries[i][j].delete(0, tk.END)
                if self.puzzle[i][j] != 0:
                    self.entries[i][j].insert(0, self.puzzle[i][j])
                    self.entries[i][j].config(state="disabled", disabledforeground="black")
                else:
                    self.entries[i][j].config(state="normal", bg="white")

    def new_game(self):
        self.generate_puzzle()
        self.display_puzzle()

    def reset_game(self):
        self.display_puzzle()

    def validate_input(self, event):
        entry = event.widget
        row, col = None, None
        # Find the entry's position
        for i in range(9):
            for j in range(9):
                if self.entries[i][j] == entry:
                    row, col = i, j
                    break
            if row is not None:
                break
        
        val = entry.get()
        if val and not val.isdigit():
            entry.delete(0, tk.END)  # Clear non-numeric input
        elif val and (int(val) < 1 or int(val) > 9):
            entry.delete(0, tk.END)  # Clear out-of-range input

    def check_solution(self):
        # Build current grid from entries
        current = [[0 for _ in range(9)] for _ in range(9)]
        for i in range(9):
            for j in range(9):
                val = self.entries[i][j].get()
                current[i][j] = int(val) if val else 0

        # Check if it matches the solution or is valid
        is_complete = all(current[i][j] != 0 for i in range(9) for j in range(9))
        is_correct = all(current[i][j] == self.grid[i][j] for i in range(9) for j in range(9))

        if is_complete and is_correct:
            messagebox.showinfo("Sudoku", "Congratulations! You solved it!")
        elif is_complete:
            messagebox.showerror("Sudoku", "The grid is full, but there’s a mistake.")
        else:
            messagebox.showwarning("Sudoku", "Keep going—some cells are empty or incorrect.")

if __name__ == "__main__":
    root = tk.Tk()
    app = SudokuApp(root)
    root.mainloop()