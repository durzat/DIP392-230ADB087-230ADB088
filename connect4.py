import pygame
import sys



WIDTH = 700
HEIGHT = 700
ROW_COUNT = 6
COLUMN_COUNT = 7
BLUE = (255, 255, 255)
GREEN = (255, 255, 0)
BLACK = (48, 25, 52)
RED = (255, 165, 0)
SQUARESIZE = 100
RADIUS = int(SQUARESIZE / 2 - 5)

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Connect Four")
font = pygame.font.SysFont("monospace", 30)



class BoardGame:
    def __init__(self):
        self.board = self.init_board()

    def init_board(self):
        return [[0 for _ in range(COLUMN_COUNT)] for _ in range(ROW_COUNT)]

    def add_token(self, row, col, piece):
        self.board[row][col] = piece


class GameTurn:
    def __init__(self):
        self.turn = 0
    
    def new_turn(self):
        self.turn = (self.turn + 1) % 2
        return self.turn


class GameState:
    @staticmethod
    def check_if_win(board, piece):
        for c in range(COLUMN_COUNT - 3):
            for r in range(ROW_COUNT):
                if board[r][c] == piece and board[r][c + 1] == piece and board[r][c + 2] == piece and board[r][c + 3] == piece:
                    return True

        for c in range(COLUMN_COUNT):
            for r in range(ROW_COUNT - 3):
                if board[r][c] == piece and board[r + 1][c] == piece and board[r + 2][c] == piece and board[r + 3][c] == piece:
                    return True

        for c in range(COLUMN_COUNT - 3):
            for r in range(ROW_COUNT - 3):
                if board[r][c] == piece and board[r + 1][c + 1] == piece and board[r + 2][c + 2] == piece and board[r + 3][c + 3] == piece:
                    return True

        for c in range(COLUMN_COUNT - 3):
            for r in range(3, ROW_COUNT):
                if board[r][c] == piece and board[r - 1][c + 1] == piece and board[r - 2][c + 2] == piece and board[r - 3][c + 3] == piece:
                    return True

        return False

    @staticmethod
    def check_if_egality(board):
        for row in board:
            if 0 in row:
                return False
        return True


class Move:
    @staticmethod
    def check_if_valid_move(board, col):
        return board[ROW_COUNT - 1][col] == 0

    @staticmethod
    def get_next_open_row(board, col):
        for r in range(ROW_COUNT):
            if board[r][col] == 0:
                return r


class Graphic:
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

    @staticmethod
    def display_choice(posx, turn):
        pygame.draw.rect(screen, BLACK, (0, 0, WIDTH, SQUARESIZE))
        pygame.draw.circle(screen, RED if turn == 0 else GREEN, (posx, int(SQUARESIZE / 2)), RADIUS)
        pygame.display.update()

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
                        if game_turn.turn + 1 == 1:
                            label = font.render("Player 1 wins!", 1 , RED)
                        else:
                            label = font.render("Player 2 wins!", 1 , RED)   
                        graphic.display_error(label)
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
