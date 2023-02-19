# Re-enforcement Learning
This repository is for building and maintaining [Re-enforcement Learning Algorithms](https://en.wikipedia.org/wiki/Temporal_difference_learning). The initial focus is on building temporal-difference learning algorithms to play board-games of various complexity.

## How to play games
Games will be added over time, and the repository structure will develop depending which games are added. Use the subsections below to train and play games against RL-trained agents.

### TicTacToe
From the root of this repository, run:
`python3 src/TicTacToe/main.py`

This command will print out lines describing the results of the training games, then offer you the chance to make your first move to start a game of TicTacToe against the trained agent.

#### Technical Aspects
The **TicTacToe** agent uses a **state-value function** which is effective because there are fewer than 9! (362,880) possible states in a game with a 3x3 board. The agent is able to achieve perfect play with fewer than 10,000 training runs. If you are comfortable editing python code, you can change the parameter `Board.SIZE` and experiment with boards larger than 3x3.

#### Requirements
The entire program is writen in **python3** and only using base libraries.

### Connect Four
Not yet implemented - a 6*7 board with ~42! states

