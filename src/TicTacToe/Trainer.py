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
        game_results = []

        for n_games_played in range(n_games):
            game = Game(agent_1, agent_2)
            game.play()

            if isinstance(agent_1, LearningAgent):
                agent_1.learn_from_result(game.game_states, game.game_result)
            if isinstance(agent_2, LearningAgent):
                agent_2.learn_from_result(game.game_states, game.game_result)

            if n_games / (n_games_played+1) % 10 == 0:
                print(f'Training {round((n_games_played / n_games), 0)}% complete')

        Trainer.save_learned_values(agent_1, agent_2)
        Trainer.training_stats(game_results, n_games)

    @staticmethod
    def training_stats(results, n_games):
        pass

    @staticmethod
    def save_learned_values(agent_1, agent_2):
        if not isinstance(agent_1, LearningAgent) and not isinstance(agent_2, LearningAgent):
            return

        if isinstance(agent_1, ValueLearningAgent) and isinstance(agent_2, ValueLearningAgent):
            combined_learning = {}
            for key in agent_1.state_values.keys():
                if key in agent_2.state_values:
                    combined_learning[key] = (agent_1.state_values[key] + agent_2.state_values[key]) / 2
                else:
                    combined_learning[key] = agent_1.state_values[key]

            for key in agent_2.state_values.keys():
                if key not in agent_1.state_values:
                    combined_learning[key] = agent_2.state_values[key]

            Trainer.save_agent_states_values(combined_learning)
            return

        if isinstance(agent_1, ValueLearningAgent):
            Trainer.save_agent_states_values(agent_1.state_values)
            return

        if isinstance(agent_2, ValueLearningAgent):
            Trainer.save_agent_states_values(agent_2.state_values)
            return

    @staticmethod
    def save_agent_states_values(state_values):
        filename = 'state_values.pkl'

        with open(filename, 'wb') as file:
            pickle.dump(state_values, file)
