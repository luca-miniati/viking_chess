import pygame
from pygame.constants import KEYDOWN
from pygame.event import get

WIDTH = 11 * 60
HEIGHT = 11 * 60

DISPLAY = pygame.display.set_mode((WIDTH + 2, HEIGHT + 2))
CLOCK = pygame.time.Clock()
FPS = 60

NUM_BOXES = 11
BOX_WIDTH = WIDTH / NUM_BOXES

DARK = (108, 136, 166)
LIGHT = (191, 223, 255)
GRAY = (50, 50, 50)
WHITE = (255, 255, 255)
BROWN = (89, 56, 40)
RED = (240, 112, 98)
YELLOW = (255, 251, 140)

START = None
DEST = None
CLICKING = False
MOVE = 'white'

GRID = [
    [0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0],
    [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 0, 0, 0, 0, 2, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 2, 2, 2, 0, 0, 0, 1],
    [1, 1, 0, 2, 2, 3, 2, 2, 0, 1, 1],
    [1, 0, 0, 0, 2, 2, 2, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 2, 0, 0, 0, 0, 1],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
    [0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0]
]

def draw_grid():
    for i in range(0, NUM_BOXES + 1):
        pygame.draw.line(DISPLAY, GRAY, (i * BOX_WIDTH, 0), (i * BOX_WIDTH, HEIGHT), 2)
    for j in range(0, NUM_BOXES + 1):
        pygame.draw.line(DISPLAY, GRAY, (0, j * BOX_WIDTH), (WIDTH, j * BOX_WIDTH), 2)

def color_squares():
    pygame.draw.rect(DISPLAY, RED, pygame.Rect(0, 0, BOX_WIDTH, BOX_WIDTH))
    pygame.draw.rect(DISPLAY, RED, pygame.Rect(WIDTH - BOX_WIDTH, 0, BOX_WIDTH, BOX_WIDTH))
    pygame.draw.rect(DISPLAY, RED, pygame.Rect(0, HEIGHT - BOX_WIDTH, BOX_WIDTH, BOX_WIDTH))
    pygame.draw.rect(DISPLAY, RED, pygame.Rect(WIDTH - BOX_WIDTH, HEIGHT - BOX_WIDTH, BOX_WIDTH, BOX_WIDTH))
    if CLICKING:
        for square in get_legal_moves(START):
            y, x = square
            pygame.draw.rect(DISPLAY, YELLOW, pygame.Rect(x * BOX_WIDTH, y * BOX_WIDTH, BOX_WIDTH, BOX_WIDTH))

def draw_pieces():
    drag_img = None
    for i in range(0, len(GRID)):
        for j in range(0, len(GRID)):
            if GRID[i][j] == 0:
                continue
            elif GRID[i][j] == 1:
                img = pygame.transform.smoothscale(pygame.image.load('pieces/black/r.png'), (BOX_WIDTH, BOX_WIDTH))
            elif GRID[i][j] == 2:
                img = pygame.transform.smoothscale(pygame.image.load('pieces/white/R.png'), (BOX_WIDTH, BOX_WIDTH))
            elif GRID[i][j] == 3:
                img = pygame.transform.smoothscale(pygame.image.load('pieces/white/K.png'), (BOX_WIDTH, BOX_WIDTH))
        
            if CLICKING:
                if (i, j) == START:
                    if GRID[i][j] == 1:
                        drag_img = pygame.transform.smoothscale(pygame.image.load('pieces/black/r.png'), (BOX_WIDTH, BOX_WIDTH))
                    elif GRID[i][j] == 2:
                        drag_img = pygame.transform.smoothscale(pygame.image.load('pieces/white/R.png'), (BOX_WIDTH, BOX_WIDTH))
                    elif GRID[i][j] == 3:
                        drag_img = pygame.transform.smoothscale(pygame.image.load('pieces/white/K.png'), (BOX_WIDTH, BOX_WIDTH))
                    continue

            DISPLAY.blit(img, (j * BOX_WIDTH, i * BOX_WIDTH))
    
    if drag_img != None:
        x, y = pygame.mouse.get_pos()
        DISPLAY.blit(drag_img, (x - BOX_WIDTH / 2, y - BOX_WIDTH / 2))
            

