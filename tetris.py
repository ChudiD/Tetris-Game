import pygame
import random
import os

# Initialize Pygame and the mixer module
pygame.init()
pygame.mixer.init()

# Screen dimensions
s_width = 800
s_height = 750  # Increased height to accommodate the text and play area
play_width = 300  # Play area width (10 blocks wide)
play_height = 600  # Play area height (20 blocks high)
block_size = 30

top_left_x = (s_width - play_width) // 2
top_left_y = 150  # Adjusted to move the play area down

# Shapes (7 Tetrominoes)
S = [['.....',
      '.....',
      '..00.',
      '.00..',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '...0.',
      '.....']]

Z = [['.....',
      '.....',
      '.00..',
      '..00.',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '.0...',
      '.....']]

I = [['..0..',
      '..0..',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '0000.',
      '.....',
      '.....',
      '.....']]

O = [['.....',
      '.....',
      '.00..',
      '.00..',
      '.....']]

J = [['.....',
      '.0...',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..00.',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '...0.',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '.00..',
      '.....']]

L = [['.....',
      '...0.',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '..00.',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '.0...',
      '.....'],
     ['.....',
      '.00..',
      '..0..',
      '..0..',
      '.....']]

T = [['.....',
      '..0..',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '..0..',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '..0..',
      '.....']]

shapes = [S, Z, I, O, J, L, T]
shape_colors = [
    (57, 255, 20),    # S - Neon Green
    (255, 0, 0),      # Z - Neon Red
    (0, 255, 255),    # I - Neon Cyan
    (255, 255, 0),    # O - Neon Yellow
    (255, 165, 0),    # J - Neon Orange
    (77, 77, 255),    # L - Neon Blue
    (148, 0, 211)     # T - Neon Purple
]

class Piece(object):
    def __init__(self, x, y, shape):
        self.x = x
        self.y = y
        self.shape = shape
        self.color = shape_colors[shapes.index(shape)]
        self.rotation = 0

def create_grid(locked_positions={}):
    grid = [[(0,0,0) for _ in range(10)] for _ in range(20)]
    for y in range(len(grid)):
        for x in range(len(grid[y])):
            if (x, y) in locked_positions:
                grid[y][x] = locked_positions[(x, y)]
    return grid

def convert_shape_format(piece):
    positions = []
    format = piece.shape[piece.rotation % len(piece.shape)]
    for i, line in enumerate(format):
        row = list(line)
        for j, column in enumerate(row):
            if column == '0':
                positions.append((piece.x + j - 2, piece.y + i - 4))
    return positions

def valid_space(piece, grid):
    accepted_pos = [[(x, y) for x in range(10)
                     if grid[y][x] == (0,0,0)] for y in range(20)]
    accepted_pos = [x for sublist in accepted_pos for x in sublist]
    formatted = convert_shape_format(piece)
    for pos in formatted:
        if pos not in accepted_pos and pos[1] > -1:
            return False
    return True

def check_lost(positions):
    for pos in positions:
        x, y = pos
        if y < 1:
            return True
    return False

def get_shape():
    return Piece(5, 0, random.choice(shapes))

def draw_text_middle(surface, text, size, color, position):
    font = pygame.font.SysFont('comicsans', size, bold=True)
    label = font.render(text, 1, color)
    surface.blit(label, (s_width / 2 - label.get_width() / 2,
                         position))

def draw_grid(surface, grid):
    for y in range(len(grid)):
        pygame.draw.line(surface, (128,128,128),
                         (top_left_x, top_left_y + y * block_size),
                         (top_left_x + play_width, top_left_y + y * block_size))
        for x in range(len(grid[y])):
            pygame.draw.line(surface, (128,128,128),
                             (top_left_x + x * block_size, top_left_y),
                             (top_left_x + x * block_size, top_left_y + play_height))

