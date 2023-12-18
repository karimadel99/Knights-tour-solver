import pandas as pd

def is_valid_move(board, x, y, N):
    return 0 <= x < N and 0 <= y < N and board[x][y] == -1

def solve_knights_tour_backtracking(N, start_x, starty):
    # Initialize the chessboard
    board = [[-1 for _ in range(N)] for _ in range(N)]

    # Possible moves for a knight
    move_x = [2, 1, -1, -2, -2, -1, 1, 2]
    move_y = [1, 2, 2, 1, -1, -2, -2, -1]

    # Start the knight's tour
    board[start_x][starty] = 0
    solution = knight_tour_util(board, start_x, starty, 1, move_x, move_y, N)
    
    if solution:
        return board
    else:
        return None

def knight_tour_util(board, x, y, move_num, move_x, move_y, N):
    if move_num == N * N:
        return True

    for k in range(8):
        next_x = x + move_x[k]
        next_y = y + move_y[k]

        if is_valid_move(board, next_x, next_y, N):
            board[next_x][next_y] = move_num
            if knight_tour_util(board, next_x, next_y, move_num + 1, move_x, move_y, N):
                return True

            # Backtrack
            board[next_x][next_y] = -1

    return False


