import numpy as np
import random
import pickle

class TicTacToe:
    def __init__(self):
        self.board = [' ' for _ in range(9)]
        self.current_winner = None

    def print_board(self):
        for row in [self.board[i*3:(i+1)*3] for i in range(3)]:
            print('| ' + ' | '.join(row) + ' |')

    @staticmethod
    def print_board_nums():
        number_board = [[str(i) for i in range(j*3, (j+1)*3)] for j in range(3)]
        for row in number_board:
            print('| ' + ' | '.join(row) + ' |')

    def available_moves(self):
        return [i for i, spot in enumerate(self.board) if spot == ' ']

    def empty_squares(self):
        return ' ' in self.board

    def num_empty_squares(self):
        return self.board.count(' ')

    def make_move(self, square, letter):
        if self.board[square] == ' ':
            self.board[square] = letter
            if self.winner(square, letter):
                self.current_winner = letter
            return True
        return False

    def winner(self, square, letter):
        row_ind = square // 3
        row = self.board[row_ind*3:(row_ind+1)*3]
        if all([spot == letter for spot in row]):
            return True
        col_ind = square % 3
        column = [self.board[col_ind+i*3] for i in range(3)]
        if all([spot == letter for spot in column]):
            return True
        if square % 2 == 0:
            diagonal1 = [self.board[i] for i in [0, 4, 8]]
            if all([spot == letter for spot in diagonal1]):
                return True
            diagonal2 = [self.board[i] for i in [2, 4, 6]]
            if all([spot == letter for spot in diagonal2]):
                return True
        return False

class QLearningPlayer:
    def __init__(self, letter, epsilon=0.2, alpha=0.3, gamma=0.9):
        self.letter = letter
        self.epsilon = epsilon  # Exploration rate
        self.alpha = alpha      # Learning rate
        self.gamma = gamma      # Discount factor
        self.q_table = {}

    def get_q_value(self, state, action):
        return self.q_table.get((state, action), 0.0)

    def choose_action(self, state, available_moves):
        if random.uniform(0, 1) < self.epsilon:
            return random.choice(available_moves)
        else:
            q_values = [self.get_q_value(state, a) for a in available_moves]
            max_q = max(q_values)
            return random.choice([a for a, q in zip(available_moves, q_values) if q == max_q])

    def learn(self, state, action, reward, next_state, next_available_moves):
        old_q = self.get_q_value(state, action)
        future_q = max([self.get_q_value(next_state, a) for a in next_available_moves]) if next_available_moves else 0
        self.q_table[(state, action)] = old_q + self.alpha * (reward + self.gamma * future_q - old_q)

    def save_q_table(self, filename):
        with open(filename, 'wb') as f:
            pickle.dump(self.q_table, f)

    def load_q_table(self, filename):
        with open(filename, 'rb') as f:
            self.q_table = pickle.load(f)

def state_to_tuple(board):
    return tuple(board)

def play_game(ai_player, human_player, episodes=1000):
    for episode in range(episodes):
        game = TicTacToe()
        state = state_to_tuple(game.board)
        while game.empty_squares():
            if game.current_winner:
                break
            if game.board.count(' ') % 2 == 1:
                action = ai_player.choose_action(state, game.available_moves())
                game.make_move(action, ai_player.letter)
                reward = 1 if game.current_winner == ai_player.letter else 0
                next_state = state_to_tuple(game.board)
                next_available_moves = game.available_moves()
                ai_player.learn(state, action, reward, next_state, next_available_moves)
                state = next_state
            else:
                action = human_player.get_move(state, game.available_moves())
                game.make_move(action, human_player.letter)
                state = state_to_tuple(game.board)


def play(game, x_player, o_player, print_game=True):
    if print_game:
        game.print_board_nums()

    letter = 'X'
    while game.empty_squares():
        if game.current_winner:
            if print_game:
                print(letter + ' wins!')
            return letter

        if letter == 'O':
            square = o_player.get_move(game)
        else:
            square = x_player.get_move(game)

        if game.make_move(square, letter):
            if print_game:
                print(letter + f' makes a move to square {square}')
                game.print_board()
                print('')

            letter = 'O' if letter == 'X' else 'X'

        if game.current_winner:
            if print_game:
                print(letter + ' wins!')
            return letter

    if print_game:
        print('It\'s a tie!')

# Human player randomly choosing actions
class RandomPlayer:
    def __init__(self, letter):
        self.letter = letter

    def get_move(self, state, available_moves):
        return random.choice(available_moves)

class HumanPlayer:
    def __init__(self, letter):
        self.letter = letter

    def get_move(self, state, game):
        valid_square = False
        val = None
        while not valid_square:
            square = input(self.letter + '\'s turn. Input move (0-8): ')
            try:
                val = int(square)
                if val not in game.available_moves():
                    raise ValueError
                valid_square = True
            except ValueError:
                print('Invalid square. Try again.')
        return val

# Training the AI
if __name__ == '__main__':
    ai_player = QLearningPlayer('X')
    human_player = RandomPlayer('O')
    play_game(ai_player, human_player, episodes=10000)
    ai_player.save_q_table('q_table.pkl')

game = TicTacToe()
me = HumanPlayer('X')
print('Ready AI')
# Testing the AI
ai_player.load_q_table('q_table.pkl')
play(game, ai_player, me, print_game=True)
print('done')
