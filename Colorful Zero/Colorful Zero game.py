import numpy as np
import myCreateImages
import cmpt120image


def welcome():
    """
    print initial messages to user
    """
    print('\n')
    print('Dear player! Welcome to the "Colourful Zero" game ')
    print('-------------------------------------------------\n')


def pretty_print_board(title, list2D):
    """
    receives a 2D list of lists of numbers and prints it in a tidy
    format with general title, column and row subtitles.
    You may want to adapt to also print the sum-col and sum-row
    and their titles
    """

    print('\n')
    print(title)
    print('--------------\n')

    # Calling function to store sum of rows and cols
    sum_row = np.array(calc_sumrow(list2D))
    sum_col = np.array(calc_sumcol(list2D))

    # printing 2d matrix in a pretty way
    for i in range(len(list2D)):
        for j in range(len(list2D)):
            print('{:4}'.format(list2D[i][j]), end=' ')
        print('{:4}'.format(sum_row[i]), end=' ')
        print('')

    for i in range(len(list2D)):
        print('{:4}'.format(sum_col[i]), end=' ')
    print('')


def create_initial_board(boardID):
    """
    given a boardID (1 to 5)
    reads from a file boardX.csv,
    where X is the BoardID
    and creates and returns a structure (list of lists)
    representing the board
    """
    listarr = []

    # reading csv file according to the board id
    csv_file = 'board' + str(boardID) + '.csv'
    with open(csv_file, mode='r') as file:
        first_line = file.readline()
        file_contents = file.readlines()

        # reading contents of a file and converting them into a list
        for lines in file_contents:
            listres = list(lines.split(','))
            listres[-1] = listres[-1].strip()
            listres = list(map(int, listres))
            listarr.append(listres)

    return listarr


def is_int(st):
    """
    given a string, determine whether it can be converted to an integer
    with the int() function.

    Note: a string can be converted to an integer with int() if and only if
    it is all digits (can be checked with st.isdigit()), or if it begins with
    the '-' character and all remaining characters are digits.

    Can be used for input validation.

    Example: is_int("-4") would return True
    """
    try:
        num = int(st)
        if type(num) == int:
            if 1 <= num < 6:
                return True
            else:
                return False

    except:
        return False


def calc_sumrow(board):
    """
    returns a list (row) where each element is the sum of all
    the corresponding values in the cols in the board
     1 2 3
     4 5 6
     1 1 1
     6 8 10 <---

     (i.e. returns the list [6,8,10])
    """
    boardnp = np.array(board)
    return boardnp.sum(axis=1)


def calc_sumcol(board):
    """
    returns a list (colum) where each element is the sum of all
    the corresponding values in the rows in the board
     1 2 3  6
     4 5 6  15
     1 1 1  3
            ^

    (i.e. returns the list [6,15,3])
    """
    boardnp = np.array(board)
    return boardnp.sum(axis=0)


def all_zero(lst):
    """
    determine whether all items in a list of numbers are 0

    Example: all_zero([0,0,0,0]) would return True
    """

    sum_row = np.array(calc_sumrow(lst))
    sum_col = np.array(calc_sumcol(lst))

    # checking if sum of all rows and cols is zero
    if all(v == 0 for v in sum_row) and all(v == 0 for v in sum_col):
        return True
    else:
        return False


def check_points(board):
    """ Function to check if there is any zero in sum of
    rows and cols and add points accordingly """

    count = 0
    sum_row = np.array(calc_sumrow(board))
    sum_col = np.array(calc_sumcol(board))
    for i in sum_row:
        if i == 0:
            count += 1

    for i in sum_col:
        if i == 0:
            count += 1

    return count


# def fill_square(x, y, img, colour):
#     """
#     fills a 100x100 pixel square starting at img[x][y] with
#     the RGB colour given as a parameter
#
#     Example: fill_square(0,0,img,[255,0,0]) would set the
#     upper left 100x100 pixel square of img to the colour red
#     """
#     pass


