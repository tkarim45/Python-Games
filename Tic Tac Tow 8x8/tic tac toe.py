# Tic Tac Toe Board
board = [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',
         ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',
         ' ', ' ', ' ', ' ', ' ', ' ']
# Player info
player = 1
player1_score = 0
player2_score = 0

# Win Flags
Win = 1
Draw = -1
Running = 0
End = 2

Game = Running
Mark = 'X'

# Check for Player Icon
flag1 = flag2 = False

# Corner Check Flag. If true then the player gets 2 points
corner_check_flag = False


# This is how the tic tac grid looks like and the players has to choose the cell no to mark it with his/her ICON
# 1  | 2  |  3  |  4  |  5  |  6  |  7
# --------------------------------------
# 8  | 9  | 10  | 11  | 12  | 13  | 14
# --------------------------------------
# 15 | 16 | 17  | 18  | 19  | 20  | 21
# --------------------------------------
# 22 | 23 | 24  | 25  | 26  | 27  | 28
# --------------------------------------
# 29 | 30 | 31  | 32  | 33  | 34  | 35
# --------------------------------------
# 36 | 37 | 38  | 39  | 40  | 41  | 42
# --------------------------------------
# 43 | 44 | 45  | 46  | 47  | 48  | 49


# This Function Draws Game Board
def draw_board():
    print(" %c | %c | %c | %c | %c | %c | %c" % (board[1], board[2], board[3], board[4], board[5], board[6], board[7]))
    print("___|___|___|___|___|___|___")
    print(" %c | %c | %c | %c | %c | %c | %c " % (
        board[8], board[9], board[10], board[11], board[12], board[13], board[14]))
    print("___|___|___|___|___|___|___")
    print(" %c | %c | %c | %c | %c | %c | %c " % (
        board[15], board[16], board[17], board[18], board[19], board[20], board[21]))
    print("___|___|___|___|___|___|___")
    print(" %c | %c | %c | %c | %c | %c | %c " % (
        board[22], board[23], board[24], board[25], board[26], board[27], board[28]))
    print("___|___|___|___|___|___|___")
    print(" %c | %c | %c | %c | %c | %c | %c " % (
        board[29], board[30], board[31], board[32], board[33], board[34], board[35]))
    print("___|___|___|___|___|___|___")
    print(" %c | %c | %c | %c | %c | %c | %c " % (
        board[36], board[37], board[38], board[39], board[40], board[41], board[42]))
    print("___|___|___|___|___|___|___")
    print(" %c | %c | %c | %c | %c | %c | %c " % (
        board[43], board[44], board[45], board[46], board[47], board[48], board[49]))
    print("   |   |   |   |   |   |   ")


# This Function Prints the Score Board
def print_scoreboard(p1, p2, p1_score, p2_score):
    print("\t--------------------------------")
    print("\t              SCOREBOARD       ")
    print("\t--------------------------------")
    print("\t   ", p1, "\t    ", p1_score)
    print("\t   ", p2, "\t    ", p2_score)
    print("\t--------------------------------\n")