def clear_rows(grid, locked):
    increment = 0
    for y in range(len(grid)-1, -1, -1):
        if (0,0,0) not in grid[y]:
            increment += 1
            ind = y
            for x in range(len(grid[y])):
                try:
                    del locked[(x, y)]
                except:
                    continue
    if increment > 0:
        # Shift every row above down
        for key in sorted(list(locked), key=lambda x: x[1])[::-1]:
            x, y = key
            if y < ind:
                newKey = (x, y + increment)
                locked[newKey] = locked.pop(key)
    return increment

def draw_next_shapes(surface, shapes):
    font = pygame.font.SysFont('comicsans', 30)
    label = font.render('Next Shapes', 1, (255,255,255))

    sx = top_left_x + play_width + 50
    sy = top_left_y + play_height/2 - 100

    surface.blit(label, (sx + 10, sy - 30))

    for i, shape in enumerate(shapes):
        format = shape.shape[shape.rotation % len(shape.shape)]

        for y, line in enumerate(format):
            row = list(line)
            for x, column in enumerate(row):
                if column == '0':
                    pygame.draw.rect(surface, shape.color,
                                     (sx + x * block_size,
                                      sy + y * block_size + i * 100,
                                      block_size, block_size), 0)
                    # Outline
                    pygame.draw.rect(surface, (255, 255, 255),
                                     (sx + x * block_size,
                                      sy + y * block_size + i * 100,
                                      block_size, block_size), 2)
        # Label the shapes with numbers 1, 2, 4
        label_num = font.render(str([1,2,3][i%3]), 1, (255,255,255))
        surface.blit(label_num, (sx - 30, sy + i * 100 + 20))

def draw_window(surface, grid, score=0, level=0, lines=0):
    surface.fill((0,0,0))
    font = pygame.font.SysFont('comicsans', 60)
    label = font.render('Tetris', 1, (255,255,255))
    surface.blit(label, (s_width / 2 - label.get_width() / 2, 30))

    # Display the new message
    small_font = pygame.font.SysFont('comicsans', 30)
    label2 = small_font.render('LAST UNTIL THE END OF THE SONG', 1, (255, 255, 255))
    surface.blit(label2, (s_width / 2 - label2.get_width() / 2, 100))

    # Draw current score
    font = pygame.font.SysFont('comicsans', 30)
    sx = top_left_x - 200
    sy = top_left_y + 100
    score_label = font.render(f'Score: {score}', 1, (255,255,255))
    level_label = font.render(f'Level: {level}', 1, (255,255,255))
    lines_label = font.render(f'Lines: {lines}', 1, (255,255,255))

    surface.blit(score_label, (sx, sy))
    surface.blit(level_label, (sx, sy + 30))
    surface.blit(lines_label, (sx, sy + 60))

    for y in range(len(grid)):
        for x in range(len(grid[y])):
            if grid[y][x] != (0,0,0):
                color = grid[y][x]
                # Draw the block
                pygame.draw.rect(surface, color,
                                 (top_left_x + x * block_size,
                                  top_left_y + y * block_size,
                                  block_size, block_size), 0)
                # Draw the outline to simulate glow
                pygame.draw.rect(surface, (255, 255, 255),
                                 (top_left_x + x * block_size,
                                  top_left_y + y * block_size,
                                  block_size, block_size), 2)
    draw_grid(surface, grid)
    pygame.draw.rect(surface, (255, 0, 0),
                     (top_left_x, top_left_y, play_width, play_height), 5)

