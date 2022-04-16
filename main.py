import numpy as np
import pygame
import sys
import math
from pygame import mixer


# global variable
BLUE = (30, 38, 230, 90)
WHITE = (219, 219, 213, 86)
BLACK = (0, 0, 0, 0)
RED = (255, 37, 32, 100)
YELLOW = (255, 206, 43, 88)
# board size can be changed easily from here
ROW_COUNT = 6
COLUMN_COUNT = 7

mixer.init()


def create_board():
    # board of zeros with 6 rows and 7 columns
    board = np.zeros((ROW_COUNT, COLUMN_COUNT))
    return board


def drop_piece(board, row, col, piece):
    board[row][col] = piece


def is_valid_location(board, col):
    # checking if the column has an empty slot
    # ROW_COUNT-1 is the last row
    return board[ROW_COUNT-1][col] == 0


def get_next_open_row(board, col):
    # check next row available in that column
    for r in range(ROW_COUNT):
        if board[r][col] == 0:
            return r


# changing orientation due to numpy index order
# so drops start at the bottom of the column and not at the top
def print_board(board):
    print(np.flip(board, 0))


def winning_move(board, piece):
    # Check horizontal locations
    for c in range(COLUMN_COUNT-3):
        for r in range(ROW_COUNT):
            if board[r][c] == piece and board[r][c+1] == piece and board[r][c+2] == piece and board[r][c+3] == piece:
                return True

    # Check vertical locations
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT-3):
            if board[r][c] == piece and board[r+1][c] == piece and board[r+2][c] == piece and board[r+3][c] == piece:
                return True

    # Check positively sloped diagonals
    for c in range(COLUMN_COUNT-3):
        for r in range(ROW_COUNT-3):
            if board[r][c] == piece and board[r+1][c+1] == piece and \
                    board[r+2][c+2] == piece and board[r+3][c+3] == piece:
                return True

    # Check negatively sloped diagonals
    for c in range(COLUMN_COUNT-3):
        for r in range(3, ROW_COUNT):
            if board[r][c] == piece and board[r-1][c+1] == piece \
                    and board[r-2][c+2] == piece and board[r-3][c+3] == piece:
                return True


# draw board with pygame graphics
def draw_board(board):
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            # .rect(Surface, color, Rect(x, y, w, h), width=0)
            # adding a square_size to rect*square_size to shift empty black row to the top
            pygame.draw.rect(screen, BLUE, (c*SQUARE_SIZE, r*SQUARE_SIZE+SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
            pygame.draw.circle(screen, WHITE, (int(c*SQUARE_SIZE+SQUARE_SIZE/2),
                                               int(r*SQUARE_SIZE+SQUARE_SIZE+SQUARE_SIZE/2)), RADIUS)
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            if board[r][c] == 1:
                pygame.draw.circle(screen, RED, (int(c * SQUARE_SIZE + SQUARE_SIZE / 2),
                                                 height-int(r * SQUARE_SIZE + SQUARE_SIZE / 2)), RADIUS)
            elif board[r][c] == 2:
                pygame.draw.circle(screen, YELLOW, (int(c * SQUARE_SIZE + SQUARE_SIZE / 2),
                                                    height-int(r * SQUARE_SIZE + SQUARE_SIZE / 2)), RADIUS)
    # to update the screen after every change
    pygame.display.update()


board = create_board()

print_board(board)

game_over = False
# to identify player turn
turn = 0

pygame.init()

# which is the size of each circle on the board
SQUARE_SIZE = 100

width = COLUMN_COUNT * SQUARE_SIZE
height = (ROW_COUNT+1) * SQUARE_SIZE

# tuple
size = (width, height)

RADIUS = int(SQUARE_SIZE/2 - 5)

# to make pygame read it
screen = pygame.display.set_mode(size)
draw_board(board)
pygame.display.update()

FONT = pygame.font.SysFont('ocr a extended', 80)

# loop to keep running until someone has a four in a row
while not game_over:

    # if x button clicked then exit window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.MOUSEMOTION:
            pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARE_SIZE))
            # adding these conditions draws stretches of circle. Need to delete previous circles
            # with above code
            pos_x = event.pos[0]
            if turn == 0:
                pygame.draw.circle(screen, RED, (pos_x, int(SQUARE_SIZE/2)), RADIUS)
            else:
                pygame.draw.circle(screen, YELLOW, (pos_x, int(SQUARE_SIZE/2)), RADIUS)
        pygame.display.update()

        # tracking MOUSEBUTTONDOWN event
        if event.type == pygame.MOUSEBUTTONDOWN:
            pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARE_SIZE))
            mixer.music.load('pop_sound.wav')
            mixer.music.play()
            # Ask for Player 1 input
            if turn == 0:
                pos_x = event.pos[0]
                # floor to get whole number, int to get int value, values up to 7
                col = int(math.floor(pos_x/SQUARE_SIZE))
                # int(input('Player 1 Make your selection (0-6):'))

                if is_valid_location(board, col):
                    row = get_next_open_row(board, col)
                    drop_piece(board, row, col, 1)

                    if winning_move(board, 1):
                        label = FONT.render("Player 1 Wins!!! Yippee", 1, RED)
                        mixer.music.load('victory_sound.wav')
                        mixer.music.play()
                        screen.blit(label, (40, 10))
                        print("Player 1 Wins! Congrats!")
                        game_over = True

            # Ask for Player 2 input
            else:
                pos_x = event.pos[0]
                col = int(math.floor(pos_x/SQUARE_SIZE))

                if is_valid_location(board, col):
                    row = get_next_open_row(board, col)
                    drop_piece(board, row, col, 2)

                    if winning_move(board, 2):
                        label = FONT.render("Player 2 Wins!!! Yippee", 1, YELLOW)
                        mixer.music.load('victory_sound.wav')
                        mixer.music.play()
                        screen.blit(label, (40, 10))
                        print("Player 2 Wins! Congrats!")
                        game_over = True

            print_board(board)
            draw_board(board)

            turn += 1
            # mod with two to get remainder 0 so that turns alternate between 0 and 1
            turn = turn % 2

            if game_over:
                pygame.time.wait(4000)


