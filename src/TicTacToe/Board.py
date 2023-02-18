import copy

from Display import Display
from GameResult import GameResult
from BoardState import BoardState


class Board:

    SIZE = 3

    def __init__(self):
        # TODO: assert SIZE must >= 3
        self.available_moves = set([(r, c) for r in range(Board.SIZE) for c in range(Board.SIZE)])
        self.state = BoardState(Board.SIZE)
        self.display = Display(Board.SIZE)

    def __str__(self):
        return self.display.display_str

    def calculate_state_after_move(self, player, row, column):
        state_copy = copy.deepcopy(self.state)
        state_copy.update(player, row, column)
        return state_copy

    def make_move(self, player, row, column):
        # TODO: assert player must equal 1 or -1
        self.available_moves.remove((row, column))  # will error if the move isn't possible
        self.state.update(player, row, column)
        self.display.add_move_marker(player, row, column)

    def game_result(self, player, last_move_row, last_move_column):
        if self.state.has_winner(last_move_row, last_move_column):
            return GameResult.WINNER_1 if player == 1 else GameResult.WINNER_2

        if not self.available_moves:
            return GameResult.DRAW  # no more moves can be made

        return GameResult.INCOMPLETE


