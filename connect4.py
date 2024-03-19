def print_board(board):
    for row in board:
        print("|", end="")
        for cell in row:
            if cell == 0:
                print(" ", end="|")
            elif cell == 1:
                print("X", end="|")
            elif cell == 2:
                print("O", end="|")
        print()
    print("-" * (len(board[0]) * 2 + 1))
    for col in range(len(board[0])):
        print(" " + str(col + 1), end="")
    print()

def drop_piece(board, col, piece):
    for row in range(len(board)-1, -1, -1):
        if board[row][col] == 0:
            board[row][col] = piece
            return True
    return False

def check_win(board, player):

    for row in range(len(board)):
        for col in range(len(board[0]) - 3):
            if board[row][col] == player and board[row][col+1] == player and board[row][col+2] == player and board[row][col+3] == player:
                return True

    for row in range(len(board) - 3):
        for col in range(len(board[0])):
            if board[row][col] == player and board[row+1][col] == player and board[row+2][col] == player and board[row+3][col] == player:
                return True

    for row in range(len(board) - 3):
        for col in range(len(board[0]) - 3):
            if board[row][col] == player and board[row+1][col+1] == player and board[row+2][col+2] == player and board[row+3][col+3] == player:
                return True

    for row in range(3, len(board)):
        for col in range(len(board[0]) - 3):
            if board[row][col] == player and board[row-1][col+1] == player and board[row-2][col+2] == player and board[row-3][col+3] == player:
                return True

    return False

def main():
    board = [[0 for _ in range(7)] for _ in range(6)]
    player = 1
    game_over = False
    
    while not game_over:
        print_board(board)
        print(f"Player {player}'s turn")
        try:
            col = int(input("Choose a column: ")) - 1
            if col < 0 or col >= len(board[0]):
                print("Invalid column! Please choose a column between 1 and", len(board[0]))
                continue
            if not drop_piece(board, col, player):
                print("Column is full! Choose another column.")
                continue
            if check_win(board, player):
                print_board(board)
                print(f"Player {player} wins!")
                game_over = True
            elif all(cell != 0 for row in board for cell in row):
                print_board(board)
                print("It's a draw!")
                game_over = True
            else:
                player = 1 if player == 2 else 2
        except ValueError:
            print("Invalid input! Please enter a number.")
        except KeyboardInterrupt:
            print("\nGame ended by user.")
            break

if __name__ == "__main__":
    main()

