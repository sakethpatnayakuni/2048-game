import pygame
import random
import numpy as np

# Initialize Pygame
pygame.init()

# Constants
SIZE = 6
TILE_SIZE = 100
GRID_SIZE = SIZE * TILE_SIZE
BACKGROUND_COLOR = (187, 173, 160)
EMPTY_COLOR = (204, 192, 179)
TILE_COLORS = {
    2: (238, 228, 218),
    4: (237, 224, 200),
    8: (242, 177, 121),
    16: (245, 149, 99),
    32: (246, 124, 95),
    64: (246, 94, 59),
    128: (237, 207, 114),
    256: (237, 204, 97),
    512: (237, 200, 80),
    1024: (237, 197, 63),
    2048: (237, 194, 46)
}
TEXT_COLOR = (255, 255, 255)
FONT_SIZE = 40

# Initialize the display
screen = pygame.display.set_mode((GRID_SIZE, GRID_SIZE))
pygame.display.set_caption('2048')

# Define game functions
def init_game():
    board = np.zeros((SIZE, SIZE), dtype=int)
    add_random_tile(board)
    add_random_tile(board)
    return board

def add_random_tile(board):
    empty_positions = np.argwhere(board == 0)
    if empty_positions.size == 0:
        return
    i, j = empty_positions[random.randint(0, empty_positions.shape[0] - 1)]
    board[i, j] = random.choice([2])  # You can add more values for more complexity

def draw_board(board):
    screen.fill(BACKGROUND_COLOR)
    font = pygame.font.Font(None, FONT_SIZE)
    
    for i in range(SIZE):
        for j in range(SIZE):
            value = board[i, j]
            rect = pygame.Rect(j * TILE_SIZE, i * TILE_SIZE, TILE_SIZE, TILE_SIZE)
            color = TILE_COLORS.get(value, EMPTY_COLOR)
            pygame.draw.rect(screen, color, rect)
            if value != 0:
                text_surface = font.render(str(value), True, TEXT_COLOR)
                text_rect = text_surface.get_rect(center=rect.center)
                screen.blit(text_surface, text_rect)
    
    pygame.display.flip()

def compress(board):
    new_board = np.zeros_like(board)
    for row in range(SIZE):
        new_row = [num for num in board[row] if num != 0]
        new_row_merged = []
        skip = False
        for i in range(len(new_row)):
            if skip:
                skip = False
                continue
            if i + 1 < len(new_row) and new_row[i] == new_row[i + 1]:
                new_row_merged.append(new_row[i] * 2)
                skip = True
            else:
                new_row_merged.append(new_row[i])
        new_row_merged.extend([0] * (SIZE - len(new_row_merged)))
        new_board[row] = new_row_merged
    return new_board

def reverse(board):
    return np.fliplr(board)

def transpose(board):
    return np.transpose(board)

def move_left(board):
    new_board = compress(board)
    return new_board, not np.array_equal(board, new_board)

def move_right(board):
    reversed_board = reverse(board)
    new_board, moved = move_left(reversed_board)
    return reverse(new_board), moved

def move_up(board):
    transposed_board = transpose(board)
    new_board, moved = move_left(transposed_board)
    return transpose(new_board), moved

def move_down(board):
    transposed_board = transpose(board)
    new_board, moved = move_right(transposed_board)
    return transpose(new_board), moved

def main():
    board = init_game()
    draw_board(board)
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                moved = False
                if event.key == pygame.K_LEFT:
                    board, moved = move_left(board)
                elif event.key == pygame.K_RIGHT:
                    board, moved = move_right(board)
                elif event.key == pygame.K_UP:
                    board, moved = move_up(board)
                elif event.key == pygame.K_DOWN:
                    board, moved = move_down(board)
                
                if moved:
                    add_random_tile(board)
                    draw_board(board)
    
    pygame.quit()

if __name__ == "__main__":
    main()
