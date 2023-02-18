import pickle

from Agents import LearningAgent
from GameResult import GameResult
from Game import Game


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

            if isinstance(self.agent_1, LearningAgent):
                self.agent_1.learn_from_result(game.game_states, game.game_result)
            if isinstance(self.agent_2, LearningAgent):
                self.agent_2.learn_from_result(game.game_states, game.game_result)

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
