import random

SCORE_MIN = -100
SCORE_MAX = 100
N = 8


def allowed_moves(board, color):
    # TODO: Your turn now !
    moves = find_capturing_moves(board, color)
    if (len(moves) == 0):
        moves = find_non_capt_moves(board, color)
    return moves


def get_my_positions(board, color):
#return all player's discs positions
    my_positions = []
    for r in range(N):
        for c in range(N):
            if board[r][c].lower() == color:
                my_positions.append([r, c])
    return my_positions

"""*******************************************************
****************************************"""
#Non-Capturing Moves related functions:


def find_non_capt_moves(board, color):
    #List all player's non-capturing moves
    moves = []
    for position in get_my_positions(board, color):
        r = position[0]
        c = position[1]
        if can_move([r, c], [r+1, c+1], board):
            moves.append([(r, c), (r+1, c+1)])
        if can_move([r, c], [r-1, c+1], board):
            moves.append([(r, c), (r-1, c+1)])
        if can_move([r, c], [r+1, c-1], board):
            moves.append([(r, c), (r+1, c-1)])
        if can_move([r, c], [r-1, c-1], board):
            moves.append([(r, c), (r-1, c-1)])
    return moves


def can_move(actuel, dest, board):
    #Return if a non-capturing move is possible or not
    #destination valide?
    if (dest[0] < 0 or dest[0] > N-1 or dest[1] < 0 or dest[1] > N-1):
        return False
    if (board[dest[0]][dest[1]] != '_'):
        return False

    if (board[actuel[0]][actuel[1]] == 'w'):
        if (dest[0] > actuel[0]):
            return False
        else:
            return True

    if board[actuel[0]][actuel[1]] == 'b':
        if dest[0] < actuel[0]:
            return False
        else:
            return True
    if board[actuel[0]][actuel[1]] == 'B' or
       board[actuel[0]][actuel[1]] == 'W':
            return True

"""*******************************************************
****************************************"""

#Capturing Moves related functions:

def find_capturing_moves(board, color):
    """
        Return the list of all jumps (multiple jumps included)
    """
    moves = []
    for position in get_my_positions(board, color):
        
        first_jumps=[]
        q = [] 
        #for each player's disc find possible "one-jump"s  
        first_jumps = jumps(position, board, color) 
        if len(first_jumps) > 0:
            #store possible position sequences
            q = [[position, p] for p in first_jumps]
        while len(q) > 0:
            #find all possible paths for jumps
            jump = q.pop(0)
            new_board = []
            new_board = update_board(board, jump)
            pos_capt = jumps(jump[-1], new_board, color)
            if len(pos_capt) == 0:
                moves += [jump]
            else:
                for p in pos_capt:
                    q += [jump + [p]]
    return moves


def jumps(position, board, color):
    """
    Get possible 1st jump destinations
    """
    row = position[0]
    col = position[1]

    br_1 = []
    br_2 = []
    br_3 = []
    br_4 = []
    #find out all possible branches
    if can_jump([row, col], [row + 1, col + 1],[row + 2, col + 2], board, color):
        br_1 = [[row + 2, col + 2]]
    if can_jump([row, col], [row - 1, col + 1], [row - 2, col + 2], board, color):
        br_2 = [[row - 2, col + 2]]
    if can_jump([row, col], [row + 1, col - 1], [row + 2, col - 2], board, color):
        br_3 = [[row + 2, col - 2]]
    if can_jump([row, col], [row - 1, col - 1], [row - 2, col - 2], board, color):
        br_4 = [[row - 2, col - 2]]
    jumps_dest = br_1 + br_2 + br_3 + br_4
    return jumps_dest


def can_jump(actuel, via, dest, board, color):
    #destination valide?
    if dest[0] < 0 or dest[0] > 7 or dest[1] < 0 or dest[1] > 7:
        return False
    if board[dest[0]][dest[1]] != '_':
        return False
    #whites
    if color == 'w':
        if dest[0] > actuel[0] and board[actuel[0]][actuel[1]] != 'W':
            return False
        if board[via[0]][via[1]].lower() != 'b':
            return False
        return True
    #balack moves
    if color == 'b':
        if dest[0] < actuel[0] and board[actuel[0]][actuel[1]] != 'B':
            return False
        if board[via[0]][via[1]].lower() != 'w':
            return False
        return True


"""*******************************************************
****************************************"""
#get the board updated


def single_update_board(board, prev_pos, next_pos):
    """
        updates the board based on a single move
    """
    prev_row, prev_col = prev_pos
    next_row, next_col = next_pos
    new_board = board
    color = board[prev_row][prev_col].lower()
    disc = board[prev_row][prev_col]
    # Check if a disc gets to be a king
    if board[prev_row][prev_col] == "b" and next_row == 7:
        disc = disc.upper()
    elif board[prev_row][prev_col] == "w" and next_row == 0:
        disc = disc.upper()
    s = list(new_board[next_row])
    s[next_col] = disc
    new_board[next_row] = "".join(s)
    s = list(new_board[prev_row])
    s[prev_col] = "_"
    new_board[prev_row] = "".join(s)
    # Capture the ennemy
    if abs(next_row - prev_row) == 2:
        s = list(new_board[(next_row + prev_row) / 2])
        s[(next_col + prev_col) / 2] = "_"
        new_board[(next_row + prev_row) / 2] = "".join(s)
    return new_board


