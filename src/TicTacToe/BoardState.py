class BoardState:

    def __init__(self, size):
        if size >= 3:
            ValueError(f'Supplied board size {size} is too small, must be >=3.')

        self.size = size

        self.row_score = [0] * size
        self.column_score = [0] * size
        self.diagonal_score = 0
        self.off_diagonal_score = 0

        self.squares = [[0 for _ in range(size)] for _ in range(size)]

    def __hash__(self):
        state_tuples = []
        for row in self.squares:
            state_tuples.append(tuple(row))
        return hash(tuple(state_tuples))

    def update(self, player, row, column):
        self.squares[row][column] = player

        self.row_score[row] += player
        self.column_score[column] += player
        if row == column:
            self.diagonal_score += player
        if row + column == self.size - 1:
            self.off_diagonal_score += player

    def has_winner(self, row, column):
        if abs(self.row_score[row]) == self.size or abs(self.column_score[column]) == self.size:
            return True

        if abs(self.diagonal_score) == self.size or abs(self.off_diagonal_score) == self.size:
            return True

        return False
