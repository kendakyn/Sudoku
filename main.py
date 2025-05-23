import tkinter as tk
from sudoku_ui import SudokuUI

if __name__ == "__main__":
    root = tk.Tk()
    app = SudokuUI(root)
    root.mainloop()