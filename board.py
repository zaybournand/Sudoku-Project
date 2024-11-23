import pygame
from cell import Cell


class Board:
    def __init__(self, width, height, screen, sudoku_board):
        self.width = width
        self.height = height
        self.screen = screen
        self.sudoku_board = sudoku_board  # Board passed as 2D list
        # Create the cells based on the provided board
        self.cells = [[Cell(self.sudoku_board[r][c], r, c, screen, self.sudoku_board[r][c] != 0) for c in range(9)] for
                      r in range(9)]
        self.selected_cell = None  # To track the selected cell
        self.result_screen = None  # Tracks if the result screen is to be displayed

    def draw(self):
        if self.result_screen:
            # Display result screen
            self.display_result()
        else:
            # Draw the grid lines for the Sudoku board
            for row in range(9):
                for col in range(9):
                    x, y = col * 60, row * 60

                    # Draw the thicker lines for 3x3 subgrids
                    if col % 3 == 0 and col != 0:
                        pygame.draw.line(self.screen, (0, 0, 0), (x, 0), (x, self.height), 4)  # Vertical
                    if row % 3 == 0 and row != 0:
                        pygame.draw.line(self.screen, (0, 0, 0), (0, y), (self.width, y), 4)  # Horizontal

                    # Draw the normal thin grid lines for the cells
                    pygame.draw.line(self.screen, (0, 0, 0), (x, 0), (x, self.height), 1)  # Vertical
                    pygame.draw.line(self.screen, (0, 0, 0), (0, y), (self.width, y), 1)  # Horizontal

            # Draw all cells (numbers or background)
            for row in self.cells:
                for cell in row:
                    cell.draw()

    def select(self, row, col):
        # Marks the cell at (row, col) as selected
        if self.selected_cell:
            self.selected_cell.selected = False  # Unselect the previous cell
        self.selected_cell = self.cells[row][col]
        self.selected_cell.selected = True

    def click(self, x, y):
        # Checks if a click is within the board's cells and returns the corresponding (row, col)
        if 0 <= x < self.width and 0 <= y < self.height:
            row, col = y // 60, x // 60
            return row, col
        return None

    def clear(self):
        # Clears the value and sketch of the selected cell (only if it's user-entered)
        if self.selected_cell and not self.selected_cell.immutable:
            self.selected_cell.value = 0
            self.selected_cell.sketch_value = None

    def sketch(self, value):
        # Sets the sketched value for the selected cell
        if self.selected_cell and not self.selected_cell.immutable:
            self.selected_cell.set_sketched_value(value)

    def place_number(self, value):
        # Sets the value of the selected cell (when Enter is pressed)
        if self.selected_cell and not self.selected_cell.immutable:
            self.selected_cell.set_cell_value(value)

    def reset_to_original(self):
        # Resets the board to the original values
        for row in self.cells:
            for cell in row:
                if cell.immutable:
                    cell.value = cell.sketch_value = None
                else:
                    cell.value = 0

    def is_full(self):
        # Checks if the board is full (no empty cells)
        for row in self.cells:
            for cell in row:
                if cell.value == 0:
                    return False
        return True

    def update_board(self, new_board):
        # Updates the underlying 2D board with the values from the new board
        self.sudoku_board = new_board
        for row in range(9):
            for col in range(9):
                self.cells[row][col].value = new_board[row][col]

    def find_empty(self):
        # Finds an empty cell and returns its (row, col)
        for row in range(9):
            for col in range(9):
                if self.cells[row][col].value == 0:
                    return row, col
        return None

    def check_board(self):
        # Check if the Sudoku board is solved correctly
        # Check rows, columns, and 3x3 sub-grids for duplicates
        for row in range(9):
            if not self.check_row(row):
                return False
        for col in range(9):
            if not self.check_column(col):
                return False
        for row in range(0, 9, 3):
            for col in range(0, 9, 3):
                if not self.check_subgrid(row, col):
                    return False
        return True

    def check_row(self, row):
        # Check for duplicates in a row
        values = [self.cells[row][col].value for col in range(9)]
        return self.no_duplicates(values)

    def check_column(self, col):
        # Check for duplicates in a column
        values = [self.cells[row][col].value for row in range(9)]
        return self.no_duplicates(values)

    def check_subgrid(self, row, col):
        # Check for duplicates in a 3x3 subgrid
        values = []
        for r in range(row, row + 3):
            for c in range(col, col + 3):
                values.append(self.cells[r][c].value)
        return self.no_duplicates(values)

    def reset_to_original(self):
        """Resets the board to its original state, but only clears user-modified cells."""
        for row in self.cells:
            for cell in row:
                if cell.modified:  # Only reset cells that were modified by the user
                    cell.value = 0  # Clear the user-modified value
                    cell.modified = False  # Mark as unmodified

    def no_duplicates(self, values):
        # Helper function to check for duplicates (ignores zeros)
        seen = set()
        for value in values:
            if value != 0:
                if value in seen:
                    return False
                seen.add(value)
        return True

    def check_for_winner(self):
        if self.is_full():
            if self.check_board():
                self.result_screen = "win"  # Set win screen
            else:
                self.result_screen = "lose"  # Set lose screen

    def display_result(self):
        font = pygame.font.SysFont("Arial", 36)
        if self.result_screen == "win":
            message = "You Win!"
        else:
            message = "You Lost! :("

        text = font.render(message, True, (0, 255, 0) if self.result_screen == "win" else (255, 0, 0))
        self.screen.blit(text, (self.width // 2 - text.get_width() // 2, self.height // 3))

        # Draw Restart and Exit Buttons (simple rectangles for now)
        restart_button = pygame.Rect(self.width // 4 - 75, self.height // 2 + 50, 150, 50)
        exit_button = pygame.Rect(3 * self.width // 4 - 75, self.height // 2 + 50, 150, 50)
        pygame.draw.rect(self.screen, (0, 0, 255), restart_button)
        pygame.draw.rect(self.screen, (255, 0, 0), exit_button)

        # Add text to buttons
        restart_text = font.render("Restart", True, (255, 255, 255))
        exit_text = font.render("Exit", True, (255, 255, 255))
        self.screen.blit(restart_text, (self.width // 4 - restart_text.get_width() // 2, self.height // 2 + 60))
        self.screen.blit(exit_text, (3 * self.width // 4 - exit_text.get_width() // 2, self.height // 2 + 60))

        pygame.display.update()