def mouse_to_coordinate(mouse_pos):
    x, y = mouse_pos
    return (int(y / BOX_WIDTH), int(x / BOX_WIDTH))

def move(start, dest):
    if dest not in get_legal_moves(start):
        return False
    y, x = dest
    if GRID[y][x] == 0:
        y, x = start
        piece = GRID[y][x]
        GRID[y][x] = 0
        y, x = dest
        GRID[y][x] = piece
        return True

def piece_on_edge(start, edge):
    y, x = start
    d, m = edge
    if d == 'y':
        if y == m:
            return True
    if d == 'x':
        if x == m:
            return True
    return False

def is_opposite_color(a, b):
    ay, ax = a
    by, bx = b
    if GRID[ay][ax] == GRID[by][bx]:
        return False
    elif GRID[ay][ax] == 0:
        return False
    elif GRID[by][bx] == 0:
        return False
    else:
        return True
        
def win(color):
    if color == 'white':
        img = pygame.transform.smoothscale(pygame.image.load('white_wins.png'), (595, 69))
        DISPLAY.blit(img, (WIDTH/2 - img.get_width()/2, HEIGHT/2 - img.get_height()/2))
    if color == 'black':
        img = pygame.transform.smoothscale(pygame.image.load('black_wins.png'), (594, 69))
        DISPLAY.blit(img, (WIDTH/2 - img.get_width()/2, HEIGHT/2 - img.get_height()/2))

def is_capture(a, b):
    ay, ax = a
    by, bx = b
    if GRID[ay][ax] == 1:
        if GRID[by][bx] == 1:
            return True
        else:
            return False
    if GRID[ay][ax] == 2:
        if GRID[by][bx] == 2 or GRID[by][bx] == 3:
            return True
        else:
            return False
    if GRID[ay][ax] == 3:
        if GRID[by][bx] == 2:
            return True
        else:
            return False

def check_captures(dest):
    captures = []
    # top
    y, x = dest
    if y != 0:
        if is_opposite_color(dest, (y - 1, x)):
            if not piece_on_edge((y - 1, x), ('y', 0)):
                if is_capture((y - 2, x), (y, x)):
                    captures.append((y - 1, x))
    # bottom
    if y != 10:
        if is_opposite_color(dest, (y + 1, x)):
            if not piece_on_edge((y + 1, x), ('y', 10)):
                if is_capture((y + 2, x), (y, x)):
                    captures.append((y + 1, x))
    # right
    if x != 10:
        if is_opposite_color(dest, (y, x + 1)):
            if not piece_on_edge((y, x + 1), ('x', 10)):
                if is_capture((y, x + 2), (y, x)):
                    captures.append((y, x + 1))
    # left
    if x != 0:
        if is_opposite_color(dest, (y, x - 1)):
            if not piece_on_edge((y, x - 1), ('x', 0)):
                if is_capture((y, x - 2), (y, x)):
                    captures.append((y, x - 1))
    for capture in captures:
        y, x = capture
        GRID[y][x] = 0
    return captures