# This Function Checks if the player has won or not
def check_win():
    global Game, corner_check_flag
    # Horizontal Check Row 1
    if board[1] == board[2] and board[2] == board[3] and board[3] == board[4] and board[1] != ' ':
        Game = Win
    elif board[2] == board[3] and board[3] == board[4] and board[4] == board[5] and board[2] != ' ':
        Game = Win
    elif board[3] == board[4] and board[4] == board[5] and board[5] == board[6] and board[3] != ' ':
        Game = Win
    elif board[4] == board[5] and board[5] == board[6] and board[6] == board[7] and board[4] != ' ':
        Game = Win

    # Horizontal Check Row 2
    elif board[8] == board[9] and board[9] == board[10] and board[10] == board[11] and board[8] != ' ':
        Game = Win
    elif board[9] == board[10] and board[10] == board[11] and board[11] == board[12] and board[9] != ' ':
        Game = Win
    elif board[10] == board[11] and board[11] == board[12] and board[12] == board[13] and board[10] != ' ':
        Game = Win
    elif board[11] == board[12] and board[12] == board[13] and board[13] == board[14] and board[11] != ' ':
        Game = Win

    # Horizontal Check Row 3
    elif board[15] == board[16] and board[16] == board[17] and board[17] == board[18] and board[15] != ' ':
        Game = Win
    elif board[16] == board[17] and board[17] == board[18] and board[18] == board[19] and board[16] != ' ':
        Game = Win
    elif board[17] == board[18] and board[18] == board[19] and board[19] == board[20] and board[17] != ' ':
        Game = Win
    elif board[18] == board[19] and board[19] == board[20] and board[20] == board[21] and board[18] != ' ':
        Game = Win

    # Horizontal Check Row 4
    elif board[22] == board[23] and board[23] == board[24] and board[24] == board[25] and board[22] != ' ':
        Game = Win
    elif board[23] == board[24] and board[24] == board[25] and board[25] == board[26] and board[23] != ' ':
        Game = Win
    elif board[24] == board[25] and board[25] == board[26] and board[26] == board[27] and board[24] != ' ':
        Game = Win
    elif board[25] == board[26] and board[26] == board[27] and board[27] == board[28] and board[25] != ' ':
        Game = Win

    # Horizontal Check Row 5
    elif board[29] == board[30] and board[30] == board[31] and board[31] == board[32] and board[29] != ' ':
        Game = Win
    elif board[30] == board[31] and board[31] == board[32] and board[32] == board[33] and board[30] != ' ':
        Game = Win
    elif board[31] == board[32] and board[32] == board[33] and board[33] == board[34] and board[31] != ' ':
        Game = Win
    elif board[32] == board[33] and board[33] == board[34] and board[34] == board[35] and board[32] != ' ':
        Game = Win

    # Horizontal Check Row 6
    elif board[36] == board[37] and board[37] == board[38] and board[38] == board[39] and board[36] != ' ':
        Game = Win
    elif board[37] == board[38] and board[38] == board[39] and board[39] == board[40] and board[37] != ' ':
        Game = Win
    elif board[38] == board[39] and board[39] == board[40] and board[40] == board[41] and board[38] != ' ':
        Game = Win
    elif board[39] == board[40] and board[40] == board[41] and board[41] == board[42] and board[39] != ' ':
        Game = Win

    # Horizontal Check Row 7
    elif board[43] == board[44] and board[44] == board[45] and board[45] == board[46] and board[43] != ' ':
        Game = Win
    elif board[44] == board[45] and board[45] == board[46] and board[46] == board[47] and board[44] != ' ':
        Game = Win
    elif board[45] == board[46] and board[46] == board[47] and board[47] == board[48] and board[45] != ' ':
        Game = Win
    elif board[46] == board[47] and board[47] == board[48] and board[48] == board[49] and board[46] != ' ':
        Game = Win

    # Vertical Check Column 1
    elif board[1] == board[8] and board[8] == board[15] and board[15] == board[22] and board[1] != ' ':
        Game = Win
    elif board[8] == board[15] and board[15] == board[22] and board[22] == board[29] and board[8] != ' ':
        Game = Win
    elif board[15] == board[22] and board[22] == board[29] and board[29] == board[36] and board[15] != ' ':
        Game = Win
    elif board[22] == board[29] and board[29] == board[36] and board[36] == board[43] and board[22] != ' ':
        Game = Win

    # Vertical Check Column 2
    elif board[2] == board[9] and board[9] == board[16] and board[16] == board[23] and board[2] != ' ':
        Game = Win
    elif board[9] == board[16] and board[16] == board[23] and board[23] == board[30] and board[9] != ' ':
        Game = Win
    elif board[16] == board[23] and board[23] == board[30] and board[30] == board[37] and board[16] != ' ':
        Game = Win
    elif board[23] == board[30] and board[30] == board[37] and board[37] == board[44] and board[23] != ' ':
        Game = Win

    # Vertical Check Column 3
    elif board[3] == board[10] and board[10] == board[17] and board[17] == board[24] and board[3] != ' ':
        Game = Win
    elif board[10] == board[17] and board[17] == board[24] and board[24] == board[31] and board[10] != ' ':
        Game = Win
    elif board[17] == board[24] and board[24] == board[31] and board[31] == board[38] and board[17] != ' ':
        Game = Win
    elif board[24] == board[31] and board[31] == board[38] and board[38] == board[45] and board[24] != ' ':
        Game = Win

    # Vertical Check Column 4
    elif board[4] == board[11] and board[11] == board[18] and board[18] == board[25] and board[4] != ' ':
        Game = Win
    elif board[11] == board[18] and board[18] == board[25] and board[25] == board[32] and board[11] != ' ':
        Game = Win
    elif board[18] == board[25] and board[25] == board[32] and board[32] == board[39] and board[18] != ' ':
        Game = Win
    elif board[25] == board[32] and board[32] == board[39] and board[39] == board[46] and board[25] != ' ':
        Game = Win

    # Vertical Check Column 5
    elif board[5] == board[12] and board[12] == board[19] and board[19] == board[26] and board[5] != ' ':
        Game = Win
    elif board[12] == board[19] and board[19] == board[26] and board[26] == board[33] and board[12] != ' ':
        Game = Win
    elif board[19] == board[26] and board[26] == board[33] and board[33] == board[40] and board[19] != ' ':
        Game = Win
    elif board[26] == board[33] and board[33] == board[40] and board[40] == board[47] and board[26] != ' ':
        Game = Win

    # Vertical Check Column 6
    elif board[6] == board[13] and board[13] == board[20] and board[20] == board[27] and board[6] != ' ':
        Game = Win
    elif board[13] == board[20] and board[20] == board[27] and board[27] == board[34] and board[13] != ' ':
        Game = Win
    elif board[20] == board[27] and board[27] == board[34] and board[34] == board[41] and board[20] != ' ':
        Game = Win
    elif board[27] == board[34] and board[34] == board[41] and board[41] == board[48] and board[27] != ' ':
        Game = Win

    # Vertical Check Column 7
    elif board[7] == board[14] and board[14] == board[21] and board[21] == board[28] and board[7] != ' ':
        Game = Win
    elif board[14] == board[21] and board[21] == board[28] and board[28] == board[35] and board[14] != ' ':
        Game = Win
    elif board[21] == board[28] and board[28] == board[35] and board[35] == board[42] and board[21] != ' ':
        Game = Win
    elif board[28] == board[35] and board[35] == board[42] and board[42] == board[49] and board[28] != ' ':
        Game = Win

    # Diagonal 1 Check 1
    elif board[1] == board[9] and board[9] == board[17] and board[17] == board[25] and board[9] != ' ' and board[17] != ' ':
        Game = Win
    elif board[9] == board[17] and board[17] == board[25] and board[25] == board[33] and board[17] != ' ' and board[25] != ' ':
        Game = Win
    elif board[17] == board[25] and board[25] == board[33] and board[33] == board[41] and board[25] != ' ' and board[33] != ' ':
        Game = Win
    elif board[25] == board[33] and board[33] == board[41] and board[41] == board[49] and board[33] != ' ' and board[41] != ' ':
        Game = Win

    # Diagonal 1 Check 2
    elif board[8] == board[16] and board[16] == board[24] and board[24] == board[32] and board[16] != ' ' and board[29] != ' ':
        Game = Win
    elif board[16] == board[24] and board[24] == board[32] and board[32] == board[40] and board[29] != ' ' and board[32] != ' ':
        Game = Win
    elif board[24] == board[32] and board[32] == board[40] and board[40] == board[48] and board[32] != ' ' and board[40] != ' ':
        Game = Win

    # Diagonal 1 Check 3
    elif board[2] == board[10] and board[10] == board[18] and board[18] == board[26] and board[10] != ' ' and board[18] != ' ':
        Game = Win
    elif board[10] == board[18] and board[18] == board[26] and board[26] == board[34] and board[18] != ' ' and board[26] != ' ':
        Game = Win
    elif board[18] == board[26] and board[26] == board[34] and board[34] == board[42] and board[26] != ' ' and board[34] != ' ':
        Game = Win

    # Diagonal 1 Check 4
    elif board[15] == board[23] and board[23] == board[31] and board[31] == board[39] and board[23] != ' ' and board[31] != ' ':
        Game = Win
    elif board[23] == board[31] and board[31] == board[39] and board[39] == board[47] and board[31] != ' ' and board[39] != ' ':
        Game = Win

    # Diagonal 1 Check 5
    elif board[3] == board[11] and board[11] == board[19] and board[19] == board[27] and board[11] != ' ' and board[19] != ' ':
        Game = Win
    elif board[11] == board[19] and board[19] == board[27] and board[27] == board[35] and board[19] != ' ' and board[27] != ' ':
        Game = Win

    # Diagonal 1 Check 6
    elif board[22] == board[30] and board[30] == board[38] and board[38] == board[46] and board[30] != ' ' and board[38] != ' ':
        Game = Win

    # Diagonal 1 Check 7
    elif board[4] == board[12] and board[12] == board[20] and board[20] == board[28] and board[12] != ' ' and board[20] != ' ':
        Game = Win

    # Diagonal 2 Check 1
    elif board[7] == board[13] and board[13] == board[19] and board[19] == board[25] and board[13] != ' ' and board[19] != ' ':
        Game = Win
    elif board[13] == board[19] and board[19] == board[25] and board[25] == board[31] and board[19] != ' ' and board[25] != ' ':
        Game = Win
    elif board[19] == board[25] and board[25] == board[31] and board[31] == board[37] and board[25] != ' ' and board[31] != ' ':
        Game = Win
    elif board[25] == board[31] and board[31] == board[37] and board[37] == board[43] and board[31] != ' ' and board[37] != ' ':
        Game = Win

    # Diagonal 2 Check 2
    elif board[6] == board[12] and board[12] == board[18] and board[18] == board[24] and board[12] != ' ' and board[18] != ' ':
        Game = Win
    elif board[12] == board[18] and board[18] == board[24] and board[24] == board[30] and board[18] != ' ' and board[24] != ' ':
        Game = Win
    elif board[18] == board[24] and board[24] == board[30] and board[30] == board[36] and board[24] != ' ' and board[30] != ' ':
        Game = Win

    # Diagonal 2 Check 3
    elif board[14] == board[20] and board[20] == board[26] and board[26] == board[32] and board[20] != ' ' and board[26] != ' ':
        Game = Win
    elif board[20] == board[26] and board[26] == board[32] and board[32] == board[38] and board[26] != ' ' and board[32] != ' ':
        Game = Win
    elif board[26] == board[32] and board[32] == board[38] and board[38] == board[44] and board[32] != ' ' and board[38] != ' ':
        Game = Win

    # Diagonal 2 Check 4
    elif board[5] == board[11] and board[11] == board[17] and board[17] == board[23] and board[11] != ' ' and board[17] != ' ':
        Game = Win
    elif board[11] == board[17] and board[17] == board[23] and board[23] == board[29] and board[17] != ' ' and board[23] != ' ':
        Game = Win

    # Diagonal 2 Check 5
    elif board[21] == board[27] and board[27] == board[33] and board[33] == board[39] and board[27] != ' ' and board[33] != ' ':
        Game = Win
    elif board[27] == board[33] and board[33] == board[39] and board[39] == board[45] and board[33] != ' ' and board[39] != ' ':
        Game = Win

    # Diagonal 2 Check 6
    elif board[4] == board[10] and board[10] == board[16] and board[16] == board[22] and board[16] != ' ' and board[10] != ' ':
        Game = Win

    # Diagonal 2 Check 7
    elif board[28] == board[34] and board[34] == board[40] and board[40] == board[46] and board[40] != ' ' and board[34] != ' ':
        Game = Win

    # Corner Check
    elif board[1] == board[7] and board[7] == board[49] and board[49] == board[43] and board[1] != ' ':
        corner_check_flag = True
        Game = Win

    # Check for Draw
    elif board[1] != ' ' and board[2] != ' ' and board[3] != ' ' and board[4] != ' ' and board[5] != ' ' \
            and board[6] != ' ' and board[7] != ' ' and board[8] != ' ' and board[9] != ' ' and board[10] != ' ' \
            and board[11] != ' ' and board[12] != ' ' and board[13] != ' ' and board[14] != ' ' and board[15] != ' ' \
            and board[16] != ' ' and board[17] != ' ' and board[18] != ' ' and board[19] != ' ' and board[20] != ' ' \
            and board[21] != ' ' and board[22] != ' ' and board[23] != ' ' and board[24] != ' ' and board[25] != ' ' \
            and board[26] != ' ' and board[27] != ' ' and board[28] != ' ' and board[29] != ' ' and board[30] != ' ' \
            and board[31] != ' ' and board[32] != ' ' and board[33] != ' ' and board[34] != ' ' and board[35] != ' ' \
            and board[36] != ' ' and board[37] != ' ' and board[38] != ' ' and board[39] != ' ' and board[40] != ' ' \
            and board[41] != ' ' and board[42] != ' ' and board[43] != ' ' and board[44] != ' ' and board[45] != ' ' \
            and board[46] != ' ' and board[47] != ' ' and board[48] != ' ' and board[49] != ' ':
        Game = Draw
    else:
        Game = Running


