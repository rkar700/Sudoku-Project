import pygame

class Cell:

    def __init__(self, value, row, col, screen,width,height):
        self.value = value
        self.row = row
        self.col = col
        self.sketched_value = value
        self.screen = screen
        self.selected = False
        self.width = width
        self.height = height
        self.original = value!=0

    def set_cell_value(self, value):
        if not self.original:
            self.value = value

    def set_sketched_value(self, value):
        if not self.original:
            self.sketched_value = value

    def draw(self):

        cell_size = self.width//9     #the board size is 540x700
        x = self.col *cell_size
        y = self.row *cell_size
        font = pygame.font.Font(None,100)
        if self.value != 0:
            text=font.render(self.value, True, (0,0,0))
            self.screen.blit(text, (x + (cell_size//2 - text.get_width()//2), y + (cell_size//2 - text.get_height()//2)))
        elif:
            small_font = pygame.font.SysFont("comicsans", 20)
            text = small_font.render(str(self.sketched_value), True, (128, 128, 128))
            self.screen.blit(text, (x + 5, y + 5))
        if self.selected:
            pygame.draw.rect(self.screen, (255, 0, 0), (x, y, cell_size, cell_size), 3)




