from Agents import ValueLearningAgent, HumanAgent, RandomAgent
from Trainer import Trainer
from Game import Game


if __name__ == '__main__':
    auto_1 = ValueLearningAgent(player=1, explore_rate=0.2, learning_rate=0.4, discount_factor=0.9)
    auto_2 = ValueLearningAgent(player=-1, explore_rate=0.2, learning_rate=0.4, discount_factor=0.9)
    t = Trainer.train(10_000, auto_1, auto_2)

    human_1 = HumanAgent(player=1)
    trained_2 = ValueLearningAgent(player=-1, explore_rate=0, learning_rate=0.1, discount_factor=0.9, state_value_file='state_values.pkl')

    g = Game(human_1, trained_2, debug=True)
    g.play()