# This Function Checks position is empty or not
def check_position(x):
    if board[x] == ' ':
        return True
    else:
        print("Space is filled. Choose Another")
        print("\n")
        return False


print("\n")
print("\t\tTic-Tac-Toe Game\n")

# Enter Name of Player 1
print("Player 1")
player1 = input("Enter the name : ")
print("\n")

# Enter Name of Player 2
print("Player 2")
player2 = input("Enter the name : ")
print("\n")

# Display Score Board
print_scoreboard(player1, player2, player1_score, player2_score)

# Player 1 has to choose his/her Icon
print("Turn to choose for", player1)
print("Enter 1 for X")
print("Enter 2 for O")
choice = int(input("Enter your choice: "))
print("\n")

# Check for Player 1 Icon
if choice == 1:
    Mark = 'X'
    flag1 = True
elif choice == 2:
    Mark = 'O'
    flag2 = True

# The Game will Start running Until the players decide to quit
while Game == Running:
    draw_board()
    print("\n")

    # Condition for Turn of Which Player
    if player % 2 != 0:
        print("Player 1's chance")
        # Check for the Player's Icon, whether he/she choose X or O
        if flag1:
            Mark = 'X'
        else:
            Mark = 'O'
    else:
        print("Player 2's chance")
        # Check for the Player's Icon, whether he/she choose X or O
        if flag2:
            Mark = 'X'
        else:
            Mark = 'O'

    # The Current Player has to choose the cell to mark with his Icon
    pos = input("Enter the position between [1-49] where you want to mark or \nEnter E to Exit: ")
    print("\n")

    # Condition for the end of Game. Players can exit the Game by pressing E button
    if pos.upper() == 'E':
        Game = End
    # Condition to Mark the cell with the Players Icon he/she chose
    elif check_position(int(pos)):
        board[int(pos)] = Mark
        player += 1
        check_win()

        # Condition to Update the score of the player if he/she won the Game
        if Game == Win:
            if player % 2 != 0:
                draw_board()
                print("\nPlayer 2 Won")

                # Condition to Check if the Player Won by marking the Corners of the game. Then add only 2 Points
                if corner_check_flag:
                    player2_score += 2
                else:
                    player2_score += 4
            else:
                draw_board()
                print("\nPlayer 1 Won")

                # Condition to Check if the Player Won by marking the Corners of the game. Then add only 2 Points
                if corner_check_flag:
                    player1_score += 2
                else:
                    player1_score += 4

            # After the player has won. The Game will Restart
            print("\n")
            Game = Running
            board = [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',
                     ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',
                     ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']

        # Condition to Check if the game has occurred in a Draw
        elif Game == Draw:
            print("Game Draw")
            print("\n")

            # If the Game has Occurred in a Draw. Then the Game will Restart
            Game = Running
            board = [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',
                     ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ',
                     ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']


# this part of the code will run when the players decide to quit the game
draw_board()
if Game == End:
    print("\n\n")

    # Print the ScoreBoard
    print_scoreboard(player1, player2, player1_score, player2_score)

    # Condition to check which Player Secured the most Points
    if player1_score == player2_score:
        print("Game Draw")
    elif player1_score > player2_score:
        print(player1, " secured the most points. YOU ON")
    else:
        print(player2, " secured the most points. YOU ON")

