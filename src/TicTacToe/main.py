from Agents import ValueLearningAgent, HumanAgent, RandomAgent
from Trainer import Trainer


if __name__ == '__main__':
    # takes ~2000 games to train with explore_rate=0.2, learning_rate=0.4, discount_factor=0.9
    a1 = ValueLearningAgent(player=1, explore_rate=0.0, learning_rate=0.1, discount_factor=0.9, state_value_file='state_values.pkl')
    a2 = ValueLearningAgent(player=-1, explore_rate=0.1, learning_rate=0.4, discount_factor=0.9)
    t = Trainer(a1, a2)
    t.train(10_000, 1_000)

    # a2 = HumanAgent(player=-1)

    # g = Game(a1, a2, debug=True)
    # g.play()

