import time
import numpy as np
import random
import pygame
import sys
import math
import button


# Global variables
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)


ROW_COUNT = 6
COLUMN_COUNT = 7

screen_width = 600
screen_height = 700

game_menu = 'game menu'

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Connect 4')


def draw_text(text, font, text_col,  x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))


PLAYER = 0
AI = 1

EMPTY = 0
PLAYER_PIECE = 1
AI_PIECE = 2

WINDOW_LENGTH = 5


def create_board():
    board = np.zeros((ROW_COUNT, COLUMN_COUNT))
    return board


def drop_piece(board, row, col, piece):
    board[row][col] = piece


def is_valid_location(board, col):
    return board[ROW_COUNT - 1][col] == 0


def get_next_open_row(board, col):
    for r in range(ROW_COUNT):
        if board[r][col] == 0:
            return r


def print_board(board):
    print(np.flip(board, 0))


def winning_move(board, piece):
    # Check horizontal locations for win
    for c in range(COLUMN_COUNT - (WINDOW_LENGTH - 1)):
        for r in range(ROW_COUNT):
            if board[r][c] == piece and board[r][c + 1] == piece and board[r][c + 2] == piece and board[r][c + 3] == piece:
                return True

    # Check vertical locations for win
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT - (WINDOW_LENGTH - 1)):
            if board[r][c] == piece and board[r + 1][c] == piece and board[r + 2][c] == piece and board[r + 3][c] == piece:
                return True

    # Check positively sloped diagonals
    for c in range(COLUMN_COUNT - (WINDOW_LENGTH - 1)):
        for r in range(ROW_COUNT - (WINDOW_LENGTH - 1)):
            if board[r][c] == piece and board[r + 1][c + 1] == piece and board[r + 2][c + 2] == piece and board[r + 3][c + 3] == piece:
                return True

    # Check negatively sloped diagonals
    for c in range(COLUMN_COUNT - (WINDOW_LENGTH - 1)):
        for r in range(WINDOW_LENGTH - 1, ROW_COUNT):
            if board[r][c] == piece and board[r - 1][c + 1] == piece and board[r - 2][c + 2] == piece and board[r - 3][c + 3] == piece:
                return True


def evaluate_window(window, piece):
    score = 0
    opp_piece = PLAYER_PIECE
    if piece == PLAYER_PIECE:
        opp_piece = AI_PIECE

    if window.count(piece) == 4:
        score += 100
    elif window.count(piece) == 3 and window.count(EMPTY) == 1:
        score += 5
    elif window.count(piece) == 2 and window.count(EMPTY) == 2:
        score += 2

    if window.count(opp_piece) == 3 and window.count(EMPTY) == 1:
        score -= 4

    return score


