from Board import Board
from GameResult import GameResult


class Game:

    def __init__(self, player_1_agent, player_2_agent, debug=False):
        self.board = Board()
        self.game_result = GameResult.INCOMPLETE
        self.turn = 0

        self.player_1_agent = player_1_agent
        self.player_2_agent = player_2_agent

        self.player_w_turn = 1
        self.active_agent = player_1_agent

        self.game_states = []

        self.debug = debug

        if self.debug:
            print("Game starting...")
            print(self.board)

    def play(self):
        while self.game_result == GameResult.INCOMPLETE:
            possible_moves = self.board.available_moves
            (selected_row, selected_column) = self.active_agent.select_move(self.board, possible_moves)
            self.board.make_move(self.player_w_turn, selected_row, selected_column)

            self.game_states.append(hash(self.board.state))

            self.game_result = self.board.game_result(self.player_w_turn, selected_row, selected_column)

            self.alternate_move()

            if self.debug:
                print(f"Turn: {self.turn}")
                print(self.board)

        if self.debug:
            Game.print_result(self.game_result)

    @staticmethod
    def print_result(result):
        if result == GameResult.DRAW:
            return print("Game Drawn...")

        if result == GameResult.WINNER_1:
            return print("Player 1 Wins!")

        return print("Player 2 Wins!")

    def alternate_move(self):
        self.turn += 1
        self.player_w_turn *= -1
        self.active_agent = self.player_1_agent if self.player_w_turn == 1 else self.player_2_agent
