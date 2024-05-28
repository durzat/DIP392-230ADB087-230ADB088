import pygame
import sys



# Constants for the game
WIDTH = 700
HEIGHT = 700
ROW_COUNT = 6
COLUMN_COUNT = 7
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
SQUARESIZE = 100
RADIUS = int(SQUARESIZE / 2 - 5)

# Set up the display
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Connect Four")
font = pygame.font.SysFont("monospace", 30)



class BoardGame:
    def __init__(self):
        self.board = self.init_board()

    # Initializes the game board by creating a 2D matrix (list of lists) filled with zeros, representing an empty board.
    def init_board(self):
        return [[0 for _ in range(COLUMN_COUNT)] for _ in range(ROW_COUNT)]

    # Adds a token to the game board at the position specified by the row and column coordinates.
    # The token is represented by a value (1 for player 1 and 2 for player 2).
    def add_token(self, row, col, piece):
        self.board[row][col] = piece


class GameTurn:
    def __init__(self):
        self.turn = 0
    
    # Increments the current round of the game. Changes player (alternating between 0 and 1) after each round.
    def new_turn(self):
        self.turn = (self.turn + 1) % 2
        return self.turn


class GameState:
    # Checks if the specified player (represented by piece) has won.
    # This includes checks for horizontal, vertical and diagonal alignments of four identical tokens.
    @staticmethod
    def check_if_win(board, piece):
        # Check horizontal locations for win
        for c in range(COLUMN_COUNT - 3):
            for r in range(ROW_COUNT):
                if board[r][c] == piece and board[r][c + 1] == piece and board[r][c + 2] == piece and board[r][c + 3] == piece:
                    return True

        # Check vertical locations for win
        for c in range(COLUMN_COUNT):
            for r in range(ROW_COUNT - 3):
                if board[r][c] == piece and board[r + 1][c] == piece and board[r + 2][c] == piece and board[r + 3][c] == piece:
                    return True

        # Check positively sloped diagonals
        for c in range(COLUMN_COUNT - 3):
            for r in range(ROW_COUNT - 3):
                if board[r][c] == piece and board[r + 1][c + 1] == piece and board[r + 2][c + 2] == piece and board[r + 3][c + 3] == piece:
                    return True

        # Check negatively sloped diagonals
        for c in range(COLUMN_COUNT - 3):
            for r in range(3, ROW_COUNT):
                if board[r][c] == piece and board[r - 1][c + 1] == piece and board[r - 2][c + 2] == piece and board[r - 3][c + 3] == piece:
                    return True

        return False

    # Checks if the game ends in a tie (draw), that is, if all the cells on the board are filled without there being a winner.
    @staticmethod
    def check_if_egality(board):
        for row in board:
            if 0 in row:
                return False
        return True


class Move:
    # Checks if a movement is valid, that is to say if the chosen column is not full.
    @staticmethod
    def check_if_valid_move(board, col):
        return board[ROW_COUNT - 1][col] == 0

    # Finds the next open (empty) row in a specified column where a token can be inserted.
    @staticmethod
    def get_next_open_row(board, col):
        for r in range(ROW_COUNT):
            if board[r][col] == 0:
                return r


class Graphic:
    # Displays the game board on the screen.Draw the blue squares and black circles to represent the empty cells,
    # then draw the red and green tokens according to the movements made by the players.
    @staticmethod
    def display_board(board):
        for c in range(COLUMN_COUNT):
            for r in range(ROW_COUNT):
                pygame.draw.rect(screen, BLUE, (c * SQUARESIZE, r * SQUARESIZE + SQUARESIZE, SQUARESIZE, SQUARESIZE))
                pygame.draw.circle(screen, BLACK, (int(c * SQUARESIZE + SQUARESIZE / 2), int(r * SQUARESIZE + SQUARESIZE / 2 + SQUARESIZE)), RADIUS)
        for c in range(COLUMN_COUNT):
            for r in range(ROW_COUNT):
                if board[r][c] == 1:
                    pygame.draw.circle(screen, RED, (int(c * SQUARESIZE + SQUARESIZE / 2), HEIGHT - int(r * SQUARESIZE + SQUARESIZE / 2)), RADIUS)
                elif board[r][c] == 2:
                    pygame.draw.circle(screen, GREEN, (int(c * SQUARESIZE + SQUARESIZE / 2), HEIGHT - int(r * SQUARESIZE + SQUARESIZE / 2)), RADIUS)
        pygame.display.update()

    # Shows the position of the token being placed above the board based on mouse movement. 
    @staticmethod
    def display_choice(posx, turn):
        pygame.draw.rect(screen, BLACK, (0, 0, WIDTH, SQUARESIZE))
        pygame.draw.circle(screen, RED if turn == 0 else GREEN, (posx, int(SQUARESIZE / 2)), RADIUS)
        pygame.display.update()

    # Displays a temporary message on the screen, for example when an invalid movement is performed.
    @staticmethod
    def display_error(label):
        screen.blit(label, (40, 10))
        pygame.display.update()



def main():
    board_game = BoardGame()
    game_turn = GameTurn()
    graphic = Graphic()

    game_over = False

    graphic.display_board(board_game.board)

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            if event.type == pygame.MOUSEMOTION:
                posx = event.pos[0]
                graphic.display_choice(posx, game_turn.turn)

            if event.type == pygame.MOUSEBUTTONDOWN:
                pygame.draw.rect(screen, BLACK, (0, 0, WIDTH, SQUARESIZE))
                posx = event.pos[0]
                col = posx // SQUARESIZE

                if Move.check_if_valid_move(board_game.board, col):
                    row = Move.get_next_open_row(board_game.board, col)
                    board_game.add_token(row, col, 1 if game_turn.turn == 0 else 2)

                    if GameState.check_if_win(board_game.board, 1 if game_turn.turn == 0 else 2):
                        print(f"Player {game_turn.turn + 1} wins!")
                        game_over = True

                    if GameState.check_if_egality(board_game.board):
                        print("Game is a tie!")
                        game_over = True

                    game_turn.new_turn()

                    graphic.display_board(board_game.board)
                else:
                    label = font.render("You can't play that >:(", 1, RED)
                    graphic.display_error(label)
                    pygame.time.wait(1000)

                if game_over:
                    pygame.time.wait(3000)


if __name__ == "__main__":
    main()