def update_board(board, moves):
    # Update the board up to the last position step
    new_board = board[:]
    for i in range(0, len(moves) - 1):
        prev_pos = moves[i]
        next_pos = moves[i + 1]
        new_board = single_update_board(new_board, prev_pos, next_pos)
    return new_board
"""************************************************************
********************************************"""


def opposite_color(color):
    if color == 'w':
        return 'b'
    elif color == 'b':
        return 'w'


def score(board, color):
    """
        The score takes into consideration the number of discs, the number of kings
    """
    score = [0, 0]
    for x in range(N):
        for y in range(N):
            if board[x][y].lower() == color:
                score[0] += 1 if (board[x][y] == color) else 2
            elif board[x][y] == opposite_color(color):
                score[1] += 1 if (opposite_color(color)) else 2
    return score[0] - score[1] if score[0] and score[1] else SCORE_MAX if score[1] == 0 else SCORE_MIN


def minimax(board, color, your_turn_now, depth):
    whos_turn_now = color if your_turn_now else opposite_color(color)
    if len(allowed_moves(board, whos_turn_now)) == 0 or (depth == 0):
        return score(board, color)
    if your_turn_now:
        best_value = SCORE_MIN
        for move in allowed_moves(board, color):
            new_board = update_board(board, move)
            value = minimax(new_board, color, False, depth - 1)
            best_value = max(best_value, value)
    if not your_turn_now:
        best_value = SCORE_MAX
        for move in allowed_moves(board, opposite_color(color)):
            new_board = update_board(board, move)
            value = minimax(new_board, color, True, depth - 1)
            best_value = min(best_value, value)
    return best_value


def play_minimax(board, color):
    moves = allowed_moves(board, color)
    choices = {}
    for index, move in enumerate(moves):
        new_board = update_board(board, move)
        choices[index] = minimax(new_board, color, False, 3)
    best_choices = [i for i, j in choices.iteritems() if j == max(choices.values())]
    best_choice = random.choice(best_choices)
    return moves[best_choice]


def play(board, color):
    return play_minimax(board, color)


def random_play(board, color):
    """
        An example of play function based on allowed_moves.
    """
    moves = allowed_moves(board, color)
    # There will always be an allowed move
    # because otherwise the game is over and
    # 'play' would not be called by main.py
    return random.choice(moves)
import random

SCORE_MIN = -100
SCORE_MAX = 100
N = 8


def allowed_moves(board, color):
    # TODO: Your turn now !
    moves = find_capturing_moves(board, color)
    if (len(moves) == 0):
        moves = find_non_capt_moves(board, color)
    return moves


def get_my_positions(board, color):
#return all player's discs positions
    my_positions = []
    for r in range(N):
        for c in range(N):
            if board[r][c].lower() == color:
                my_positions.append([r, c])
    return my_positions

"""*******************************************************
****************************************"""
#Non-Capturing Moves related functions:


def find_non_capt_moves(board, color):
    #List all player's non-capturing moves
    moves = []
    for position in get_my_positions(board, color):
        r = position[0]
        c = position[1]
        if can_move([r, c], [r+1, c+1], board):
            moves.append([(r, c), (r+1, c+1)])
        if can_move([r, c], [r-1, c+1], board):
            moves.append([(r, c), (r-1, c+1)])
        if can_move([r, c], [r+1, c-1], board):
            moves.append([(r, c), (r+1, c-1)])
        if can_move([r, c], [r-1, c-1], board):
            moves.append([(r, c), (r-1, c-1)])
    return moves


def can_move(actuel, dest, board):
    #Return if a non-capturing move is possible or not
    #destination valide?
    if (dest[0] < 0 or dest[0] > N-1 or dest[1] < 0 or dest[1] > N-1):
        return False
    if (board[dest[0]][dest[1]] != '_'):
        return False

    if (board[actuel[0]][actuel[1]] == 'w'):
        if (dest[0] > actuel[0]):
            return False
        else:
            return True

    if board[actuel[0]][actuel[1]] == 'b':
        if dest[0] < actuel[0]:
            return False
        else:
            return True
    if board[actuel[0]][actuel[1]] == 'B' or
       board[actuel[0]][actuel[1]] == 'W':
            return True

"""*******************************************************
****************************************"""

#Capturing Moves related functions:

def find_capturing_moves(board, color):
    """
        Return the list of all jumps (multiple jumps included)
    """
    moves = []
    for position in get_my_positions(board, color):
        
        first_jumps=[]
        q = [] 
        #for each player's disc find possible "one-jump"s  
        first_jumps = jumps(position, board, color) 
        if len(first_jumps) > 0:
            #store possible position sequences
            q = [[position, p] for p in first_jumps]
        while len(q) > 0:
            #find all possible paths for jumps
            jump = q.pop(0)
            new_board = []
            new_board = update_board(board, jump)
            pos_capt = jumps(jump[-1], new_board, color)
            if len(pos_capt) == 0:
                moves += [jump]
            else:
                for p in pos_capt:
                    q += [jump + [p]]
    return moves


