import sys
import random
import pygame

pygame.init()
info = pygame.display.Info()

WIDTH, HEIGHT = info.current_w, info.current_h

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Langton's Ant.")
clock = pygame.time.Clock()

CELL_SIZE = 6
ROWS, COLS = HEIGHT // CELL_SIZE, WIDTH // CELL_SIZE
grid = [[0 for _ in range(COLS)] for _ in range(ROWS)]
stop = False

FILL_COLOR = 'white'
EMPTY_COLOR = 'black'

ant_position = ROWS // 2, COLS // 2

# Directions are ordered clock-wise. This way we can increase the index to go clockwise or decrese to go anti-clockwise
directions = ((0, 1), (1, 0), (0, -1), (-1, 0))
direction_index = random.randint(0, len(directions) -1)

# I tried to make this code run fast on large grids without using additional modules.
# I only made small optimizations, but you can achieve faster performance with modules like Numba or NumPy.
def update(grid):
    global direction_index, ant_position

    direction = directions[direction_index]
    ant_position = (ant_position[0] + direction[0]) % ROWS, (ant_position[1] + direction[1]) % COLS

    if grid[ant_position[0]][ant_position[1]]:
        grid[ant_position[0]][ant_position[1]] = 0
        # Limit the index
        direction_index += 1
        if direction_index >= len(directions):
            direction_index = 0
    else:
        grid[ant_position[0]][ant_position[1]] = 1
        # Limit the index
        direction_index -= 1
        if direction_index < 0:
            direction_index = len(directions) -1

    # Only draw the ant's current position
    color = FILL_COLOR if grid[ant_position[0]][ant_position[1]] else EMPTY_COLOR
    pygame.draw.rect(screen, color, [ant_position[1] * CELL_SIZE, ant_position[0] * CELL_SIZE, CELL_SIZE -1, CELL_SIZE -1])

screen.fill(EMPTY_COLOR)
run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                run = False

            if event.key == pygame.K_SPACE:
                stop = not stop

            # Reset the board
            if event.key == pygame.K_r:
                grid = [[0 for _ in range(COLS)] for _ in range(ROWS)]
                ant_position = ROWS // 2, COLS // 2
                direction_index = random.randint(0, len(directions) -1)
                screen.fill(EMPTY_COLOR)
    if not stop:
        update(grid)
    pygame.display.flip()

pygame.quit()
sys.exit()
