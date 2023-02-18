from abc import abstractmethod
import pickle
from enum import Enum
import copy
import random


class Display:

    CELL_WIDTH = 5
    VERTICAL_DIVIDER = "|"
    HORIZONTAL_DIVIDER = "-"
    PLAYER_1_MARKER = "X"
    PLAYER_2_MARKER = "O"

    def __init__(self, size):
        # TODO: test if this works on size > 3
        self.size = size
        self.total_row_width = Display.CELL_WIDTH * self.size + (self.size-1) * len(Display.VERTICAL_DIVIDER)

        self.display_str = self.__init_display_str()

    def add_move_marker(self, player, row, col):
        marker = Display.PLAYER_1_MARKER if player == 1 else Display.PLAYER_2_MARKER

        len_of_row_and_divider = (self.total_row_width + 1) * 2  # +1 to account for newline char in display_str rows

        # number of chars to skip to get to the display row that will add the marker
        index_for_start_of_cell_row = row * len_of_row_and_divider

        # number of chars to skip chars at start of col
        index_in_column = (Display.CELL_WIDTH + 1) * col + (Display.CELL_WIDTH // 2)  # marker in middle of cell

        market_index = index_for_start_of_cell_row + index_in_column

        self.display_str = self.display_str[:market_index] + marker + self.display_str[market_index+1:]

    def __init_display_str(self):
        cell = " " * Display.CELL_WIDTH
        empty_row = (cell + Display.VERTICAL_DIVIDER) * (self.size - 1) + cell + "\n"
        vertical_divider_row = Display.HORIZONTAL_DIVIDER * self.total_row_width + "\n"

        display_str = (empty_row + vertical_divider_row) * (self.size-1) + empty_row

        return display_str


class BoardState:

    def __init__(self, size):
        # TODO: assert SIZE must >= 3  <- just need a config validation
        self.size = size

        self.row_score = [0] * size
        self.column_score = [0] * size
        self.diagonal_score = 0
        self.off_diagonal_score = 0

        self.squares = [[0 for _ in range(size)] for _ in range(size)]

    def __str__(self):
        output_string = ''
        for row in self.squares:
            row_str = ''
            for cell in row:
                row_str += cell
            output_string += row_str + '\n'

        return output_string

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


class GameResult(Enum):
    INCOMPLETE = 0
    WINNER_1 = 1
    WINNER_2 = 2
    DRAW = 3


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
        # must return a copy of the state
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


class Agent:

    def __init__(self, player):
        self.player = player

    @abstractmethod
    def select_move(self, current_board_state, possible_moves):
        pass

    @staticmethod
    def select_random_move(possible_moves):
        selected_index = int(random.random() * len(possible_moves))
        return list(possible_moves)[selected_index]


class LearningAgent(Agent):

    def __init__(self, player):
        super().__init__(player)

    @abstractmethod
    def select_move(self, current_board_state, possible_moves):
        pass

    @abstractmethod
    def learn_from_result(self, states, result):
        pass


class RandomAgent(Agent):

    def __init__(self, player):
        super().__init__(player)

    def select_move(self, current_board_state, possible_moves):
        return Agent.select_random_move(possible_moves)


class HumanAgent(Agent):

    def __init__(self, player):
        super().__init__(player)

    def select_move(self, current_board_state, possible_moves):
        # human input is 1-indexed and the internal game state is 0 indexed, hence -1
        selected_row = int(input(f'Please type the row of the cell you want to select (1-{Board.SIZE})\n')) - 1
        selected_column = int(input(f'Please type the column of the cell you want to select (1-{Board.SIZE})\n')) - 1

        if (selected_row, selected_column) not in possible_moves:
            print(f'Selected location {(selected_row+1, selected_column+1)} not available. The square must be on the board and not already occupied')
            self.select_move(current_board_state, possible_moves)

        return selected_row, selected_column


class ValueLearningAgent(LearningAgent):

    def __init__(self, player, learning_rate, explore_rate, discount_factor):
        super().__init__(player)

        self.learning_rate = learning_rate
        self.explore_rate = explore_rate
        self.discount_factor = discount_factor

        self.state_values = ValueLearningAgent.load_state_values()

    def select_move(self, current_board_state, possible_moves):
        if random.random() < self.explore_rate:
            return Agent.select_random_move(possible_moves)

        selected_value = -float('inf')
        selected_move = None

        for (row, column) in possible_moves:
            next_state = current_board_state.calculate_state_after_move(self.player, row, column)
            next_state_value = self.state_values.get(hash(next_state), 0)

            if next_state_value > selected_value:
                selected_value = next_state_value
                selected_move = (row, column)

        if not selected_move:
            # throw error
            pass

        return selected_move

    def learn_from_result(self, states, result):
        reward = self.determine_reward(result)

        for state in states[::-1]:
            if state not in self.state_values:
                self.state_values[state] = 0

            self.state_values[state] += self.learning_rate * (self.discount_factor * reward - self.state_values[state])
            reward = self.state_values[state]

    def determine_reward(self, result):
        if result == GameResult.DRAW:
            return 0

        if self.player == 1 and result == GameResult.WINNER_1 or self.player == -1 and result == GameResult.WINNER_2:
            return 1

        return -1

    @staticmethod
    def load_state_values():
        try:
            with open("state_values.pkl", "rb") as f:
                previous_computed_state_values = pickle.load(f)
                return previous_computed_state_values
        except FileNotFoundError:
            return {}


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


class Trainer:

    def __init__(self, agent_1, agent_2):
        self.agent_1 = agent_1
        self.agent_2 = agent_2

    def train(self, n_games, batch_size):
        n_agent_1_wins_batch = 0
        n_agent_1_draws_batch = 0

        for n_games_played in range(n_games):
            game = Game(self.agent_1, self.agent_2)
            game.play()

            self.agent_1.learn_from_result(game.game_states, game.game_result)

            n_games_played += 1
            if game.game_result == GameResult.WINNER_1:
                n_agent_1_wins_batch += 1
            if game.game_result == GameResult.DRAW:
                n_agent_1_draws_batch += 1

            if n_games_played % batch_size == 0:
                print(f'Game {n_games_played} - Win rate {round((n_agent_1_wins_batch / batch_size) * 100, 3)}% | Draw rate {round((n_agent_1_draws_batch / batch_size) * 100, 3)}%')
                n_agent_1_wins_batch = 0
                n_agent_1_draws_batch = 0

        Trainer.save_agent_states_values(self.agent_1)

    @staticmethod
    def save_agent_states_values(agent):
        filename = 'state_values.pkl'

        with open(filename, 'wb') as file:
            pickle.dump(agent.state_values, file)


if __name__ == '__main__':
    a1 = ValueLearningAgent(player=1, explore_rate=0.0, learning_rate=0.15, discount_factor=0.9)
    a2 = HumanAgent(player=-1)

    # only took 2000 games to train with
    # explore_rate=0.15, learning_rate=0.4, discount_factor=0.9

    g = Game(a1, a2, debug=True)
    g.play()

    # t = Trainer(a1, a2)
    # t.train(1000, 100)
