import pandas as pd

def is_valid_move(board, x, y, N):
    return 0 <= x < N and 0 <= y < N and board[x][y] == -1

def create_empty_board(N):
    return [[-1 for _ in range(N)] for _ in range(N)]

def solve_optimized_backtracking(N, start_x, start_y):
    # Initialize the chessboard
    board = create_empty_board(N)

    # Possible moves for a knight
    move_x = [2, 1, -1, -2, -2, -1, 1, 2]
    move_y = [1, 2, 2, 1, -1, -2, -2, -1]

    # Start the knight's tour
    board[start_x][start_y] = 0
    if knight_tour_util(board, start_x, start_y, 1, move_x, move_y, N):
        return board

def knight_tour_util(board, x, y, move_num, move_x, move_y, N):
    if move_num == N * N:
        return True

    # Use Warnsdorff's rule to prioritize moves with the fewest available next moves
    moves = [(x + move_x[i], y + move_y[i]) for i in range(8)]
    moves = [(next_x, next_y) for next_x, next_y in moves if is_valid_move(board, next_x, next_y, N)]
    moves.sort(key=lambda m: len([(m[0] + move_x[i], m[1] + move_y[i]) for i in range(8) if is_valid_move(board, m[0] + move_x[i], m[1] + move_y[i], N)]))

    for next_x, next_y in moves:
        if is_valid_move(board, next_x, next_y, N):
            board[next_x][next_y] = move_num
            if knight_tour_util(board, next_x, next_y, move_num + 1, move_x, move_y, N):
                return True

            # Backtrack
            board[next_x][next_y] = -1

    return False



