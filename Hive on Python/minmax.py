import math

AI = "X"
HUMAN = "O"
EMPTY = " "

def is_terminal(board):
    return evaluate(board) != 0 or EMPTY not in board

def evaluate(board):
    wins = [
        (0,1,2), (3,4,5), (6,7,8),   # rows
        (0,3,6), (1,4,7), (2,5,8),   # cols
        (0,4,8), (2,4,6)             # diagonals
    ]

    for a,b,c in wins:
        if board[a] == board[b] == board[c] != EMPTY:
            return +1 if board[a] == AI else -1
    return 0

def get_possible_moves(board):
    return [i for i in range(len(board)) if board[i] == EMPTY]

def apply_move(board, move, player):
    new_board = board[:]
    new_board[move] = player
    return new_board

def minimax(board, depth, alpha, beta, maximizing):
    if depth == 0 or is_terminal(board):
        return evaluate(board)

    if maximizing:  # AI
        max_eval = -math.inf
        for move in get_possible_moves(board):
            result = minimax(apply_move(board, move, AI), depth - 1, alpha, beta, False)
            max_eval = max(max_eval, result)
            alpha = max(alpha, result)
            if alpha >= beta:
                break
        return max_eval

    else:  # Human
        min_eval = math.inf
        for move in get_possible_moves(board):
            result = minimax(apply_move(board, move, HUMAN), depth - 1, alpha, beta, True)
            min_eval = min(min_eval, result)
            beta = min(beta, result)
            if alpha >= beta:

                break
            else:
                print("Alpha: ", alpha)
                print("Beta: ", beta)
                print("Depth: ", depth)
        return min_eval

def best_move(board):
    best_value = -math.inf
    move_chosen = None

    for move in get_possible_moves(board):
        value = minimax(apply_move(board, move, AI), 9, -math.inf, math.inf, False)
        if value > best_value:
            best_value = value
            move_chosen = move

    return move_chosen

# Example usage:
board = [
    "O", " ", " ",
    " ", " ", " ",
    " ", " ", " "
]

print("Best move:", best_move(board))