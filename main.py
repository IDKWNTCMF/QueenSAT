import pycosat
import sys

if len(sys.argv) >= 2:
    n = int(sys.argv[1])
else:
    n = 8
clauses = []
board = [[' ' for _ in range(n)] for _ in range(n)]


def count_literal(r, c):
    return r * (n + 1) + c


def get_rc(lit):
    return lit // (n + 1) - 1, lit % (n + 1) - 1


def out(brd):
    tmp = ['-' for _ in range(n)]
    for r in range(n):
        print("|".join(brd[r]))
        if r != n - 1:
            print("+".join(tmp))


for row in range(1, n + 1):
    # Clause that at least one queen should be standing in each row
    clauses.append([count_literal(row, col) for col in range(1, n + 1)])
    for col in range(1, n + 1):
        for k in range(1, row):
            # Clauses that at most one queen should be standing in each column
            clauses.append([-count_literal(row, col), -count_literal(k, col)])
            if 0 < row + col - k <= n:
                # Clauses that at most one queen should be standing in / diagonal
                clauses.append([-count_literal(row, col), -count_literal(k, row + col - k)])
            if 0 < col - row + k <= n:
                # Clauses that at most one queen should be standing in \ diagonal
                clauses.append([-count_literal(row, col), -count_literal(k, col - row + k)])

        for k in range(1, col):
            # Clauses that at most one queen should be standing in each row
            clauses.append([-count_literal(row, col), -count_literal(row, k)])

ans = pycosat.solve(clauses)

if ans == "UNSAT":
    print("It is impossible to place n =", n, "queens!")
else:
    for literal in ans:
        if literal > 0:
            (row, col) = get_rc(literal)
            board[row][col] = 'Q'

    out(board)
