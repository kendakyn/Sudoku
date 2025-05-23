import random
import copy

class SudokuGame:
    def __init__(self):
        self.grid = [[0 for _ in range(9)] for _ in range(9)]  # Solved grid
        self.puzzle = None  # Puzzle with blanks

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
        for _ in range(40):  # Adjust for difficulty
            row, col = random.randint(0, 8), random.randint(0, 8)
            self.puzzle[row][col] = 0
        return self.puzzle

    def get_solution(self):
        return self.grid

    def get_puzzle(self):
        return self.puzzle