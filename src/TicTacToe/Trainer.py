import os
import pickle

from Agents import LearningAgent, ValueLearningAgent
from GameResult import GameResult
from Game import Game


class Trainer:

    @staticmethod
    def train(n_games, agent_1, agent_2):
        if not isinstance(agent_1, LearningAgent) and not isinstance(agent_2, LearningAgent):
            print(f'Supply at least one Learning Agent to the Trainer.')
            return

        print(f'Training on {n_games} games')
        stats = TrainingStatistics(total_n_games=n_games, print_interval_percentage=0.1)

        for n_games_played in range(1, n_games+1):
            game = Game(agent_1, agent_2)
            game.play()

            stats.update_stats(game.game_result)
            stats.print_stats(n_games_played)

            if isinstance(agent_1, LearningAgent):
                agent_1.learn_from_result(game.game_states, game.game_result)
            if isinstance(agent_2, LearningAgent):
                agent_2.learn_from_result(game.game_states, game.game_result)

        Trainer.save_learned_values(agent_1, agent_2)

        print(f'Training on {n_games} games complete!')

    @staticmethod
    def training_stats(results, n_games):
        pass

    @staticmethod
    def save_learned_values(agent_1, agent_2):
        # simply save an agent's values; nothing more complex required for this game.
        if isinstance(agent_1, ValueLearningAgent):
            Trainer.save_agent_states_values(agent_1.state_values)
            return

        if isinstance(agent_2, ValueLearningAgent):
            Trainer.save_agent_states_values(agent_2.state_values)
            return

    @staticmethod
    def save_agent_states_values(state_values):
        file_path = os.path.dirname(__file__) + '/state_values.pkl'

        with open(file_path, 'wb') as file:
            pickle.dump(state_values, file)


class TrainingStatistics:

    def __init__(self, total_n_games, print_interval_percentage):
        self.print_interval = int(total_n_games * print_interval_percentage)

        self.n_win_1 = 0
        self.n_win_2 = 0
        self.n_draws = 0

    def update_stats(self, result):
        if result == GameResult.WINNER_1:
            self.n_win_1 += 1
            return

        if result == GameResult.WINNER_2:
            self.n_win_2 += 1
            return

        self.n_draws += 1

    def print_stats(self, n_played):
        if n_played == 0 or n_played % self.print_interval != 0:
            return

        rate_player_1 = round(self.n_win_1 * 100 / n_played, 3)
        rate_player_2 = round(self.n_win_2 * 100 / n_played, 3)
        rate_draw = round(self.n_draws * 100 / n_played, 3)

        print(f'Result Rates after {n_played} games: Player 1: {rate_player_1}%, Player 2: {rate_player_2}%, Draw: {rate_draw}%')
