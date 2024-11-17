import pygame

class Cell:
    def __init__(self, value, row, col, screen):
        self.value = value
        self.row = row
        self.col = col
        self.screen = screen
        self.selected = False

    def draw(self):
        font = pygame.font.Font(None, 36)
        x, y = self.col * 60, self.row * 60
        pygame.draw.rect(self.screen, (0, 0, 0), (x, y, 60, 60), 1)
        if self.value != 0:
            text = font.render(str(self.value), True, (0, 0, 0))
            self.screen.blit(text, (x + 20, y + 15))
        if self.selected:
            pygame.draw.rect(self.screen, (255, 0, 0), (x, y, 60, 60), 3)
