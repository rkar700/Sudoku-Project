import pygame
from cell import Cell
from sudoku_generator import generate_sudoku
class Board:
    def __init__(self, width, height, screen, difficulty):
        self.width = width
        self.height = height
        self.screen = screen
        self.difficulty = difficulty
        self.selected_cell = None
        self.cells = []
        self.board = []
        self.original = []
        self.create_board()

    def create_board(self):
        removed = 30 if self.difficulty == 'easy' else 40 if self.difficulty == 'medium' else 50
        self.board = generate_sudoku(9, removed)
        self.original = [row[:] for row in self.board]
        self.cells = [[Cell(self.board[r][c], r, c, self.screen, self.width, self.height) for c in range(9)] for r in range(9)]

    def draw(self):
        cell_size = self.width // 9
        for i in range(10):
            line_width = 4 if i % 3 == 0 else 1
            pygame.draw.line(self.screen, (0, 0, 0), (0, i * cell_size), (self.width, i * cell_size), line_width)
            pygame.draw.line(self.screen, (0, 0, 0), (i * cell_size, 0), (i * cell_size, self.height), line_width)

        for row in self.cells:
            for cell in row:
                cell.draw()

    def select(self, row, col):
        if self.selected_cell:
            self.cells[self.selected_cell[0]][self.selected_cell[1]].selected = False
        self.cells[row][col].selected = True
        self.selected_cell = (row, col)

    def click(self, x, y):
        if x < self.width and y < self.height:
            cell_size = self.width // 9
            return (y//cell_size, x // cell_size)
        return None

    def clear(self):
        if self.selected_cell:
            row, col = self.selected_cell
            if self.original[row][col] == 0:
                self.cells[row][col].value = 0
                self.cells[row][col].sketched_value = 0

    def sketch(self, value):
        if self.selected_cell:
            row, col = self.selected_cell
            self.cells[row][col].set_sketched_value(value)

    def place_number(self, value):
        if self.selected_cell:
            row, col = self.selected_cell
            self.cells[row][col].set_cell_value(value)

    def reset_to_original(self):
        for r in range(9):
            for c in range(9):
                self.cells[r][c].value = self.original[r][c]
                self.cells[r][c].sketched_value = 0

    def is_full(self):
        return all(cell.value != 0 for row in self.cells for cell in row)

    def update_board(self):
        for r in range(9):
            for c in range(9):
                self.board[r][c] = self.cells[r][c].value

    def find_empty(self):
        for r in range(9):
            for c in range(9):
                if self.cells[r][c].value == 0:
                    return (r, c)
        return None

    def check_board(self):
        self.update_board()
        for r in range(9):
            row_vals = set()
            col_vals = set()
            for c in range(9):
                if self.board[r][c] in row_vals or self.board[c][r] in col_vals:
                    return False
                row_vals.add(self.board[r][c])
                col_vals.add(self.board[c][r])

        for i in range(0, 9, 3):
            for j in range(0, 9, 3):
                block = set()
                for r in range(3):
                    for c in range(3):
                        val = self.board[i + r][j + c]
                        if val in block:
                            return False
                        block.add(val)
        return True
