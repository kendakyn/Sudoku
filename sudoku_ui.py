import tkinter as tk
from tkinter import messagebox
from sudoku_game import SudokuGame

class SudokuUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Sudoku")
        self.game = SudokuGame()
        self.entries = [[None for _ in range(9)] for _ in range(9)]
        self.create_ui()
        self.new_game()

    def create_ui(self):
        # Create 9x9 grid
        for i in range(9):
            for j in range(9):
                entry = tk.Entry(self.root, width=3, justify="center", font=("Arial", 16))
                entry.grid(row=i, column=j, padx=1 if j % 3 != 0 else 2, pady=1 if i % 3 != 0 else 2)
                entry.bind("<KeyRelease>", self.validate_input)
                self.entries[i][j] = entry

        # Buttons
        btn_frame = tk.Frame(self.root)
        btn_frame.grid(row=9, column=0, columnspan=9, pady=10)
        tk.Button(btn_frame, text="New Game", command=self.new_game).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Check", command=self.check_solution).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Reset", command=self.reset_game).pack(side=tk.LEFT, padx=5)

    def display_puzzle(self):
        puzzle = self.game.get_puzzle()
        for i in range(9):
            for j in range(9):
                self.entries[i][j].delete(0, tk.END)
                if puzzle[i][j] != 0:
                    self.entries[i][j].insert(0, puzzle[i][j])
                    self.entries[i][j].config(state="disabled", disabledforeground="black")
                else:
                    self.entries[i][j].config(state="normal", bg="lightblue")

    def new_game(self):
        self.game.generate_puzzle()
        self.display_puzzle()

    def reset_game(self):
        self.display_puzzle()

    def validate_input(self, event):
        entry = event.widget
        row, col = None, None
        for i in range(9):
            for j in range(9):
                if self.entries[i][j] == entry:
                    row, col = i, j
                    break
            if row is not None:
                break
        
        val = entry.get()
        if val and not val.isdigit():
            entry.delete(0, tk.END)
        elif val and (int(val) < 1 or int(val) > 9):
            entry.delete(0, tk.END)

    def check_solution(self):
        current = [[0 for _ in range(9)] for _ in range(9)]
        for i in range(9):
            for j in range(9):
                val = self.entries[i][j].get()
                current[i][j] = int(val) if val else 0

        solution = self.game.get_solution()
        is_complete = all(current[i][j] != 0 for i in range(9) for j in range(9))
        is_correct = all(current[i][j] == solution[i][j] for i in range(9) for j in range(9))

        if is_complete and is_correct:
            messagebox.showinfo("Sudoku", "Congratulations! You solved it!")
        elif is_complete:
            messagebox.showerror("Sudoku", "The grid is full, but there’s a mistake.")
        else:
            messagebox.showwarning("Sudoku", "Keep going—some cells are empty or incorrect.")