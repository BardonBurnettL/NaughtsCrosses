import math
import random

class Player:
    def __init__(self, symbol):
        self.symbol = symbol
    
    def get_move(self, game):
        pass
    
class RandomCompPlayer(Player):
    def __init__(self, symbol):
        super().__init__(symbol)
    
    def get_move(self, game):
        square = random.choice(game.legal_moves())
        return square

class HumanPlayer(Player):
    def __init__(self, symbol):
        super().__init__(symbol)
    
    def get_move(self, game):
        legal_square = False
        val = None
        while not legal_square:
            square = input(self.symbol + '\'s turn. Input move (0-8):')
            try:
                val = int(square)
                if val not in game.legal_moves():
                    raise ValueError
                legal_square = True
            except ValueError:
                print('Invalid move. Try again.')
        return val

class CleverCompPlayer(Player):
    def __init__(self, symbol):
        super().__init__(symbol)
    
    def get_move(self, game):
        if len(game.legal_moves()) == 9:
            square = random.choice(game.legal_moves())
        else:
            square = self.minmax(game, self.symbol)['position']
        return square
    
    def minmax(self, currentBoard, currentPlayer):
        max_player = self.symbol
        min_player = 'o' if currentPlayer == 'x' else 'x'
        if currentBoard.current_winner == min_player:
            return {'position': None, 'score': 1+currentBoard.num_empty_sq() if min_player == max_player else -1*(1+currentBoard.num_empty_sq())}
        elif not currentBoard.empty_sq():
            return {'position': None, 'score': 0}
        
        if currentPlayer == max_player:
            best = {'postion': None, 'score': -math.inf}
        else:
            best = {'postion': None, 'score': math.inf}
        
        for move in currentBoard.legal_moves():
            currentBoard.make_move(move, currentPlayer)
            simScore = self.minmax(currentBoard, min_player)
            currentBoard.board[move] = ' '
            currentBoard.current_winner = None
            simScore['position'] = move
            if currentPlayer == max_player:
                if simScore['score'] > best['score']:
                    best = simScore
            else:
                if simScore['score'] < best['score']:
                    best = simScore
        
        return best

class NaughtsAndCrosses:
    def __init__(self):
        self.board = [' ' for _ in range(9)]
        self.current_winner = None
    
    def print_board(self):
        for row in [self.board[i*3:(i+1)*3] for i in range(3)]:
            print('| ' + ' | '.join(row) + ' |')
    
    def print_board_indicies(self):
        indicies_board = [[str(i) for i in range(j*3, (j+1)*3)] for j in range(3)]
        for row in indicies_board:
            print('| ' + ' | '.join(row) + ' |')
    
    def legal_moves(self):
        # Gives every square a number and returns the numbers of empty squares
        moves = []
        for (i,sq) in enumerate(self.board):
            if sq == ' ':
                moves.append(i)
        return moves

    def empty_sq(self):
        return ' ' in self.board
    
    def num_empty_sq(self):
        return self.board.count(' ')
    
    def make_move(self, square, symbol):
        # If the square is empty, make the move and return True
        if self.board[square] == ' ':
            self.board[square] = symbol
            if self.winner(square, symbol):
                self.current_winner = symbol
            return True
        return False
    
    def winner(self, square, symbol):
        # Only have to check the most recent move if we check after every move
        row_ind = square // 3
        row = self.board[row_ind*3:(row_ind+1)*3]
        if all([sq == symbol for sq in row]):
            return True
        col_ind = square % 3
        col = [self.board[col_ind +(i*3)] for i in range(3)]
        if all([sq == symbol for sq in col]):
            return True
        if square % 2 == 0:
            diag1 = [self.board[i] for i in [0,4,8]]
            if all([sq == symbol for sq in diag1]):
                return True
            diag2 = [self.board[i] for i in [2,4,6]]
            if all([sq == symbol for sq in diag2]):
                return True
        return False
    
def play(game, x_player, o_player, print_game=True):
    if print_game:
        game.print_board_indicies()
    
    symbol = 'x'
    while game.empty_sq():
        if symbol == 'o':
            square = o_player.get_move(game)
        else:
            square = x_player.get_move(game)
        if game.make_move(square, symbol):
            if print_game:
                print(symbol + f' placed on sqaure {square}')
                game.print_board()
                print('')
            if game.current_winner:
                if print_game:
                    print(symbol + ' has won!')
                return symbol
            symbol = 'o' if symbol == 'x' else 'x'
    if print_game:
        # If there are no more squares and no one has won
        print("It's a tie.")

if __name__ == '__main__':
    x_player = HumanPlayer('x')
#    o_player = RandomCompPlayer('o')
    o_player = CleverCompPlayer('o')
    nc = NaughtsAndCrosses()
    play(nc, x_player, o_player, print_game=True)