def get_legal_moves(start):
    legal_moves = []
    # right
    y, x = start
    searching = True
    if piece_on_edge(start, ('x', 10)):
        searching = False
    y, x = start
    while searching:
        if GRID[y][x + 1] == 0:
            if x + 1 == 10:
                legal_moves.append((y, x + 1))
                break
            else:
                legal_moves.append((y, x + 1))
                x += 1
        else:
            searching = False
    # left
    searching = True
    if piece_on_edge(start, ('x', 0)):
        searching = False
    y, x = start
    while searching:
        if GRID[y][x - 1] == 0:
            if x - 1 == 0:
                legal_moves.append((y, x - 1))
                break
            else:
                legal_moves.append((y, x - 1))
                x -= 1
        else:
            searching = False
    # up
    searching = True
    if piece_on_edge(start, ('y', 0)):
        searching = False
    y, x = start
    while searching:
        if GRID[y - 1][x] == 0:
            if y - 1 == 0:
                legal_moves.append((y - 1, x))
                break
            else:
                legal_moves.append((y - 1, x))
                y -= 1
        else:
            searching = False
    # down
    searching = True
    if piece_on_edge(start, ('y', 10)):
        searching = False
    y, x = start
    while searching:
        if GRID[y + 1][x] == 0:
            if y + 1 == 10:
                legal_moves.append((y + 1, x))
                break
            else:    
                legal_moves.append((y + 1, x))
                y += 1
        else:
            searching = False
    y, x = start
    if (0, 0) in legal_moves and not GRID[y][x] == 3:
        legal_moves.remove((0, 0))
    if (10, 0) in legal_moves and not GRID[y][x] == 3:
        legal_moves.remove((10, 0))
    if (0, 10) in legal_moves and not GRID[y][x] == 3:
        legal_moves.remove((0, 10))
    if (10, 10) in legal_moves and not GRID[y][x] == 3:
        legal_moves.remove((10, 10))
    return legal_moves

def check_winner():
    if GRID[0][0] == 3:
        return 'white'
    if GRID[10][0] == 3:
        return 'white'
    if GRID[0][10] == 3:
        return 'white'
    if GRID[10][10] == 3:
        return 'white'
    king = False
    for i in range(0, len(GRID)):
        for j in range(0, len(GRID)):
            if GRID[j][i] == 3:
                king = 'black'
    if not king:
        return 'black'
    return None

def reset():
    GRID = [
        [0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0],
        [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [1, 0, 0, 0, 0, 2, 0, 0, 0, 0, 1],
        [1, 0, 0, 0, 2, 2, 2, 0, 0, 0, 1],
        [1, 1, 0, 2, 2, 3, 2, 2, 0, 1, 1],
        [1, 0, 0, 0, 2, 2, 2, 0, 0, 0, 1],
        [1, 0, 0, 0, 0, 2, 0, 0, 0, 0, 1],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
        [0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0]
    ]
    MOVE = 'white'

home = True
barb = pygame.transform.smoothscale((pygame.image.load('viking.png')), (580/2, 757/2))
while home:
    DISPLAY.fill(WHITE)
    DISPLAY.blit(barb, (WIDTH/2 - barb.get_width()/2, HEIGHT/2 - barb.get_height()/2))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        if pygame.mouse.get_pressed()[0]:
            home = False
    CLOCK.tick(FPS)
    pygame.display.update()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        if not CLICKING and pygame.mouse.get_pressed()[0]:
            CLICKING = True
            START = mouse_to_coordinate(pygame.mouse.get_pos())
            y, x = START
            if GRID[y][x] == 0:
                CLICKING = False
                START = None
                continue
            if MOVE == 'white':
                y, x = START
                if GRID[y][x] == 1:
                    CLICKING = False
            if MOVE == 'black':
                y, x = START
                if GRID[y][x] == 2 or GRID[y][x] == 3:
                    CLICKING = False
        if CLICKING and not pygame.mouse.get_pressed()[0]:
            DEST = mouse_to_coordinate(pygame.mouse.get_pos())
            if START == DEST:
                CLICKING = False
                continue
            CLICKING = False
            if move(START, DEST):
                if MOVE == 'white':
                    MOVE = 'black'
                else:
                    MOVE = 'white'
                START = None
            check_captures(DEST)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                reset()

    DISPLAY.fill(WHITE)
    color_squares()
    draw_grid()
    draw_pieces()
    win(check_winner())
    pygame.display.update()
    CLOCK.tick(FPS)