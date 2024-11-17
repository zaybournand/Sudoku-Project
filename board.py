from cell import Cell

class Board:
    def __init__(self, width, height, screen, board):
        self.width = width
        self.height = height
        self.screen = screen
        self.cells = [[Cell(board[r][c], r, c, screen) for c in range(9)] for r in range(9)]

    def draw(self):
        for row in self.cells:
            for cell in row:
                cell.draw()