def main():
    global grid
    pygame.mixer.music.play()  # Restart the music when a new game starts
    locked_positions = {}
    grid = create_grid(locked_positions)
    change_piece = False
    run = True
    paused = False  # Variable to track if the game is paused
    current_piece = get_shape()
    next_pieces = [get_shape() for _ in range(3)]  # Next few pieces
    clock = pygame.time.Clock()
    fall_time = 0
    fall_speed = 0.27
    level_time = 0
    score = 0
    level = 0
    lines_cleared = 0

    while run:
        if not paused:
            grid = create_grid(locked_positions)
            fall_time += clock.get_rawtime()
            clock.tick()
            # Increase difficulty over time
            level_time += clock.get_rawtime()
            if level_time / 1000 > 5:
                level_time = 0
                if fall_speed > 0.12:
                    fall_speed -= 0.005
            if fall_time / 1000 >= fall_speed:
                fall_time = 0
                current_piece.y += 1
                if not(valid_space(current_piece, grid)) and current_piece.y > 0:
                    current_piece.y -= 1
                    change_piece = True
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    pygame.mixer.music.stop()  # Stop the music when quitting
                    pygame.display.quit()
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:
                        paused = True
                    if event.key == pygame.K_LEFT:
                        current_piece.x -= 1
                        if not(valid_space(current_piece, grid)):
                            current_piece.x += 1
                    if event.key == pygame.K_RIGHT:
                        current_piece.x += 1
                        if not(valid_space(current_piece, grid)):
                            current_piece.x -= 1
                    if event.key == pygame.K_DOWN:
                        current_piece.y += 1
                        if not(valid_space(current_piece, grid)):
                            current_piece.y -= 1
                    if event.key == pygame.K_UP:
                        current_piece.rotation += 1
                        if not(valid_space(current_piece, grid)):
                            current_piece.rotation -= 1
            shape_pos = convert_shape_format(current_piece)
            for x, y in shape_pos:
                if y > -1:
                    grid[y][x] = current_piece.color
            if change_piece:
                for pos in shape_pos:
                    locked_positions[(pos[0], pos[1])] = current_piece.color
                current_piece = next_pieces.pop(0)
                next_pieces.append(get_shape())
                change_piece = False
                cleared = clear_rows(grid, locked_positions)
                if cleared > 0:
                    lines_cleared += cleared
                    score += cleared * 10
                    if lines_cleared % 10 == 0:
                        level += 1
            draw_window(win, grid, score, level, lines_cleared)
            draw_next_shapes(win, next_pieces)
            pygame.display.update()
            if check_lost(locked_positions):
                draw_text_middle(win, "You Lost!", 80, (255,255,255), s_height/2 - 40)
                pygame.display.update()
                pygame.time.delay(2000)
                pygame.mixer.music.stop()  # Stop the music when game over
                run = False
        else:
            # Game is paused
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    pygame.mixer.music.stop()
                    pygame.display.quit()
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:
                        paused = False
            draw_text_middle(win, "Paused", 80, (255,255,255), s_height/2 - 40)
            pygame.display.update()
            clock.tick(5)  # Limit the loop to reduce CPU usage when paused

def main_menu():
    global win
    win = pygame.display.set_mode((s_width, s_height))
    pygame.display.set_caption('Tetris')

    # Load the background music
    pygame.mixer.music.load(r'c:\Users\Chudi Duru\Downloads\Playboi Carti- Bouldercrest (Piru) [feat. Offset].mp3')
    pygame.mixer.music.set_volume(0.5)  # Adjust the volume as needed (0.0 to 1.0)

    run = True
    while run:
        win.fill((0,0,0))
        draw_text_middle(win, 'Press Any Key To Play', 60, (255,255,255), s_height/2 - 40)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.mixer.music.stop()  # Stop the music when quitting
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                main()
    pygame.quit()

if __name__ == '__main__':
    main_menu()
def game_over_screen():
    global win
    game_over = True
    while game_over:
        win.fill((0, 0, 0))
        draw_text_middle(win, "You Lost!", 80, (255, 255, 255), s_height / 2 - 80)
        draw_text_middle(win, "Press R to Restart or Q to Quit", 40, (255, 255, 255), s_height / 2)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = False
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    main()
                    game_over = False
                elif event.key == pygame.K_q:
                    game_over = False
                    pygame.quit()
                    quit()

