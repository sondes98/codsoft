import math

# Initialize the board
board = [' ' for _ in range(9)]  # Represents a 3x3 board (list of 9 spaces)

def print_board(board):
    """Prints the current state of the board."""
    for row in [board[i*3:(i+1)*3] for i in range(3)]:
        print('| ' + ' | '.join(row) + ' |')

def is_winner(board, player):
    """Check if the player has won the game."""
    win_conditions = [(0, 1, 2), (3, 4, 5), (6, 7, 8),
                    (0, 3, 6), (1, 4, 7), (2, 5, 8), 
                    (0, 4, 8), (2, 4, 6)]          
    return any(board[a] == board[b] == board[c] == player for (a, b, c) in win_conditions)

def is_draw(board):
    """Check if the game is a draw."""
    return ' ' not in board

def get_available_moves(board):
    """Returns a list of available moves."""
    return [i for i, spot in enumerate(board) if spot == ' ']

def minimax(board, depth, is_maximizing):
    """The Minimax algorithm with depth-limited search."""
    if is_winner(board, 'O'):  # AI is 'O'
        return 1
    if is_winner(board, 'X'):  # Human is 'X'
        return -1
    if is_draw(board):
        return 0

    if is_maximizing:
        best_score = -math.inf
        for move in get_available_moves(board):
            board[move] = 'O'
            score = minimax(board, depth + 1, False)
            board[move] = ' '
            best_score = max(score, best_score)
        return best_score
    else:
        best_score = math.inf
        for move in get_available_moves(board):
            board[move] = 'X'
            score = minimax(board, depth + 1, True)
            board[move] = ' '
            best_score = min(score, best_score)
        return best_score

def best_move(board):
    """Finds the best move for the AI."""
    best_score = -math.inf
    move = None
    for available_move in get_available_moves(board):
        board[available_move] = 'O'
        score = minimax(board, 0, False)
        board[available_move] = ' '
        if score > best_score:
            best_score = score
            move = available_move
    return move

def play_game():
    """Main game loop."""
    while True:
        print_board(board)
        # Human move
        human_move = int(input("Enter your move (1-9): ")) - 1
        if board[human_move] == ' ':
            board[human_move] = 'X'
        else:
            print("Invalid move! Try again.")
            continue
        
        if is_winner(board, 'X'):
            print_board(board)
            print("You win!")
            break
        if is_draw(board):
            print_board(board)
            print("It's a draw!")
            break
        
        # AI move
        ai_move = best_move(board)
        board[ai_move] = 'O'
        
        if is_winner(board, 'O'):
            print_board(board)
            print("AI wins!")
            break
        if is_draw(board):
            print_board(board)
            print("It's a draw!")
            break

# Start the game
play_game()
