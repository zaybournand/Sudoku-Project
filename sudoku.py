import pygame
from sudoku_generator import SudokuGenerator
from board import Board

def main():
    pygame.init()
    screen = pygame.display.set_mode((600, 700))
    pygame.display.set_caption("Sudoku")

    # Colors and Fonts
    white = (255, 255, 255)
    font = pygame.font.Font(None, 36)

    # Start Screen
    def game_start_screen():
        screen.fill(white)
        easy_button = pygame.Rect(200, 300, 200, 50)
        medium_button = pygame.Rect(200, 400, 200, 50)
        hard_button = pygame.Rect(200, 500, 200, 50)

        pygame.draw.rect(screen, (0, 0, 0), easy_button)
        pygame.draw.rect(screen, (0, 0, 0), medium_button)
        pygame.draw.rect(screen, (0, 0, 0), hard_button)

        screen.blit(font.render("Easy", True, white), (250, 310))
        screen.blit(font.render("Medium", True, white), (240, 410))
        screen.blit(font.render("Hard", True, white), (250, 510))

        pygame.display.flip()

        # Handle difficulty selection
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if easy_button.collidepoint(event.pos):
                        return 30  # Number of empty cells for easy
                    if medium_button.collidepoint(event.pos):
                        return 40  # Number of empty cells for medium
                    if hard_button.collidepoint(event.pos):
                        return 50  # Number of empty cells for hard

    # Main Game Loop
    difficulty = game_start_screen()
    sudoku = SudokuGenerator(9, difficulty)
    sudoku.fill_values()
    sudoku.remove_cells()
    board = Board(600, 600, screen, sudoku.get_board())

    running = True
    selected_cell = None  # To track the selected cell for input

    while running:
        screen.fill(white)
        board.draw()

        if selected_cell:
            # Highlight the selected cell
            row, col = selected_cell
            pygame.draw.rect(screen, (0, 255, 0), (col * 60, row * 60, 60, 60), 5)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                # Get mouse click position
                mouse_x, mouse_y = pygame.mouse.get_pos()

                # Calculate the row and column clicked (assuming a 9x9 grid with each cell being 60x60)
                row = mouse_y // 60
                col = mouse_x // 60

                # Handle selecting the cell
                if 0 <= row < 9 and 0 <= col < 9:
                    selected_cell = (row, col)  # Update selected cell

            if event.type == pygame.KEYDOWN and selected_cell:
                # Only allow input if a cell is selected

                row, col = selected_cell
                if event.key == pygame.K_1:
                    sudoku.get_board()[row][col] = 1
                elif event.key == pygame.K_2:
                    sudoku.get_board()[row][col] = 2
                elif event.key == pygame.K_3:
                    sudoku.get_board()[row][col] = 3
                elif event.key == pygame.K_4:
                    sudoku.get_board()[row][col] = 4
                elif event.key == pygame.K_5:
                    sudoku.get_board()[row][col] = 5
                elif event.key == pygame.K_6:
                    sudoku.get_board()[row][col] = 6
                elif event.key == pygame.K_7:
                    sudoku.get_board()[row][col] = 7
                elif event.key == pygame.K_8:
                    sudoku.get_board()[row][col] = 8
                elif event.key == pygame.K_9:
                    sudoku.get_board()[row][col] = 9

                # Update the board to reflect changes
                board.update_board(sudoku.get_board())  # Assuming `update_board` is a method of the Board class

    pygame.quit()

if __name__ == "__main__":
    main()
