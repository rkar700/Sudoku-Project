import pygame
from sudoku_generator import SudokuGenerator

# Setup
pygame.init()

# Display and Fonts
SCREEN_WIDTH, SCREEN_HEIGHT = 540, 700
ROWS, COLS = 9, 9
CELL_WIDTH = SCREEN_WIDTH // COLS
BIG_FONT = pygame.font.SysFont("comicsans", 40)
SMALLER_FONT = pygame.font.SysFont("comicsans", 25)

# Palette
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
BLUE = (100, 149, 237)
RED = (255, 0, 0)
CRIMSON = (220, 20, 60)

# Board Logic
def create_board(size, blanks):
    generator = SudokuGenerator(size, blanks)
    generator.fill_values()
    generator.remove_cells()
    return generator.get_board()

# Draw Gridlines
def render_grid(surface):
    for i in range(ROWS + 1):
        thickness = 3 if i % 3 == 0 else 1
        pygame.draw.line(surface, BLACK, (0, i * CELL_WIDTH), (SCREEN_WIDTH, i * CELL_WIDTH), thickness)
        pygame.draw.line(surface, BLACK, (i * CELL_WIDTH, 0), (i * CELL_WIDTH, SCREEN_WIDTH), thickness)

# Render Numbers
def render_numbers(surface, board_state, original_positions, user_entries):
    surface.fill(WHITE)
    render_grid(surface)

    for row_idx, row in range(board_state):
        for col_idx, value in range(row):
            if value:
                cell_pos = (col_idx * CELL_WIDTH + 15, row_idx * CELL_WIDTH + 10)
                if (row_idx, col_idx) in original_positions:
                    text = BIG_FONT.render(str(value), True, BLUE)
                elif (row_idx, col_idx) in user_entries:
                    text = BIG_FONT.render(str(value), True, BLACK)
                else:
                    text = SMALLER_FONT.render(str(value), True, GRAY)
                surface.blit(text, cell_pos)

# Win Condition Checker
def check_win_condition(board):
    def is_valid(group):
        return sorted(group) == list(range(1, 10))

    for i in range(9):
        if not is_valid(board[i]) or not is_valid([board[j][i] for j in range(9)]):
            return False

    for r_base in (0, 3, 6):
        for c_base in (0, 3, 6):
            block = [board[r][c] for r in range(r_base, r_base + 3) for c in range(c_base, c_base + 3)]
            if not is_valid(block):
                return False
    return True

# Game Loop
def run_game():
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Sudoku Game")

    intro = pygame.image.load('Sudoku_Intro.png')
    win_screen = pygame.image.load('Win.png')
    lose_screen = pygame.image.load('Lose.png')

    clock = pygame.time.Clock()
    show_intro = True

    while show_intro:
        screen.blit(intro, (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if 30 <= x <= 180 and 560 <= y <= 630:
                    level = 30
                    show_intro = False
                elif 200 <= x <= 350 and 560 <= y <= 630:
                    level = 40
                    show_intro = False
                elif 375 <= x <= 530 and 560 <= y <= 630:
                    level = 50
                    show_intro = False
        pygame.display.flip()
        clock.tick(30)

    board = create_board(9, level)
    original_cells = [(r, c) for r in range(9) for c in range(9) if board[r][c] != 0]
    locked_cells = original_cells[:]
    user_board = [row[:] for row in board]
    selected_cell = None
    game_active = True

    while game_active:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if 50 <= x <= 220 and 650 <= y <= 680:
                    user_board = [row[:] for row in board]
                    locked_cells = original_cells[:]
                elif 250 <= x <= 375 and 650 <= y <= 680:
                    run_game()
                elif 450 <= x <= 520 and 650 <= y <= 680:
                    pygame.quit()
                elif y < SCREEN_WIDTH:
                    selected_cell = (y // CELL_WIDTH, x // CELL_WIDTH)
            elif event.type == pygame.KEYDOWN and selected_cell:
                r, c = selected_cell
                if (r, c) not in original_cells:
                    if pygame.K_1 <= event.key <= pygame.K_9:
                        user_board[r][c] = event.key - pygame.K_0
                    elif event.key == pygame.K_RETURN and (r, c) not in locked_cells:
                        locked_cells.append((r, c))
                    elif event.key in [pygame.K_BACKSPACE, pygame.K_DELETE]:
                        user_board[r][c] = 0
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()

        render_numbers(screen, user_board, original_cells, locked_cells)

        if selected_cell:
            r, c = selected_cell
            pygame.draw.rect(screen, CRIMSON, (c * CELL_WIDTH, r * CELL_WIDTH, CELL_WIDTH, CELL_WIDTH), 3)

        screen.blit(BIG_FONT.render("RESET", True, BLACK, CRIMSON), (50, 650))
        screen.blit(BIG_FONT.render("RESTART", True, BLACK, CRIMSON), (250, 650))
        screen.blit(BIG_FONT.render("EXIT", True, BLACK, CRIMSON), (450, 650))

        pygame.display.flip()

        if len(locked_cells) == 81:
            pygame.time.delay(1000)
            game_active = False
            win = check_win_condition(user_board)

        clock.tick(30)

    while win:
        screen.blit(win_screen, (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if 190 <= x <= 350 and 487 <= y <= 550:
                    pygame.quit()
        pygame.display.update()
        clock.tick(30)

    while not win:
        screen.blit(lose_screen, (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if 50 <= x <= 200 and 490 <= y <= 550:
                    pygame.quit()
                elif 315 <= x <= 465 and 490 <= y <= 555:
                    run_game()
        pygame.display.update()
        clock.tick(30)

if __name__ == "__main__":
    run_game()

#push