# ------------------Game Variables--------------------
game = False
board_id = 0
game_points = 0
no_of_games = 1
games_won = 0
row_input = 0
col_input = 0
value = 0
check1 = False
check2 = False
game_list = []
no_of_boards = 0

welcome()

# loop will run until the user decides to leave the game
while True:

    # loop for checking if the user has entered the correct input to start the game
    while True:
        game_check = input('Would  you like to play? (y/n): ')
        if game_check == 'y':
            # loop for checking if the user has entered the correct board id
            while True:
                board_id = input("Enter Board Id: ")
                if is_int(board_id):
                    game = True
                    break
                else:
                    print('That is not a valid value, please re-enter')
            break
        elif game_check == 'n':
            check1 = True
            break
        else:
            print('That is not a valid value, please re-enter')

    if check1:
        break

    # logic of No of turns
    board_id = int(board_id)
    no_of_turns = int(board_id * board_id / 2)

    # print board game
    game_list = create_initial_board(board_id)
    no_of_boards += 1

    print('\n')
    print(f'Game Number: {no_of_games}')
    print('---------------')
    print('---------------')

    no_of_games += 1

    # loop to start a new game whenever the no of turns run out
    while no_of_turns != 0:
        pretty_print_board('The Board is ', game_list)

        row_sum = calc_sumcol(game_list)

        print(f'Turns Left: {no_of_turns}')
        print('User, where do you want your value? (row 99 if you want no more turns)')

        # loop for checking if the user has entered correct row number
        while True:
            try:
                row_input = int(input(f'row?  (>= 0 and <= {len(game_list) - 1}): '))
                if row_input == 99:
                    print('\n')
                    print("Since you didn't want to update more digits,the game is over")
                    print('So sorry, User, you lost this game!')
                    print(f'But you still got points!: {game_points}')
                    check2 = True
                    print('\n')
                    break
                elif 0 <= row_input <= len(game_list) - 1:
                    break
                else:
                    print('That is not a valid value, please re-enter')
            except:
                print('That is not a valid value, please re-enter')

        if check2:
            break

        # loop for checking if the user has entered correct col number
        while True:
            try:
                col_input = int(input(f'col?  (>= 0 and <= {len(game_list) - 1}): '))
                if 0 <= col_input <= len(game_list) - 1:
                    break
                else:
                    print('That is not a valid value, please re-enter')
            except:
                print('That is not a valid value, please re-enter')

        # loop for checking if the user has entered correct value
        while True:
            try:
                value = int(input('value (>= -9 and <= 9): '))
                if -9 <= value <= 9:
                    break
                else:
                    print('That is not a valid value, please re-enter')
            except:
                print('That is not a valid value, please re-enter')

        no_of_turns -= 1

        # updating the value
        game_list[row_input][col_input] = value

        # updating points accordingly
        game_points += check_points(game_list)

        # checking if the user has won or not
        if all_zero(game_list):
            print('\n')
            games_won += 1
            print('You Won')
            game_points += 10
            print('Yey! Congratulations again, user, you won this game! ')
            print(f'You got  {game_points} points!')
            print('\n')
            break

        #  logic of, if no of turns ran out
        if no_of_turns == 0:
            pretty_print_board('The Board is ', game_list)
            print('\n')
            print('So sorry, User, you lost this game!')
            print(f'But you still got points!: {game_points}')
            print('\n')
            break

print('\n')
print("TOTALS ALL GAMES")
print(f'Total points user in all games: {game_points}')
print(f'Total games the user won: {games_won}')
print('\n')
print('Bye!!')
print('\n')

colordict = myCreateImages.read_color_coding()
colordict3d = myCreateImages.list_3d_color(colordict, game_list)

cmpt120image.showImage(colordict3d)
cmpt120image.saveImage(colordict3d, f'boardImage{no_of_boards}-{no_of_games}.jpg')

