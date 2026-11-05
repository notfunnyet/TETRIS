import pygame
import random
import sys

pygame.init()

CELL = 30
COLS = 10
ROWS = 20
WIDTH = COLS * CELL
HEIGHT = ROWS * CELL

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("TETRIS")

clock = pygame.time.Clock()
font = pygame.font.SysFont("Comic Sans MS", 25)

# Cores
BLACK = (15, 15, 20)
WHITE = (240, 240, 240)

SHAPES = [
    [[1, 1, 1, 1]],
    [[1, 1], [1, 1]],
    [[0, 1, 0], [1, 1, 1]],
    [[1, 0, 0], [1, 1, 1]],
    [[0, 0, 1], [1, 1, 1]],
    [[1, 1, 0], [0, 1, 1]],
    [[0, 1, 1], [1, 1, 0]]
]

COLORS = [
    (0, 220, 255),
    (255, 220, 0),
    (160, 80, 255),
    (255, 140, 0),
    (50, 100, 255),
    (50, 220, 100),
    (255, 70, 70)
]

board = [[BLACK for _ in range(COLS)] for _ in range(ROWS)]

score = 0
game_over = False

def new_piece():
    index = random.randrange(len(SHAPES))
    return {
        "shape": SHAPES[index],
        "color": COLORS[index],
        "x": COLS // 2 - 2,
        "y": 0
    }

piece = new_piece()

def valid(piece, dx=0, dy=0, shape=None):
    shape = shape or piece["shape"]

    for y, row in enumerate(shape):
        for x, cell in enumerate(row):
            if cell:
                nx = piece["x"] + x + dx
                ny = piece["y"] + y + dy

                if nx < 0 or nx >= COLS or ny >= ROWS:
                    return False

                if ny >= 0 and board[ny][nx] != BLACK:
                    return False

    return True

def lock_piece():
    global piece, game_over, score

    for y, row in enumerate(piece["shape"]):
        for x, cell in enumerate(row):
            if cell:
                px = piece["x"] + x
                py = piece["y"] + y

                if py < 0:
                    game_over = True
                else:
                    board[py][px] = piece["color"]

    new_board = [row for row in board if BLACK in row]
    cleared = ROWS - len(new_board)

    score += cleared * 100

    for _ in range(cleared):
        new_board.insert(0, [BLACK for _ in range(COLS)])

    board[:] = new_board

    piece = new_piece()

    if not valid(piece):
        game_over = True

def rotate_piece():
    rotated = [list(row) for row in zip(*piece["shape"][::-1])]

    if valid(piece, shape=rotated):
        piece["shape"] = rotated

def draw():
    screen.fill(BLACK)

    for y in range(ROWS):
        for x in range(COLS):
            rect = pygame.Rect(
                x * CELL, y * CELL, CELL, CELL
            )

            pygame.draw.rect(screen, board[y][x], rect)
            pygame.draw.rect(screen, (40, 40, 50), rect, 1)

    # Peça atual
    for y, row in enumerate(piece["shape"]):
        for x, cell in enumerate(row):
            if cell:
                rect = pygame.Rect(
                    (piece["x"] + x) * CELL,
                    (piece["y"] + y) * CELL,
                    CELL, CELL
                )

                pygame.draw.rect(screen, piece["color"], rect)
                pygame.draw.rect(screen, WHITE, rect, 1)

    text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(text, (8, 5))

    if game_over:
        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.set_alpha(180)
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (0, 0))

        msg = font.render("GAME OVER", True, (255, 80, 80))
        screen.blit(msg, (WIDTH // 2 - 75, HEIGHT // 2 - 15))

        restart = pygame.font.SysFont("Arial", 16).render(
            "Pressione R para reiniciar", True, WHITE
        )
        screen.blit(restart, (WIDTH // 2 - 95, HEIGHT // 2 + 25))

    pygame.display.flip()

fall_timer = 0
fall_speed = 500

while True:
    dt = clock.tick(60)
    fall_timer += dt

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:

            if game_over and event.key == pygame.K_r:
                board = [[BLACK for _ in range(COLS)] for _ in range(ROWS)]
                score = 0
                game_over = False
                piece = new_piece()

            elif not game_over:
                if event.key == pygame.K_LEFT and valid(piece, dx=-1):
                    piece["x"] -= 1

                elif event.key == pygame.K_RIGHT and valid(piece, dx=1):
                    piece["x"] += 1

                elif event.key == pygame.K_DOWN and valid(piece, dy=1):
                    piece["y"] += 1

                elif event.key == pygame.K_UP:
                    rotate_piece()

                elif event.key == pygame.K_SPACE:
                    while valid(piece, dy=1):
                        piece["y"] += 1
                    lock_piece()

    if not game_over and fall_timer >= fall_speed:
        if valid(piece, dy=1):
            piece["y"] += 1
        else:
            lock_piece()

        fall_timer = 0

    draw()
