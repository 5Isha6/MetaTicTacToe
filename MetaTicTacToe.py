import random

class TicTacToe:
    def __init__(self):
        self.board = [[' ' for _ in range(3)] for _ in range(3)]

    def is_full(self):
        for row in self.board:
            for cell in row:
                if cell == ' ':
                    return False
        return True

    def reset(self):
        self.board = [[' ' for _ in range(3)] for _ in range(3)]

    def block_moves(self):
       for i in range(3):
        for j in range(3):
            if self.board[i][j] == ' ':
                self.board[i][j] = '*'

    def get_winner(self):
        for row in self.board:
            if row[0] == row[1] == row[2] != ' ':
                return row[0]
        for col in range(3):
            if self.board[0][col] == self.board[1][col] == self.board[2][col] != ' ':
                return self.board[0][col]
        if self.board[0][0] == self.board[1][1] == self.board[2][2] != ' ':
            return self.board[0][0]
        if self.board[0][2] == self.board[1][1] == self.board[2][0] != ' ':
            return self.board[0][2]
        return None

    def play_move(self, row, col, symbol):
        self.board[row][col] = symbol
        winner = self.get_winner()
        is_full = self.is_full()
        if  winner is not None:
            self.block_moves()
            is_full = False
        
        return winner, is_full

class MetaTicTacToe:
    def __init__(self):
        self.meta_board = [[TicTacToe() for _ in range(3)] for _ in range(3)]

    def print_meta_board(self):
        for row in range(3):
            for game_row in range(3):
                for col in range(3):
                    print(self.meta_board[row][col].board[game_row], end=' | ')
                print()
            print('-' * 29)

    def get_winner(self):
        for row in self.meta_board:
            row_winners = [game.get_winner() for game in row]
            if row_winners[0] == row_winners[1] == row_winners[2] != None:
                return row_winners[0]
        for col in range(3):
            col_winners = [self.meta_board[row][col].get_winner() for row in range(3)]
            if col_winners[0] == col_winners[1] == col_winners[2] != None:
                return col_winners[0]
        diagonal_winners_1 = [self.meta_board[i][i].get_winner() for i in range(3)]
        if diagonal_winners_1[0] == diagonal_winners_1[1] == diagonal_winners_1[2] != None:
            return diagonal_winners_1[0]
        diagonal_winners_2 = [self.meta_board[i][2 - i].get_winner() for i in range(3)]
        if diagonal_winners_2[0] == diagonal_winners_2[1] == diagonal_winners_2[2] != None:
            return diagonal_winners_2[0]
        return None

    def play_move(self, row, col, game_row, game_col, symbol):
        game = self.meta_board[row][col]
        winner,is_full = game.play_move(game_row, game_col, symbol)
        if winner is not None:
            print(f"{symbol} wins {row},{col} game!")
        if is_full:
            print(f"{row},{col} game is a tie, resetting it...")
            game.reset()

def get_players():
    available_types = [('Human','Computer'),('Computer','Human'),('Human','Human'),('Computer','Computer')]
    print(f"Choose the players, first players is always 'X'")
    for i,(a,b) in enumerate(available_types):
        print(f"{i+1}) Player 1 (X): {a} vs Player 2 (O): {b}")
    players = int(input("Enter your choice (1 or 2 or 3 or 4): ")) - 1

    return available_types[players]
        
def get_move(player_type, game):
    available_moves = [(r, c, gr, gc) for r in range(3) for c in range(3) for gr in range(3) for gc in range(3) if game.meta_board[r][c].board[gr][gc]==' ']
    if player_type == "Human":
        while True:
            move = input("Enter your move as row,col,game_row,game_col (e.g. 0,0,1,1): ")
            row, col, game_row, game_col = map(int, move.split(","))
            if (row,col,game_row,game_col) in available_moves:
                return row, col, game_row, game_col
            else:
                print("Invalid move")
    else:  # player_type == "Computer"
        row,col,game_row,game_col = random.choice(available_moves)
    return row, col, game_row, game_col

def main():
    game = MetaTicTacToe()
    player_types = list(get_players())
    symbols = ["X","O"]
    game.print_meta_board()
    while game.get_winner() is None:
        for i, (player_type, symbol) in enumerate(zip(player_types, symbols)):
            print(f"Player {i + 1} ({symbol}): {player_type}")
            row, col, game_row, game_col = get_move(player_type, game)
            game.play_move(row, col, game_row, game_col, symbol)
            game.print_meta_board()

            winner = game.get_winner()
            if winner is not None:
                game.print_meta_board()
                print(f"Player {i + 1} ({symbol}) wins!")
                return
            elif all(game.meta_board[r][c].is_full() for r in range(3) for c in range(3)):
                game.print_meta_board()
                print("It's a tie!")
                return

if __name__ == "__main__":
    main()