def score_position(board, piece):
    score = 0

    # Score center column
    center_array = [int(i) for i in list(board[:, COLUMN_COUNT // 2])]
    center_count = center_array.count(piece)
    score += center_count * 3

    # Score Horizontal
    for r in range(ROW_COUNT):
        row_array = [int(i) for i in list(board[r, :])]
        for c in range(COLUMN_COUNT - (WINDOW_LENGTH - 1)):
            window = row_array[c:c + WINDOW_LENGTH]
            score += evaluate_window(window, piece)

    # Score Vertical
    for c in range(COLUMN_COUNT):
        col_array = [int(i) for i in list(board[:, c])]
        for r in range(ROW_COUNT - (WINDOW_LENGTH - 1)):
            window = col_array[r:r + WINDOW_LENGTH]
            score += evaluate_window(window, piece)

    # Score posiive sloped diagonal
    for r in range(ROW_COUNT - (WINDOW_LENGTH - 1)):
        for c in range(COLUMN_COUNT - (WINDOW_LENGTH - 1)):
            window = [board[r + i][c + i] for i in range(WINDOW_LENGTH)]
            score += evaluate_window(window, piece)

    # Score negative sloped diagonal
    for r in range(ROW_COUNT - (WINDOW_LENGTH - 1)):
        for c in range(COLUMN_COUNT - (WINDOW_LENGTH - 1)):
            window = [board[r + 3 - i][c + i] for i in range(WINDOW_LENGTH)]
            score += evaluate_window(window, piece)

    return score


def is_terminal_node(board):
    return winning_move(board, PLAYER_PIECE) or winning_move(board, AI_PIECE) or len(get_valid_locations(board)) == 0


def minimax(board, depth, alpha, beta, maximizingPlayer):
    valid_locations = get_valid_locations(board)
    is_terminal = is_terminal_node(board)
    if depth == 0 or is_terminal:
        if is_terminal:
            if winning_move(board, AI_PIECE):
                return (None, 100000000000000)
            elif winning_move(board, PLAYER_PIECE):
                return (None, -10000000000000)
            else:  # Game is over, no more valid moves
                return (None, 0)
        else:  # Depth is zero
            return (None, score_position(board, AI_PIECE))
    if maximizingPlayer:
        value = -math.inf
        column = random.choice(valid_locations)
        for col in valid_locations:
            row = get_next_open_row(board, col)
            b_copy = board.copy()
            drop_piece(b_copy, row, col, AI_PIECE)
            new_score = minimax(b_copy, depth - 1, alpha, beta, False)[1]
            if new_score > value:
                value = new_score
                column = col
            alpha = max(alpha, value)
            if alpha >= beta:
                break
        return column, value

    else:  # Minimizing player
        value = math.inf
        column = random.choice(valid_locations)
        for col in valid_locations:
            row = get_next_open_row(board, col)
            b_copy = board.copy()
            drop_piece(b_copy, row, col, PLAYER_PIECE)
            new_score = minimax(b_copy, depth - 1, alpha, beta, True)[1]
            if new_score < value:
                value = new_score
                column = col
            beta = min(beta, value)
            if alpha >= beta:
                break
        return column, value


def alphabeta(board, depth, alpha, beta, maximizingPlayer):
    valid_locations = get_valid_locations(board)
    is_terminal = is_terminal_node(board)
    if depth == 0 or is_terminal:
        if is_terminal:
            if winning_move(board, AI_PIECE):
                return (None, 100000000000000)
            elif winning_move(board, PLAYER_PIECE):
                return (None, -10000000000000)
            else:  # Game is over, no more valid moves
                return (None, 0)
        else:  # Depth is zero
            return (None, score_position(board, AI_PIECE))
    if maximizingPlayer:
        value = -math.inf
        column = random.choice(valid_locations)
        for col in valid_locations:
            row = get_next_open_row(board, col)
            b_copy = board.copy()
            drop_piece(b_copy, row, col, AI_PIECE)
            new_score = alphabeta(b_copy, depth - 1, alpha, beta, False)[1]
            if new_score > value:
                value = new_score
                column = col
            alpha = max(alpha, value)
            if alpha >= beta:
                break
        return column, value

    else:  # Minimizing player
        value = math.inf
        column = random.choice(valid_locations)
        for col in valid_locations:
            row = get_next_open_row(board, col)
            b_copy = board.copy()
            drop_piece(b_copy, row, col, PLAYER_PIECE)
            new_score = alphabeta(b_copy, depth - 1, alpha, beta, True)[1]
            if new_score < value:
                value = new_score
                column = col
            beta = min(beta, value)
            if alpha >= beta:
                break
        return column, value


def get_valid_locations(board):
    valid_locations = []
    for col in range(COLUMN_COUNT):
        if is_valid_location(board, col):
            valid_locations.append(col)
    return valid_locations


def pick_best_move(board, piece):
    valid_locations = get_valid_locations(board)
    best_score = -10000
    best_col = random.choice(valid_locations)
    for col in valid_locations:
        row = get_next_open_row(board, col)
        temp_board = board.copy()
        drop_piece(temp_board, row, col, piece)
        score = score_position(temp_board, piece)
        if score > best_score:
            best_score = score
            best_col = col

    return best_col


SQUARESIZE = 100
RADIUS = int(SQUARESIZE / 2 - 5)
height = 6


def draw_board(board):

    global SQUARESIZE, RADIUS, width, height

    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            pygame.draw.rect(screen, BLUE, (c * SQUARESIZE, r *
                             SQUARESIZE + SQUARESIZE, SQUARESIZE, SQUARESIZE))
            pygame.draw.circle(screen, BLACK, (
                int(c * SQUARESIZE + SQUARESIZE / 2), int(r * SQUARESIZE + SQUARESIZE + SQUARESIZE / 2)), RADIUS)

    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            if board[r][c] == 0:
                pygame.draw.circle(screen, BLACK, (
                    int(c * SQUARESIZE + SQUARESIZE / 2), height - int(r * SQUARESIZE + SQUARESIZE / 2)), RADIUS)
            elif board[r][c] == 1:
                pygame.draw.circle(screen, RED, (
                    int(c * SQUARESIZE + SQUARESIZE / 2), height - int(r * SQUARESIZE + SQUARESIZE / 2)), RADIUS)
            elif board[r][c] == 2:
                pygame.draw.circle(screen, YELLOW, (
                    int(c * SQUARESIZE + SQUARESIZE / 2), height - int(r * SQUARESIZE + SQUARESIZE / 2)), RADIUS)
    pygame.display.update()


# user can choose which algorithm to use
def choose_algorithm():
    print("Choose an algorithm to play with")
    print("1. Minimax")
    print("2. Alpha Beta Pruning")
    print("3. Quit")
    choice = input("Enter your choice: ")
    return choice


def play_game():

    global SQUARESIZE, RADIUS, width, height

    board = create_board()
    print_board(board)
    game_over = False

    turn = random.randint(PLAYER, AI)

    pygame.init()

    SQUARESIZE = 100

    width = COLUMN_COUNT * SQUARESIZE
    height = (ROW_COUNT + 1) * SQUARESIZE

    size = (width, height)

    RADIUS = int(SQUARESIZE / 2 - 5)

    screen = pygame.display.set_mode(size)
    draw_board(board)

    pygame.display.update()

    myfont = pygame.font.SysFont("monospace", 75)

    choice = choose_algorithm()

    # count the number of moves made by the AI and the player
    ai_moves = 0
    player_moves = 0

    while not game_over:
        # ask user which algorithm to use

        if choice == "1":
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

                if event.type == pygame.MOUSEMOTION:
                    pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARESIZE))
                    posx = event.pos[0]
                    if turn == PLAYER:
                        pygame.draw.circle(
                            screen, RED, (posx, int(SQUARESIZE/2)), RADIUS)

                pygame.display.update()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARESIZE))
                    # print(event.pos)
                    # Ask for Player 1 Input
                    if turn == PLAYER:
                        # remove previous label
                        pygame.draw.rect(
                            screen, BLACK, (0, 0, width, SQUARESIZE))

                        # show player 1 label
                        label = myfont.render("Player 1 Turn", 1, RED)
                        screen.blit(label, (40, 10))
                        posx = event.pos[0]
                        col = int(math.floor(posx/SQUARESIZE))

                        if is_valid_location(board, col):
                            # increment the number of moves made by the player
                            player_moves += 1

                            row = get_next_open_row(board, col)
                            drop_piece(board, row, col, PLAYER_PIECE)

                            if winning_move(board, PLAYER_PIECE):
                                # remove the label
                                pygame.draw.rect(
                                    screen, BLACK, (0, 0, width, SQUARESIZE))
                                label = myfont.render(
                                    "Player 1 wins!!", 1, RED)
                                screen.blit(label, (40, 10))
                                game_over = True

                            turn += 1
                            turn = turn % 2

                            print("Player moves: ", player_moves)

                            draw_board(board)

            # # Ask for Player 2 Input
            if turn == AI and not game_over:
                start = time.time()
                # remove previous label
                pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARESIZE))

                # show player 1 label
                label = myfont.render("AI Turn", 1, RED)
                screen.blit(label, (40, 10))

                # col = random.randint(0, COLUMN_COUNT-1)
                # col = pick_best_move(board, AI_PIECE)
                col, minimax_score = minimax(
                    board, 5, -math.inf, math.inf, True)

                if is_valid_location(board, col):
                    # pygame.time.wait(500)
                    row = get_next_open_row(board, col)
                    drop_piece(board, row, col, AI_PIECE)

                    if winning_move(board, AI_PIECE):
                        # increment the number of moves made by the AI
                        ai_moves += 1
                        # remove the label
                        pygame.draw.rect(
                            screen, BLACK, (0, 0, width, SQUARESIZE))
                        label = myfont.render("AI wins!!", 1, YELLOW)
                        screen.blit(label, (40, 10))
                        game_over = True

                    end = time.time()
                    print("AI took ", end - start, " seconds to make a move")
                    print("AI moves: ", ai_moves)

                    pygame.time.wait(5000)

                    draw_board(board)

                    turn += 1
                    turn = turn % 2

            if game_over:
                pygame.time.wait(3000)

        elif choice == "2":

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

                if event.type == pygame.MOUSEMOTION:
                    pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARESIZE))
                    posx = event.pos[0]
                    if turn == PLAYER:
                        pygame.draw.circle(
                            screen, RED, (posx, int(SQUARESIZE/2)), RADIUS)

                pygame.display.update()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARESIZE))
                    # print(event.pos)
                    # Ask for Player 1 Input
                    if turn == PLAYER:
                        # remove previous label
                        pygame.draw.rect(
                            screen, BLACK, (0, 0, width, SQUARESIZE))

                        # show player 1 label
                        label = myfont.render("Player 1", 1, RED)
                        screen.blit(label, (40, 10))

                        posx = event.pos[0]
                        col = int(math.floor(posx/SQUARESIZE))

                        if is_valid_location(board, col):
                            # increment the number of moves made by the player
                            player_moves += 1
                            row = get_next_open_row(board, col)
                            drop_piece(board, row, col, PLAYER_PIECE)

                            if winning_move(board, PLAYER_PIECE):
                                # remove the label
                                pygame.draw.rect(
                                    screen, BLACK, (0, 0, width, SQUARESIZE))

                                label = myfont.render(
                                    "Player 1 wins!!", 1, RED)
                                screen.blit(label, (40, 10))
                                game_over = True

                            turn += 1
                            turn = turn % 2

                            print("Player moves: ", player_moves)

                            draw_board(board)

            # # Ask for Player 2 Input
            if turn == AI and not game_over:
                # print how much time it takes to calculate the best move for AI
                start = time.time()

                # remove previous label
                pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARESIZE))

                # show player 1 label
                label = myfont.render("AI Turn", 1, RED)
                screen.blit(label, (40, 10))

                # col = random.randint(0, COLUMN_COUNT-1)
                # col = pick_best_move(board, AI_PIECE)
                col, minimax_score = alphabeta(
                    board, 5, -math.inf, math.inf, True)

                if is_valid_location(board, col):
                    # increment the number of moves made by the AI
                    ai_moves += 1
                    # pygame.time.wait(500)
                    row = get_next_open_row(board, col)
                    drop_piece(board, row, col, AI_PIECE)

                    if winning_move(board, AI_PIECE):

                        # remove the label
                        pygame.draw.rect(
                            screen, BLACK, (0, 0, width, SQUARESIZE))

                        label = myfont.render("AI wins!!", 1, YELLOW)
                        screen.blit(label, (40, 10))
                        game_over = True

                    end = time.time()
                    print("AI took ", end - start,
                          " seconds to calculate the best move")
                    print("AI moves: ", ai_moves)

                    turn += 1
                    turn = turn % 2

            if game_over:
                pygame.time.wait(3000)

        elif choice == "3":
            sys.exit()


def menu():
    global game_menu, screen_height, screen_width, bg

    # Load Button Images
    start_img = pygame.image.load('Start.png').convert_alpha()
    quit_img = pygame.image.load('quit.png').convert_alpha()

    # Create Button Instances
    start_button = button.Button(220, 250, start_img, 0.35)
    quit_button = button.Button(220, 350, quit_img, 1.25)

    run = True
    while run:

        # Draw the start button
        if game_menu == 'game menu':
            if start_button.draw(screen):
                game_menu = 'start'
            if quit_button.draw(screen):
                game_menu = 'quit'

        # Checks for Button Clicks (Which BUtton has been Clicked)
        if game_menu == 'start':
            play_game()
        if game_menu == 'quit':
            pygame.quit()

        # checking for a particular event during the game
        for event in pygame.event.get():
            # if the event is quit, then quit the game
            if event.type == pygame.QUIT:
                run = False

        pygame.display.update()

    pygame.quit()


if __name__ == '__main__':
    menu()
