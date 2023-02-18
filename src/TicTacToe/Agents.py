from abc import abstractmethod
import pickle
import random

from GameResult import GameResult


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

    def __init__(self, player, learning_rate, explore_rate, discount_factor, state_value_file=None):
        super().__init__(player)

        self.learning_rate = learning_rate
        self.explore_rate = explore_rate
        self.discount_factor = discount_factor

        self.state_values = ValueLearningAgent.load_state_values(state_value_file)

    def select_move(self, current_board_state, possible_moves):
        if random.random() < self.explore_rate:
            return Agent.select_random_move(possible_moves)

        selected_value = -float('inf')
        selected_move = None

        for (row, column) in possible_moves:
            next_state = current_board_state.calculate_state_after_move(self.player, row, column)
            next_state_value = self.state_values.get(hash(next_state), 0) * self.player

            if next_state_value > selected_value:
                selected_value = next_state_value
                selected_move = (row, column)

        if not selected_move:
            # throw error
            pass

        return selected_move

    def learn_from_result(self, states, result):
        reward = ValueLearningAgent.determine_reward(result)

        for state in states[::-1]:
            if state not in self.state_values:
                self.state_values[state] = 0

            self.state_values[state] += self.learning_rate * (self.discount_factor * reward - self.state_values[state])
            reward = self.state_values[state]

    @staticmethod
    def determine_reward(result):
        if result == GameResult.DRAW:
            return 0

        if result == GameResult.WINNER_1:
            return 1

        return -1

    @staticmethod
    def load_state_values(file_name):
        if not file_name:
            return {}

        try:
            with open(file_name, "rb") as f:
                previous_computed_state_values = pickle.load(f)
                return previous_computed_state_values
        except FileNotFoundError:
            return {}