def jumps(position, board, color):
    """
    Get possible 1st jump destinations
    """
    row = position[0]
    col = position[1]

    br_1 = []
    br_2 = []
    br_3 = []
    br_4 = []
    #find out all possible branches
    if can_jump([row, col], [row + 1, col + 1],[row + 2, col + 2], board, color):
        br_1 = [[row + 2, col + 2]]
    if can_jump([row, col], [row - 1, col + 1], [row - 2, col + 2], board, color):
        br_2 = [[row - 2, col + 2]]
    if can_jump([row, col], [row + 1, col - 1], [row + 2, col - 2], board, color):
        br_3 = [[row + 2, col - 2]]
    if can_jump([row, col], [row - 1, col - 1], [row - 2, col - 2], board, color):
        br_4 = [[row - 2, col - 2]]
    jumps_dest = br_1 + br_2 + br_3 + br_4
    return jumps_dest


def can_jump(actuel, via, dest, board, color):
    #destination valide?
    if dest[0] < 0 or dest[0] > 7 or dest[1] < 0 or dest[1] > 7:
        return False
    if board[dest[0]][dest[1]] != '_':
        return False
    #whites
    if color == 'w':
        if dest[0] > actuel[0] and board[actuel[0]][actuel[1]] != 'W':
            return False
        if board[via[0]][via[1]].lower() != 'b':
            return False
        return True
    #balack moves
    if color == 'b':
        if dest[0] < actuel[0] and board[actuel[0]][actuel[1]] != 'B':
            return False
        if board[via[0]][via[1]].lower() != 'w':
            return False
        return True


"""*******************************************************
****************************************"""
#get the board updated


def single_update_board(board, prev_pos, next_pos):
    """
        updates the board based on a single move
    """
    prev_row, prev_col = prev_pos
    next_row, next_col = next_pos
    new_board = board
    color = board[prev_row][prev_col].lower()
    disc = board[prev_row][prev_col]
    # Check if a disc gets to be a king
    if board[prev_row][prev_col] == "b" and next_row == 7:
        disc = disc.upper()
    elif board[prev_row][prev_col] == "w" and next_row == 0:
        disc = disc.upper()
    s = list(new_board[next_row])
    s[next_col] = disc
    new_board[next_row] = "".join(s)
    s = list(new_board[prev_row])
    s[prev_col] = "_"
    new_board[prev_row] = "".join(s)
    # Capture the ennemy
    if abs(next_row - prev_row) == 2:
        s = list(new_board[(next_row + prev_row) / 2])
        s[(next_col + prev_col) / 2] = "_"
        new_board[(next_row + prev_row) / 2] = "".join(s)
    return new_board


def update_board(board, moves):
    # Update the board up to the last position step
    new_board = board[:]
    for i in range(0, len(moves) - 1):
        prev_pos = moves[i]
        next_pos = moves[i + 1]
        new_board = single_update_board(new_board, prev_pos, next_pos)
    return new_board
"""************************************************************
********************************************"""


def opposite_color(color):
    if color == 'w':
        return 'b'
    elif color == 'b':
        return 'w'


def score(board, color):
    """
        The score takes into consideration the number of discs, the number of kings
    """
    score = [0, 0]
    for x in range(N):
        for y in range(N):
            if board[x][y].lower() == color:
                score[0] += 1 if (board[x][y] == color) else 2
            elif board[x][y] == opposite_color(color):
                score[1] += 1 if (opposite_color(color)) else 2
    return score[0] - score[1] if score[0] and score[1] else SCORE_MAX if score[1] == 0 else SCORE_MIN


def minimax(board, color, your_turn_now, depth):
    whos_turn_now = color if your_turn_now else opposite_color(color)
    if len(allowed_moves(board, whos_turn_now)) == 0 or (depth == 0):
        return score(board, color)
    if your_turn_now:
        best_value = SCORE_MIN
        for move in allowed_moves(board, color):
            new_board = update_board(board, move)
            value = minimax(new_board, color, False, depth - 1)
            best_value = max(best_value, value)
    if not your_turn_now:
        best_value = SCORE_MAX
        for move in allowed_moves(board, opposite_color(color)):
            new_board = update_board(board, move)
            value = minimax(new_board, color, True, depth - 1)
            best_value = min(best_value, value)
    return best_value


def play_minimax(board, color):
    moves = allowed_moves(board, color)
    choices = {}
    for index, move in enumerate(moves):
        new_board = update_board(board, move)
        choices[index] = minimax(new_board, color, False, 3)
    best_choices = [i for i, j in choices.iteritems() if j == max(choices.values())]
    best_choice = random.choice(best_choices)
    return moves[best_choice]


def play(board, color):
    return play_minimax(board, color)


def random_play(board, color):
    """
        An example of play function based on allowed_moves.
    """
    moves = allowed_moves(board, color)
    # There will always be an allowed move
    # because otherwise the game is over and
    # 'play' would not be called by main.py
    return random.choice(moves)