def game_over_screen():
    global win, run
    game_over = True
    while game_over:
        win.fill((0, 0, 0))
        draw_text_middle(win, "You Lost!", 80, (255, 255, 255), s_height / 2 - 80)
        draw_text_middle(win, "Press R to Restart or Q to Quit", 40, (255, 255, 255), s_height / 2)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = False
                run = False
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    game_over = False  # Exit game over screen to restart
                elif event.key == pygame.K_q:
                    game_over = False
                    run = False
                    pygame.quit()
                    quit()

def main():
    global grid, run
    run = True
    while run:
        pygame.mixer.music.play()  # Restart the music when a new game starts
        locked_positions = {}
        grid = create_grid(locked_positions)
        change_piece = False
        paused = False  # Variable to track if the game is paused
        current_piece = get_shape()
        next_pieces = [get_shape() for _ in range(3)]  # Next few pieces
        clock = pygame.time.Clock()
        fall_time = 0
        fall_speed = 0.27
        level_time = 0
        score = 0
        level = 0
        lines_cleared = 0
        game_over = False  # Flag to control the game loop

        while not game_over:
            if not paused:
                grid = create_grid(locked_positions)
                fall_time += clock.get_rawtime()
                clock.tick()
                # Increase difficulty over time
                level_time += clock.get_rawtime()
                if level_time / 1000 > 5:
                    level_time = 0
                    if fall_speed > 0.12:
                        fall_speed -= 0.005
                if fall_time / 1000 >= fall_speed:
                    fall_time = 0
                    current_piece.y += 1
                    if not(valid_space(current_piece, grid)) and current_piece.y > 0:
                        current_piece.y -= 1
                        change_piece = True
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        game_over = True
                        run = False
                        pygame.mixer.music.stop()  # Stop the music when quitting
                        pygame.display.quit()
                        pygame.quit()
                        quit()
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_p:
                            paused = True
                        if event.key == pygame.K_LEFT:
                            current_piece.x -= 1
                            if not(valid_space(current_piece, grid)):
                                current_piece.x += 1
                        if event.key == pygame.K_RIGHT:
                            current_piece.x += 1
                            if not(valid_space(current_piece, grid)):
                                current_piece.x -= 1
                        if event.key == pygame.K_DOWN:
                            current_piece.y += 1
                            if not(valid_space(current_piece, grid)):
                                current_piece.y -= 1
                        if event.key == pygame.K_UP:
                            current_piece.rotation += 1
                            if not(valid_space(current_piece, grid)):
                                current_piece.rotation -= 1
                shape_pos = convert_shape_format(current_piece)
                for x, y in shape_pos:
                    if y > -1:
                        grid[y][x] = current_piece.color
                if change_piece:
                    for pos in shape_pos:
                        locked_positions[(pos[0], pos[1])] = current_piece.color
                    current_piece = next_pieces.pop(0)
                    next_pieces.append(get_shape())
                    change_piece = False
                    cleared = clear_rows(grid, locked_positions)
                    if cleared > 0:
                        lines_cleared += cleared
                        score += cleared * 10
                        if lines_cleared % 10 == 0:
                            level += 1
                draw_window(win, grid, score, level, lines_cleared)
                draw_next_shapes(win, next_pieces)
                pygame.display.update()
                if check_lost(locked_positions):
                    pygame.mixer.music.stop()  # Stop the music when game over
                    game_over_screen()
                    game_over = True  # Exit the inner game loop
            else:
                # Game is paused
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        game_over = True
                        run = False
                        pygame.mixer.music.stop()
                        pygame.display.quit()
                        pygame.quit()
                        quit()
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_p:
                            paused = False
                draw_text_middle(win, "Paused", 80, (255,255,255), s_height/2 - 40)
                pygame.display.update()
                clock.tick(5)  # Limit the loop to reduce CPU usage when paused
